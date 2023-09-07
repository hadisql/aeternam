from django.db.models.signals import post_delete
from django.dispatch import receiver

from accounts.models import Relation
from .models import AlbumAccess

@receiver(post_delete, sender=Relation)
def delete_album_access(sender, instance, **kwargs):
    user1 = instance.user_sending
    user2 = instance.user_receiving

    try:
        # if relation is deleted, both users lose access to albums they used to have given to each other
        album_access1 = AlbumAccess.objects.filter(album__creator=user1, user=user2)
        album_access2 = AlbumAccess.objects.filter(album__creator=user2, user=user1)
        for access in album_access1:
            access.delete()
            print(f"Deleted access for {access.user}")
        for access in album_access2:
            access.delete()
            print(f"Deleted access for {access.user}")
    except AlbumAccess.DoesNotExist:
        pass
