import os
from dotenv import load_dotenv
from groq import Groq
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


load_dotenv(dotenv_path=".env")

api_key = os.getenv("GROQ_API_KEY")

print("API KEY:", api_key)

client = Groq(api_key=api_key)

def generate_nudge(food_spend, threshold, personality, projection):

    overspend_amount = food_spend - threshold

    prompt = f"""
    User spent ₹{food_spend} on food delivery.
    Budget threshold ₹{threshold}.
    Overspent ₹{overspend_amount}.
    Projected spend ₹{projection}.

    Personality: {personality}

    Generate a short funny financial nudge.
    Keep under 2 lines.
    """
    nudge = ""
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            temperature=0.8
        )
        nudge = chat_completion.choices[0].message.content
        generate_email(nudge)
        return nudge

    except Exception as e:
        return f"ERROR: {str(e)}"
print("API KEY:", api_key)