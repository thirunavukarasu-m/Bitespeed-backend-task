from models import db, Contact

def get_primary_contact(phone_contact, email_contact, resolve_hierarchy=False):
    """
    Determines and returns the primary contact from given phone or email contact objects.

    Args:
        phone_contact (Contact, Required): Contact object matched via phone number.
        email_contact (Contact, Required): Contact object matched via email.
        resolve_hierarchy (bool): If True, compare createdAt timestamps to determine primary.
                                  If False, returns the primary from whichever object exists.

    Returns:
        Contact: The resolved primary Contact object.
    """

    if resolve_hierarchy:
        valid_object = phone_contact if phone_contact.createdAt <= email_contact.createdAt else email_contact
    else:
        valid_object = phone_contact or email_contact

    # Get true primary contact if this is a secondary
    primary_contact_id = valid_object.id if valid_object.linkPrecedence == 'primary' else valid_object.linkedId
    return Contact.query.get(primary_contact_id)



def get_secondary_contacts(primary_contact_id):
    """
    Retrieve secondary contacts linked to a primary contact.
    
    Args:
        primary_contact_id (int): The ID of the primary contact.
        
    Returns:
        list: A list of secondary contacts linked to the primary contact.
    """
    
    return Contact.query.filter_by(linkedId=primary_contact_id, linkPrecedence='secondary').with_entities(Contact.id, Contact.email, Contact.phoneNumber).all() if primary_contact_id else None

def create_contact(phone, email, contact_type, linked_id=None):
    """
    Creates a new contact record in the database.

    Args:
        phone (str): The phone number of the contact.
        email (str): The email address of the contact.
        contact_type (str): Either "primary" or "secondary", indicating the role of the contact.
        linked_id (int, optional): If the contact is secondary, this links to the primary contact's ID.

    Returns:
        Contact: The newly created Contact object.
    """
    contact = Contact(
        phoneNumber=phone,
        email=email,
        linkPrecedence=contact_type,
        linkedId=linked_id
    )
    db.session.add(contact)
    db.session.commit()
    return contact

def format_response(primary_contact, secondary_contacts=None):
    """
    Formats the contact information into a structured JSON response.

    Args:
        primary_contact (Contact): The main contact record to be shown as primary.
        secondary_contacts (list, optional): A list of secondary contact records (tuples or Contact objects).

    Returns:
        dict: A dictionary structured for JSON response with:
              - primaryContactId (int)
              - emails (list of unique emails)
              - phoneNumbers (list of unique phone numbers)
              - secondaryContactIds (list of linked contact IDs)
    """
    emails = list(dict.fromkeys(
        contact.email for contact in [primary_contact] + (secondary_contacts or []) if contact.email
    ))
    phonenumbers = list(dict.fromkeys(
        contact.phoneNumber for contact in [primary_contact] + (secondary_contacts or []) if contact.phoneNumber
    ))

    return {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": emails,
            "phoneNumbers": phonenumbers,
            "secondaryContactIds": [row[0] for row in secondary_contacts] if secondary_contacts else []
        }
    }
