import smtplib
from email.message import EmailMessage

def generate_email(nudge):
# Create email
       
    msg = EmailMessage()
    msg['Subject'] = 'BUDGET NUDGE NOTIFICATION'
    msg['From'] = 'jakelegacy560@gmail.com'
    msg['To'] = 'thunderhazk@gmail.com'
    msg.set_content(nudge)

    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('jakelegacy560@gmail.com', 'axbo bydt cyrs dsun')
        server.send_message(msg)

    print("Email sent successfully!")
generate_email("nudge generated")
