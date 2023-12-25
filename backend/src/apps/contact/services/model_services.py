from apps.accounts.models import User
from apps.contact.models import Contact


def create_contact_by_users(connecting_user: User, user: User):
    contact = Contact.objects.create()
    contact.connect.add(connecting_user, user)
    contact.save()
    
    return contact