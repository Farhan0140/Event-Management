from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from app_admin.models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail


@receiver(m2m_changed, sender=Event.participant.through)
def for_rsvp(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        user_email = []

        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            user_email.append(user.email)
            
        send_mail (
            f"RSVP Confirmation",
            f"Your RSVP completed successfully for {instance.event_name} event ",
            "djangomama11@gmail.com",
            user_email,
            fail_silently=False,
        )
        