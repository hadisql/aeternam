from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model
from albums.models import Album, AlbumAccess
from photos.models import Photo, PhotoAccess
from django.conf import settings
from django.core.files import File
import os
from django.db import models
from accounts.models import Relation
import itertools
from random import shuffle

import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class Command(BaseCommand):
    help = 'Create albums and grant access to users'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of albums to create')
        parser.add_argument('user_email', type=str, help='Email from whom album will be created')
        parser.add_argument('--access', nargs='+', type=str, help='List of user emails to grant access to albums')
        parser.add_argument('--album_name', nargs='+', type=str, help='Names of the albums')
        parser.add_argument('--fill_photos', nargs='+', type=str, help='Number of photos to fill for each album')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        user_email = kwargs['user_email']
        access_emails = kwargs.get('access', [])
        album_names = kwargs.get('album_name', [])
        fill_photos = kwargs.get('fill_photos', [])

        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with email '{user_email}' does not exist."))
            return

        fake_photos_dir = os.path.join(settings.MEDIA_ROOT, 'fake_photos')
        photo_files = os.listdir(fake_photos_dir)
        shuffle(photo_files) # allows to fill photo album differently between two create_albums (for different users), but doesn't prevent same photos to be saved accross users
        photo_files_cycle = itertools.cycle(photo_files)

        for i in range(count):
            # Set album name if provided, otherwise use default naming
            if album_names:
                album_title = album_names[i] if i < len(album_names) else f"Album {i}"
            else:
                album_title = f"Album {i}"

            # ## TEST
            # if fill_photos and i < len(fill_photos):
            #     num_photos = int(fill_photos[i])
            #     print(f"for album {i}, num_photos = {num_photos}")
            #     self.test_photos(photo_files_cycle, num_photos)
            # ##

            album = Album.objects.create(title=album_title, creator=user)
            self.stdout.write(self.style.WARNING(f"Album '{album_title}' created successfully."))

            # Fill album with photos
            if fill_photos and i < len(fill_photos):
                num_photos = int(fill_photos[i])
                self.create_photos(album, num_photos, photo_files_cycle)


            # Case where --access set to "all"
            if access_emails and len(access_emails) == 1 and access_emails[0] == "all":
                logger.info(f"Access will be given to ALL user's relations")
                relations = Relation.objects.filter(models.Q(user_receiving=user) | models.Q(user_sending=user))
                access_emails = []
                for relation in relations:
                    if relation.user_receiving == user:
                        access_emails.append(relation.user_sending.email)
                    else:
                        access_emails.append(relation.user_receiving.email)

            # Grant access to users
            if access_emails:
                for email in access_emails:
                    try:
                        access_user = User.objects.get(email=email)
                        AlbumAccess.objects.create(album=album, user=access_user)
                        self.stdout.write(self.style.SUCCESS(f"Access is given to {email}."))
                        album_photos = Photo.objects.filter(album=album)
                        # logger.info(f"album has photos : {album_photos}")
                        if album_photos:
                            for photo in album_photos:
                                # logger.info(f"granting photo access to photo {photo.id}")
                                PhotoAccess.objects.create(photo=photo, user=access_user)
                                self.stdout.write(self.style.SUCCESS(f"Access is given for photo {photo.id}."))
                    except User.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"User with email '{email}' does not exist."))
                # we add photo accesses for the user himself
                if album_photos:
                    for photo in album_photos:
                        logger.info(f"granting photo access to photo {photo.id} for album creator himself.")
                        PhotoAccess.objects.create(photo=photo, user=user)
            else:
                album_photos = Photo.objects.filter(album=album)
                if album_photos:
                    for photo in album_photos:
                        logger.info(f"granting photo access to photo {photo.id} for the user himself.")
                        PhotoAccess.objects.create(photo=photo, user=user)
                self.stdout.write(self.style.WARNING(f"No access was given to other users."))

    def create_photos(self, album, num_photos, photo_files_cycle):
        fake_photos_dir = os.path.join(settings.MEDIA_ROOT, 'fake_photos')

        first = True # used to set first photo as cover photo
        for _ in range(num_photos):
            photo_file = next(photo_files_cycle)
            photo_path = os.path.join(fake_photos_dir, photo_file)
            with open(photo_path, 'rb') as f:
                if first:
                    first = False
                    photo = Photo(album=album, uploaded_by=album.creator, is_default=True)
                else:
                    photo = Photo(album=album, uploaded_by=album.creator)
                photo.image.save(photo_file, File(f))

            if 'resized' in photo.image.name:
                # delete the original copied photo if photo has been resized
                resized_photo_dir = os.path.join(settings.MEDIA_ROOT, f'albums/{photo.album.id}')
                try:
                    os.remove(os.path.join(resized_photo_dir, photo_file))
                    logger.info(f"original photo {photo_file} was deleted successfully from album directory.")
                except:
                    logger.warning(f"original photo {photo_file} not found in album directory.")

        self.stdout.write(self.style.SUCCESS(f"{num_photos} photos added to the album."))


    # def test_photos(self, photo_files_cycle, num_photos):

    #     for _ in range(num_photos):
    #         photo_file = next(photo_files_cycle)
    #         logger.info(f"adding photo {photo_file} to the album")
