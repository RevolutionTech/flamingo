"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

import os

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from flamingo.tests import FlamingoTestCase
from photo.models import Photo


class PhotoTestCase(FlamingoTestCase):

    PHOTO_TITLE = 'John Smith'
    PHOTO_DESCRIPTION = 'A photo of John Smith and Pocahontas.'
    TEST_PHOTOS_DIR = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'testphotos'
    )

    def tearDown(self):
        Photo.objects.all().delete()
        super(PhotoTestCase, self).tearDown()

    def testUserAddPhoto(self):
        # Get photo from testphotos/ directory
        photo_filename = 'jsmith.jpg'
        photo_full_filename = os.path.join(
            self.TEST_PHOTOS_DIR,
            photo_filename
        )
        try:
            jsmith_image_content = open(photo_full_filename, 'rb').read()
        except IOError:
            raise IOError(
                "Test photo \"{photo_filename}\" missing or could not be read."
                    .format(photo_filename=photo_filename)
            )
        jsmith_image = SimpleUploadedFile(
            name=photo_filename,
            content=jsmith_image_content,
            content_type='image/jpeg'
        )

        # Create photo instance
        Photo.objects.create(
            user_profile=self.user_profile,
            title=self.PHOTO_TITLE,
            img=jsmith_image,
            description=self.PHOTO_DESCRIPTION
        )
        self.assertEquals(Photo.objects.all().count(), 1)
        photo = Photo.objects.get()

        # Verify photo properties
        self.assertEquals(
            unicode(photo),
            self.PHOTO_TITLE
        )
        self.assertEquals(
            photo.title,
            self.PHOTO_TITLE
        )
        self.assertEquals(
            photo.description,
            self.PHOTO_DESCRIPTION
        )
        jsmith_img = Image.open(jsmith_image)
        img = Image.open(photo.img)
        self.assertEquals(img.width, jsmith_img.width)
        self.assertEquals(img.height, jsmith_img.height)
