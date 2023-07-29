from django.db import models

from accounts.models import CustomUser
from photos.models import Album



class Relation(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_sender')

    RELATION_CHOICES =(
        ("UNDEFINED", "UNDEFINED"),
        ("SIBLING", "SIBLING"),
        ("PARENT/CHILDREN", "PARENT/CHILDREN"),
        ("COUSIN", "COUSIN"),
        ("AUNT-UNCLE/NEPHEW-NIECE", "AUNT-UNCLE/NEPHEW-NIECE"),
        ("GRANDPARENT/GRANDCHILDREN", "GRANDPARENT/GRANDCHILDREN"),
        ("BROTHER/SISTER IN LAW", "BROTHER/SISTER IN LAW"),
        ("FRIEND", "FRIEND"),
        )

    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES, default="UNDEFINED")

    class Meta:
        # Unique_together constraint to ensure unique pairs of users
        unique_together = ['user_receiving', 'user_sending']

    def save(self, *args, **kwargs):
        # Check if the interchangeable relation already exists
        if Relation.objects.filter(user_receiving=self.user_sending, user_sending=self.user_receiving).exists():
            # If it exists, don't save the new relation
            return
        super(Relation, self).save(*args, **kwargs)


class RelationRequest(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_req_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='relation_req_sender')

    RELATION_CHOICES =(
    ("UNDEFINED", "UNDEFINED"),
    ("SIBLING", "SIBLING"),
    ("PARENT/CHILDREN", "PARENT/CHILDREN"),
    ("COUSIN", "COUSIN"),
    ("AUNT-UNCLE/NEPHEW-NIECE", "AUNT-UNCLE/NEPHEW-NIECE"),
    ("GRANDPARENT/GRANDCHILDREN", "GRANDPARENT/GRANDCHILDREN"),
    ("BROTHER/SISTER IN LAW", "BROTHER/SISTER IN LAW"),
    ("FRIEND", "FRIEND"),
    )

    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES, default="UNDEFINED")

    class Meta:
        # Unique_together constraint to ensure unique pairs of users
        unique_together = ['user_receiving', 'user_sending']

# -------- Album Access ---------
class AlbumAccess(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='accesses')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_accesses')
    has_access = models.BooleanField(default=False)

# ------- Access Requests ---------
class AlbumAccessRequest(models.Model):
    user_receiving = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_receiver')
    user_sending = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='album_req_sender')
    message_from_sender = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
