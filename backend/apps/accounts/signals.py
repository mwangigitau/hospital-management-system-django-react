from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Role, User


@receiver(post_save, sender=User)
def sync_user_group_from_role(sender, instance, **kwargs):
    if not instance.role_id:
        return

    role_group, _ = Group.objects.get_or_create(name=instance.role.name)
    role_groups = Group.objects.filter(name__in=Role.objects.values_list('name', flat=True)).exclude(pk=role_group.pk)
    if role_groups.exists():
        instance.groups.remove(*role_groups)
    instance.groups.add(role_group)
