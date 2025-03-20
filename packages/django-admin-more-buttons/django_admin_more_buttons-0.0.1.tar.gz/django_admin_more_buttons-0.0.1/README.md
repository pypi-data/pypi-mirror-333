# More buttons in admin

Add more buttons with custom behavior to your admin's submit line.

## Using

1. Add `admin_buttons` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "admin_buttons",
]
```

2. Mix our class in your `ModelAdmin`, and define a `admin_buttons_config`
   attribute:


```python
from admin_buttons.admin import AdminButtonsMixin
from django.contrib import admin
from django.db import models
from django.shortcuts import redirect


class SpecialModelAdmin[M: models.Model](AdminButtonsMixin, admin.ModelAdmin[M]):
    """
    ModelAdmin for models that do something special. Their special thing
    will be done upon the click of a button
    """

    admin_buttons_config = [
        {
            # the button html name
            "name": "_dosomethingspecial",

            # the method to be called when clicking the button
            "method": "do_something_special",

            # The button label
            "label": _("Do something very special"),

            # Optionally, define a condition. If it does not pass, the
            # button will not be displayed
            "condition": lambda request, context: (
                request.user.has_perm("someperm")
                and not re.search(r"add/?$", request.path)
            ),

            # Optionally, include extra html after the button
            "extra_html": mark_safe_lazy(
                '<input type="number" step=1 min=1 max=99 value=1 '
                'name="n_times" aria-label="'
                f'{_("Number of times do to something special")}">'
            ),

            # Optionally, use a separator before this button:
            use_separator: True,
        },
    ]

    # The chosen method works as a view. Therefore, it should return a response
    # To simply return to the change view, redirect to HTTP_REFERER, as below:
    def do_something_special(self, request: HttpRequest, obj: M | None):
        obj.something_special()
        return redirect(request.META["HTTP_REFERER"])

```

## Development

All contributions are welcome! To setup development:

1. `pip install -r dev.requirements.txt`
2. `pre-commit install`
