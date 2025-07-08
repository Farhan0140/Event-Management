from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from app_admin.models import Event
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.models import Group


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
        

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_RENDER_URL}/user/activate/{instance.id}/{token}/"

        try:
            send_mail(
                "Activate your Account",
                f"Hi, {instance.username},\n\nPlease activate your account by clicking the link below\n\n{activation_url}\n\n\nThank You for your registration....",
                "settings.EMAIL_HOST_USER",
                [instance.email],
                fail_silently=False,
            )
        except Exception as e:
            print("Failed to send message")



@receiver(post_save, sender=User)
def assigning_default_role(sender, instance, created, **kwargs):
    if created:
        user_group, created_or_exists = Group.objects.get_or_create(name="Participant")
        instance.groups.add(user_group)
        instance.save()

