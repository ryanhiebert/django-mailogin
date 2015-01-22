from django.core import signing
from django.core.mail import send_mail
from django.views.generic import FormView
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.contrib.auth import get_user_model

from .forms import EmailForm


class EmailLoginStartView(FormView):
    form_class = EmailForm
    subject_template = None
    text_template = None
    html_template = None
    pattern_name = None

    def form_valid(self, form):
        self.send_email(form.email)
        return super(EmailLoginStartView, self).form_valid(form)

    def send_email(self, email):
        """Send a login or registration email to the given address."""
        path = reverse(self.pattern_name, args=[signing.dumps(email, salt='mailogin')])
        context = Context({'url': self.request.build_absolute_uri(path)})

        subject = get_template(self.subject_template).render(context)
        text = get_template(self.text_template).render(context)
        html = get_template(self.html_template).render(context)
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(subject, text, from_email, [email], html_message=html)


class EmailLoginStopView(RedirectView):
    create_pattern_name = None
    success_pattern_name = None
    failure_pattern_name = None

    def get_redirect_url(self, cipher):
        try:
            email = signing.loads(cipher, salt='mailogin')
        except signing.BadSignature:
            return reverse(self.failure_pattern_name)

        User = get_user_model()

        try:
            user, created = User.objects.get_or_create(
                email=email, defaults={'username': email})
        except User.MultipleObjectsReturned:
            return reverse(self.failure_pattern_name)

        return reverse(create_pattern_name if created else success_pattern_name)
