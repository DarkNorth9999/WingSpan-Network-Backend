from app.models.user import User
from app.database import get_db
from app.models.subscription import Subscription
from app.integrations.breevo_email import send_emails
from app.integrations.twilio_sms import send_sms

async def process_notification( flight_id: str, message: str):
    db_gen = get_db()
    db = next(db_gen)
    subscriptions = db.query(Subscription).filter_by(flight_id=flight_id).all()
    email_list = []
    phone_list = []

    for subscription in subscriptions:
        user = db.query(User).filter_by(user_id=subscription.user_id).first()
        if subscription.email:
            email_list.append(user.email)
        if subscription.phone_number:
            phone_list.append(user.phone)

    if email_list:
        await send_emails(email_list, message)
    if phone_list:
        await send_sms(phone_list, message)



# async def send_emails(email_list, message):
#     for email in email_list:
#         print(f"Sending email to {email}: {message}")
#
# async def send_sms(phone_list, message):
#     for phone in phone_list:
#         print(f"Sending SMS to {phone}: {message}")