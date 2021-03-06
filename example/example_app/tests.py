from os.path import join
from math import sqrt
from functools import reduce
from operator import add
from PIL import Image
from django.test import (
    TestCase,
    override_settings,
)
from django.conf import settings
from django_snippet_image import __version__

from .models import (
    ExampleModel,
    Statuses,
)

ASSETS_PATH = join(settings.BASE_DIR, 'example_app/assets/')

BACKGROUND_FILE = join(ASSETS_PATH, 'background.jpg')
PURPOSE_IMAGE_WITH_BACKGROUND = join(ASSETS_PATH, 'snippet-image-with-background.jpg')
PURPOSE_IMAGE_WITH_SIZE = join(ASSETS_PATH, 'snippet-image-with-size.jpg')
PURPOSE_IMAGE_WITH_SIZE_AND_BACKGROUND = join(ASSETS_PATH, 'snippet-image-with-size-and-background.jpg')
PURPOSE_IMAGE_WITHOUT_BACKGROUND = join(ASSETS_PATH, 'snippet-image-without-background.jpg')


class SnippetImageTestCase(TestCase):
    text = 'What time is it?'

    def test_version(self):
        self.assertEqual(__version__, '0.1.3')

    def test_should_be_created(self):
        instance = ExampleModel(
            text=self.text,
            status=Statuses.DRAFT,
        )
        instance.save()
        self.assertIsNone(instance.snippet_image_field.name)

    def test_with_background(self):
        instance = ExampleModel(
            text=self.text,
            status=Statuses.PUBLISH,
        )

        with open(BACKGROUND_FILE, 'rb') as background_file:
            instance.background.save('background.jpg', background_file)

        instance.save()
        rms = compare_image(instance.snippet_image_field.path, PURPOSE_IMAGE_WITH_BACKGROUND)
        self.assertEqual(rms, 0)

    @override_settings(
        SNIPPET_IMAGE_DEFAULT_OVERLAY=None,
        SNIPPET_IMAGE_DEFAULT_SIZE=(1200, 630),
    )
    def test_with_size(self):
        instance = ExampleModel(
            text=self.text,
            status=Statuses.PUBLISH,
        )
        instance.save()
        rms = compare_image(instance.snippet_image_field.path, PURPOSE_IMAGE_WITH_SIZE)
        self.assertEqual(rms, 0)

    @override_settings(
        SNIPPET_IMAGE_DEFAULT_OVERLAY=None,
        SNIPPET_IMAGE_DEFAULT_SIZE=(1200, 630),
    )
    def test_with_size_and_background(self):
        instance = ExampleModel(
            text=self.text,
            status=Statuses.PUBLISH,
        )

        with open(BACKGROUND_FILE, 'rb') as background_file:
            instance.background.save('background.jpg', background_file)

        instance.save()
        rms = compare_image(instance.snippet_image_field.path, PURPOSE_IMAGE_WITH_SIZE_AND_BACKGROUND)
        self.assertEqual(rms, 0)

    def test_without_background(self):
        instance = ExampleModel(
            text=self.text,
            status=Statuses.PUBLISH,
        )
        instance.save()
        rms = compare_image(instance.snippet_image_field.path, PURPOSE_IMAGE_WITHOUT_BACKGROUND)
        self.assertEqual(rms, 0)


def compare_image(result_image, purpose_file):
    result_image = Image.open(result_image)
    purpose_image = Image.open(purpose_file)
    rms = compare_images_histograms(
        result_image,
        purpose_image,
    )

    return rms


def compare_images_histograms(source, purpose):
    source_histogram = source.histogram()
    purpose_histogram = purpose.histogram()
    rms = sqrt(
        reduce(
            add,
            map(
                lambda a, b: (a - b) ** 2,
                source_histogram,
                purpose_histogram,
            )
        ),
    )

    return rms
