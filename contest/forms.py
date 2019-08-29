"""
:Created: 1 November 2015
:Author: Lucas Connors

"""

from django import forms
from django.conf import settings


class UploadPhotoForm(forms.Form):

    image = forms.ImageField()

    def clean_image(self):
        image = self.cleaned_data['image']
        if image.size > settings.MAXIMUM_IMAGE_SIZE:
            raise forms.ValidationError("Image file too large (2MB maximum).")
        return image
