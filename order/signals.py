from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Order

def create_order_permissions(sender, **kwargs):
    order_content_type = ContentType.objects.get_for_model(Order)

    admin_group, _ = Group.objects.get_or_create(name='Admins')
    admin_group.permissions.add(
        Permission.objects.get(codename='add_order', content_type=order_content_type),
        Permission.objects.get(codename='change_order', content_type=order_content_type),
        Permission.objects.get(codename='delete_order', content_type=order_content_type),
        Permission.objects.get(codename='view_order', content_type=order_content_type),
    )

from django.db.models.signals import post_migrate
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        post_migrate.connect(create_order_permissions, sender=self)
