from django.core.mail import EmailMessage


def receipt_creation_mail(seller_mail, name):
    email = EmailMessage(
            'Purchase receipt', 'Here is your receipt.', 'settings.EMAIL_HOST_USER', [seller_mail])
    email.attach_file('pdfprint/'+name+'.pdf')
    email.send()