from django.conf import settings
from django.core.mail import send_mail
from django_rq import job


@job
def deliver_certificate(base_url, student):
    subject = 'Your Grade Certificate - Lumino'

    message = f"""
    Hello {student.get_full_name()}!
    
    Your grade certificate has been generated.
    
    You can download it from: {base_url}/media/certificates/{student.username}_certificate.pdf
    
    Best regards,
    The Lumino Team
    """
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student.email],
        fail_silently=False,
    )

    return f'Certificate email sent to {student.email}'
