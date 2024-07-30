import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

configuration = sib_api_v3_sdk.Configuration()

configuration.api_key['api-key'] = os.getenv('BREEVO_API_KEY')

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

def send_email(subject, html, to_address=None, receiver_username=None):
    subject = subject
    sender = {"name": "Yash", "email": "yugitoabyss@gmail.com"}
    html_content = html

    if to_address:
        to = [{"email": "yashyashaggarwal@gmail.com", "name": "Yash Aggarwal"}]
    else:
        to = [{"email": "yashyashaggarwal@gmail.com", "name": "Yash Aggarwal"}]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)



async def send_emails(email_list, message):
    sender = {"name": "Yash", "email": "yugitoabyss@gmail.com"}
    to = [{"email": address, "name": address.split('@')[0]} for address in email_list]

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        text_content=message,
        sender=sender,
        subject="Flight Notification"
    )

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        print(f"Exception when calling SMTPApi->send_transac_email: {e}")

