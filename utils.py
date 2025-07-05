from models import Contact

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

def get_secondary_contact_ids(primary_contact_id):
    """
    Retrieve secondary contacts linked to a primary contact.
    
    Args:
        primary_contact_id (int): The ID of the primary contact.
        
    Returns:
        list: A list of secondary contacts linked to the primary contact.
    """
    
    return [row[0] for row in Contact.query.filter_by(linkedId=primary_contact_id, linkPrecedence='secondary').with_entities(Contact.id).all()]if primary_contact_id else []


