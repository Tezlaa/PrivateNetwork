from django.db import transaction
from django.db.models import QuerySet, Subquery, OuterRef

from apps.accounts.models import User
from apps.contact.models import Contact


@transaction.atomic
def create_contact_by_users(request_user: User, user: User) -> Contact:
    contact = Contact.objects.filter(connect__in=[user, request_user])
    if contact.count() < 2:
        contact = Contact.objects.create()
        contact.connect.add(user, request_user)
    
    return contact


def get_contact_by_user(user: User) -> QuerySet[Contact]:
    return Contact.objects.filter(connect__in=[user]).annotate(
        connect_user=Subquery(
            Contact.objects.filter(pk=OuterRef('id')).values('connect__username')
        )
    )