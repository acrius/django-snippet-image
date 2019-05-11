from django.db.models import (
    Model,
    CharField,
    ImageField,
)
from django_snippet_image import SnippetImageField


class Statuses:
    DRAFT = 'draft'
    PUBLISH = 'publish'

    CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISH, 'Publish'),
    )


class ExampleModel(Model):
    text = CharField(
        max_length=200,
        verbose_name='Text for snippet image',
    )
    background = ImageField(
        verbose_name='Background for snippet image',
        blank=True,
        null=True,
    )
    snippet_image_field = SnippetImageField(
        verbose_name='Example snippet image field',
        null=True,
    )
    status = CharField(
        max_length=20,
        choices=Statuses.CHOICES,
    )

    # Methods for collect data for snippet image.

    def get_snippet_image_text(self, snippet_type):
        return self.text if snippet_type == 'default' and self.text else ''

    def get_snippet_image_background(self, snippet_type):
        if snippet_type == 'default' and self.background:
            return self.background.path

    def snippet_image_should_be_created(self):
        return self.status == Statuses.PUBLISH

    class Meta:
        verbose_name = 'example object'
        verbose_name_plural = 'example objects'
