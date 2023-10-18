from accounts.models import CustomUser
from photos.models import Photo, PhotoAccess
from albums.models import Album, AlbumAccess
from django.db.models import Q

all_users = CustomUser.objects.all()

for user in all_users:
	concerned_photos = Photo.objects.filter(
		Q(uploaded_by=user) | Q(album__creator__exact=user) | Q(album__album_accesses__user=user)
	)
	for photo in concerned_photos:
		if not PhotoAccess.objects.filter(photo=photo, user=user):
			PhotoAccess.objects.create(photo=photo, user=user)
