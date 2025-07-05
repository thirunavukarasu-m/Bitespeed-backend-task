from models import db, Contact

def get_primary_contact(email = None, phone_number = None):
    """
    Retrieve the primary contact for a given contact ID.
    
    Args:
        contact_id (int): The ID of the contact.
        
    Returns:
        Contact: The primary contact object if found, otherwise None.
    """
    if email:
        return Contact.query.filter_by(email=email, linkPrecedence='primary').first()
    
    if phone_number:
        return Contact.query.filter_by(phoneNumber=phone_number, linkPrecedence='primary').first()
    
    return "Please provide either an email or a phone number to retrieve the primary contact."

def get_secondary_contacts(primary_contact_id):
    """
    Retrieve secondary contacts linked to a primary contact.
    
    Args:
        primary_contact_id (int): The ID of the primary contact.
        
    Returns:
        list: A list of secondary contacts linked to the primary contact.
    """
    
    return Contact.query.filter_by(linkedId=primary_contact_id, linkPrecedence='secondary').with_entities(Contact.id, Contact.email, Contact.phoneNumber).all() if primary_contact_id else None

def create_contact(phone, email, contact_type, linked_id = None):

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