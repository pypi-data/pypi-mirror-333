from cms.models import CMSPlugin
from django import forms
from django.apps import apps
from django.db import models
from django.utils.translation import gettext as _
from easy_thumbnails.fields import ThumbnailerImageField
from parler.models import TranslatableModel, TranslatedFields

# HTMLField is a custom field that allows to use a rich text editor
# Probe for djangocms_text first, then for djangocms_text_ckeditor
# and finally fallback to a simple textarea
if (
    apps.is_installed('djangocms_text')
    or apps.is_installed('djangocms_text.contrib.text_ckeditor4')
    or apps.is_installed('djangocms_text.contrib.text_ckeditor5')
    or apps.is_installed('djangocms_text.contrib.text_quill')
    or apps.is_installed('djangocms_text.contrib.text_tinymce')
):
    from djangocms_text.fields import HTMLField
elif apps.is_installed('djangocms_text_ckeditor'):
    from djangocms_text_ckeditor.fields import HTMLField
else:

    class HTMLField(models.TextField):
        def __init__(self, *args, **kwargs):
            kwargs.setdefault('widget', forms.Textarea)
            super().__init__(*args, **kwargs)


class Album(TranslatableModel):
    translations = TranslatedFields(
        name=models
        .CharField(blank=True, max_length=100, verbose_name=_('name of album'))
    )

    class Meta:
        verbose_name: str = _('album')
        verbose_name_plural: str = _('albums')

    def __str__(self):
        return self.name or _('– no name –')


class AlbumPicture(TranslatableModel):
    """Album picture with caption and copyright notice"""
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, verbose_name=_('album')
    )
    picture = ThumbnailerImageField(
        upload_to='djangocms_photo_gallery', verbose_name=_('picture')
    )
    translations = TranslatedFields(
        title=models.CharField(
            blank=True, max_length=50, verbose_name=_('title')
        ),
        caption=HTMLField(blank=True, verbose_name=_('caption')),
        copyright_notice=models.CharField(
            blank=True, max_length=50, verbose_name=_('copyright notice')
        )
    )

    class Meta:
        verbose_name: str = _('album picture')
        verbose_name_plural: str = _('album pictures')

    def __str__(self):
        return f'{self.caption}'


class AlbumPlugin(CMSPlugin):
    album = models.ForeignKey(
        Album, verbose_name=_('album'), on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.album.name}'
