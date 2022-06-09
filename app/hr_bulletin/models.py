from django.db import models
from enum import Enum
import datetime
from datetime import datetime as date_time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_image_file_extension, FileExtensionValidator
import logging
from app.hr_storage.storage_backends import PublicMediaStorage
from django.conf import settings

log = logging.getLogger(__name__)


class PostStatus(Enum):
    DRAFT = 'Draft'
    PUBLISHED = 'Published'
    REMOVED = 'Removed'

    def __str__(self):
        return self.value


def validate_date_published(date_submitted: date_time):
    if date_time.now() < date_submitted:
        raise ValidationError(
            _('%(date_submitted)s cannot be a future date'), params={'date_submitted': date_submitted},
        )
    elif date_submitted < date_time(2022, 6, 8, 13, 0, 0):
        raise ValidationError(
            _('%(date_submitted)s cannot be a date prior to this application\'s existence'), params={'date_submitted': date_submitted},
        )


class Post(models.Model):

    author = models.ForeignKey("hr_django.User", on_delete=models.PROTECT, related_name='posts')
    title = models.CharField(max_length=200, blank=False, null=False)
    subtitle = models.CharField(max_length=200, blank=True, null=True, default='')
    body = models.CharField(max_length=20000, blank=False, null=False)
    date_created = models.DateTimeField(auto_add_now=True)
    date_published = models.DateTimeField(null=True, blank=False, default=None, verbose_name="Date Published", validators=validate_date_published)
    date_last_modified = models.DateTimeField(default=None, null=True, blank=True)
    status = models.CharField(nax_length=50, choices=[(tag, tag.value) for tag in PostStatus])
    title_image_url = models.FileField(upload_to="media/bulletin", storage=PublicMediaStorage, max_length=1000, default=None, blank=True, null=True, validators=[FileExtensionValidator( [ '.jpg', '.jpeg', '.gif', '.png', '.WebP', '.bmp', '.svg' ])])

    def __str__(self):
        return f'{self.title} by {self.author}, {self.date_created}'

class PostImage(models.Model):

    @property
    def thumbnail_preview(self):
        from django.utils.html import mark_safe
        if self.image:
            return mark_safe('<img src="{}" width="150" height="150" object-fit="cover"/>'.format(self.image.url))

    image = models.ImageField(storage=PublicMediaStorage, upload_to=None, null=True, blank=False)
    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name="post_images")
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="post_images")


def get_readable_date(target_date: date_time) -> str:
    return f'{target_date.month} {target_date.day}, {target_date.year}'
