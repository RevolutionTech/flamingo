"""
:Created: 15 August 2015
:Author: Lucas Connors

"""

from PIL import Image

from flamingo.tests import FlamingoTestCase
from photo.models import Photo


class PhotoTestCase(FlamingoTestCase):

    PHOTO_FILENAME = 'jsmith.jpg'
    PHOTO_TITLE = 'John Smith'
    PHOTO_DESCRIPTION = 'John Smith and Pocahontas.'

    def testUserAddPhoto(self):
        # Delete default photos
        Photo.objects.all().delete()

        # Create photo instance
        image, photo = self.create_test_photo(
            user_profile=self.user_profile,
            title=self.PHOTO_TITLE,
            filename=self.PHOTO_FILENAME,
            description=self.PHOTO_DESCRIPTION
        )
        self.assertEquals(Photo.objects.all().count(), 1)

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
        original_image = Image.open(image)
        stored_image = Image.open(photo.img)
        self.assertEquals(stored_image.width, original_image.width)
        self.assertEquals(stored_image.height, original_image.height)


class PhotoAdminWebTestCase(FlamingoTestCase):

    def testPhotoAppAdminPageRenders(self):
        response = self.client.get('/admin/photo/')
        self.assertEquals(response.status_code, 200)

    def testPhotoChangelistAdminPageRenders(self):
        response = self.client.get('/admin/photo/photo/')
        self.assertEquals(response.status_code, 200)

    def testPhotoAddAdminPageRenders(self):
        response = self.client.get('/admin/photo/photo/add/')
        self.assertEquals(response.status_code, 200)

    def testPhotoChangeAdminPageRenders(self):
        url = '/admin/photo/photo/{photo_id}/change/'.format(
            photo_id=self.photo.id
        )
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
