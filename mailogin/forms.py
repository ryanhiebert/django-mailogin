from django import forms
from django.template.loader import get_template


class EmailForm(forms.Form):
    email = forms.EmailField()

    def send_email(self, text_template, html_template=None, signer=None):
        """Send an email to the given email address.

        Render the given `template` with a link constructed by the `signer`.
        """
        plain = get_template(text_template)
        html = get_template(html_template)


class EmailLoginForm(forms.Form):
    """Process the email login link data."""
