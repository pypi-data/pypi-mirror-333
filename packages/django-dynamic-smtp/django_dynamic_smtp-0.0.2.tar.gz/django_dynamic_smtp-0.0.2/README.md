# Django dynamic SMTP

Configure email configuration in the admin.

## Usage

1. Install with `pip install django-dynamic-smtp`

2. Add `dynamic_smtp` to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...,
    "dynamic_smtp",
]
```

3. Configure your email backend:

```
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "dynamic_smtp.email.DynamicSMPTEmailBackend"
)
```

4. Migrate: `./manage.py migrate`
5. Access you admin and configure your SMTP settings

## Dependencies

This package needs quite a few dependencies, considering its simplicity.

- `Django`
- `beautifulsoup4` and `lxml`: prepare text version of HTML emails
- `django-object-actions`: Button for email test
- `django-tinymce`: Button for email test
- `django-solo`: Use singleton model

## Contributing

All contributions are welcome! To setup you environment:

1. `pip install -r dev.requirements.txt`
2. `pre-commit install`
