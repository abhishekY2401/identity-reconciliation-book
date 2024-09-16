from app.models.contact import Contact
from app.database import db
from datetime import datetime, timezone


def reconcile_contact(phone_number=None, email=None):
    """
    Reconcile customer identity based on phone number or email.
    If no match is found, create a primary contact.
    If a match is found, consolidate with the existing primary contact.
    """

    # Ensure that at least one of phone_number or email is provided
    if not phone_number and not email:
        raise ValueError(
            "At least one of phone_number or email must be provided.")

    # Find all contacts that match either the email or phone_number
    matching_contacts = Contact.query.filter(
        (Contact.phone_number == phone_number) | (Contact.email == email)
    ).all()

    if not matching_contacts:
        # No matches found, create a new primary contact
        new_contact = Contact(
            phone_number=phone_number,
            email=email,
            link_precedence='primary',
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        db.session.add(new_contact)
        db.session.commit()

        # Prepare response with the new primary contact and empty secondary IDs
        return prepare_reconciliation_response(new_contact)

    # List to store primary and secondary contacts
    primary_contact = None
    secondary_contacts = []

    # Identify the primary contact and collect all secondary contacts
    for contact in matching_contacts:
        if contact.link_precedence == 'primary':
            if primary_contact is None or contact.created_at < primary_contact.created_at:
                primary_contact = contact
            else:
                # If we find a newer primary, convert it to secondary
                contact.link_precedence = 'secondary'
                contact.linked_id = primary_contact.id
                contact.updated_at = datetime.now(timezone.utc)
                db.session.add(contact)
                db.session.commit()
                secondary_contacts.append(contact)
        else:
            secondary_contacts.append(contact)

    if not primary_contact:
        # No primary contact found, the first secondary should point to its linked primary
        primary_contact = Contact.query.filter_by(
            id=matching_contacts[0].linked_id).first()

    # Check if any secondary or primary contact has the same phone and email combination
    existing_contact = Contact.query.filter_by(
        phone_number=phone_number, email=email).first()
    if existing_contact:
        # If a contact with the same phone number and email already exists, avoid creating a duplicate
        return prepare_reconciliation_response(primary_contact, secondary_contacts)

    # Check if new information (either phone or email) is provided
    new_information = False
    if primary_contact.phone_number != phone_number and phone_number:
        new_information = True
    if primary_contact.email != email and email:
        new_information = True

    if new_information:
        # Create a new secondary contact with the provided phone/email only if it's not a duplicate
        new_secondary = Contact(
            phone_number=phone_number,
            email=email,
            linked_id=primary_contact.id,
            link_precedence='secondary',
        )
        db.session.add(new_secondary)
        db.session.commit()
        secondary_contacts.append(new_secondary)

    # Check if any two primary contacts need merging (this logic demotes the newer primary)
    for contact in matching_contacts:
        if contact.link_precedence == 'primary' and contact != primary_contact:
            # Merge by making the newer primary a secondary contact of the older primary
            secondary_contacts.append(contact)
            contact.link_precedence = 'secondary'
            contact.linked_id = primary_contact.id
            contact.updated_at = datetime.now(timezone.utc)
            db.session.add(contact)
            db.session.commit()

    # Prepare and return the consolidated response
    return prepare_reconciliation_response(primary_contact, secondary_contacts)


def prepare_reconciliation_response(primary_contact, secondary_contacts=None):
    """
    Prepares a response consolidating all linked contacts, including phone numbers, emails, and IDs.

    Args:
        primary_contact (Contact): The primary contact.
        secondary_contacts (list, optional): List of secondary contacts.

    Returns:
        dict: Consolidated response.
    """
    if secondary_contacts is None:
        secondary_contacts = []

    emails = set()
    phone_numbers = set()
    secondary_contact_ids = set()

    # Add primary contact details
    if primary_contact.email:
        emails.add(primary_contact.email)
    if primary_contact.phone_number:
        phone_numbers.add(primary_contact.phone_number)

    # Add details from all secondary contacts
    for contact in secondary_contacts:
        if contact.email:
            emails.add(contact.email)
        if contact.phone_number:
            phone_numbers.add(contact.phone_number)
        secondary_contact_ids.add(contact.id)

    # Query for any other secondary contacts linked to the same primary
    other_secondary_contacts = Contact.query.filter_by(
        linked_id=primary_contact.id).all()
    for contact in other_secondary_contacts:
        if contact.email:
            emails.add(contact.email)
        if contact.phone_number:
            phone_numbers.add(contact.phone_number)
        secondary_contact_ids.add(contact.id)

    # Prepare response in the required format
    response_data = {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": list(emails),
            "phoneNumbers": list(phone_numbers),
            "secondaryContactIds": list(secondary_contact_ids)
        }
    }

    return response_data
