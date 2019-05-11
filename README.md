# django-snippet-image

The python package provides a django field for automatic
generation of images for sharing in social networks.

django-snippet-image based on [snippet-image](https://github.com/acrius/snippet-image) package.

## Installation

```
pip3 install django-snippet-image
```

## User guide

Import package field:

```python
from django_snippet_image import SnippetImageField
```

Use it in model:

```python
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
```

Set static params:

```python
snippet_image_field = SnippetImageField(
        overlay='/user/python/app/assets/overlay.png',
        background_color=(0, 75, 125),
        font='/user/python/app/assets/OpenSans-Bold.ttf',
        verbose_name='Example snippet image field',
        null=True,
    )
```

Set dynamic params. They are set using model methods:

```python
def get_snippet_image_text(self, snippet_type):
    return self.text if snippet_type == 'default' and self.text else ''

def get_snippet_image_background(self, snippet_type):
    if snippet_type == 'default' and self.background:
        return self.background.path
```

Full example:

```python
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

```

And use in template:

```html
<meta property="og:image" content="{{ instance.snippet_image_field.url }}" />
```

## API

A SnippetImageField can be given static parameters in the field constructor,
and methods can be used to pass on dynamic values.

A SnippetImageField based on django ImageField  and takes its parameters.

ImageField params:

* verbose_name;
* name;
* width_field;
* height_field;
* upload_to;
* storage;
* null;

Param ```blank``` always is ```True```.

Auxiliary params:

* snippet_type (str) - String type of field. By default is 'default'. Read more below.

Params for create snippet sharing image:

* size (tuple(int, int)) - Size of snippet image. (width, height).
* text (str) - Text of snippet image. By default is an empty string.
* background (str) - Path to background image file.
* background_color (tuple(int, int, int)) - Background color of snippet image. Used when background is None.
                                            By default is (0, 0, 0).
* overlay (str) - Path to overlay image. if size is None, overlay size is used.
                  As an overlay, an image with a transparent background is used.
* brightness (float)- Brightness of background of snippet image. Value from 0 to 1.
* font_color(tuple(int, int, int, int)) - RGBA font color. By default is (255, 255, 255, 255).
* font_size (int) - Size of snippet image text. By default is 64.
* padding (float) - Text indents to the left and right of the snippet image.
                    Value from 0 to 1.
                    0 - 0% width;
                    1 - 100% width.
* center tuple(int, int) - Background image center for crop and resize image. (x, y).
                    Defaults is center of background image.
                    
More read on create snippet sharing image in [here](https://github.com/acrius/snippet-image).

If the parameter for generating the image is not transferred to the structure,
field will try to get it through the model method, like as ```get_snippet_image_{param}```.

For example:

```python
def get_snippet_image_text(self, snippet_type):
    return self.text if snippet_type == 'default' and self.text else ''

def get_snippet_image_background(self, snippet_type):
    if snippet_type == 'default' and self.background:
        return self.background.path
```

In order to distinguish for which field the data is requested,
the snippet_type parameter is used.

In order to determine whether to create an image snippet_image_should_be_created method of model is used.
The method returns true if you want to create an image and false if not needed.

## Example

To run the example, install dependencies, for example use poetry:

```
poetry install
```

Go to the example directory and execute:

```
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

And go to admin in ```localhost:8000/admin```

## Test

To run tests, install dependencies, for example use poetry:

```
poetry install
```

Go to the example directory and execute:

```
python3 manage.py test
```
