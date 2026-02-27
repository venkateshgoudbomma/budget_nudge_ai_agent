import smtplib
from email.message import EmailMessage

def generate_email(nudge):
# Create email
       
    msg = EmailMessage()
    msg['Subject'] = 'BUDGET NUDGE NOTIFICATION'
    msg['From'] = 'agent email'
    msg['To'] = 'user email'
    msg.set_content(nudge)

    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login('agent email', 'password')
        server.send_message(msg)

    print("Email sent successfully!")
generate_email("nudge generated")

