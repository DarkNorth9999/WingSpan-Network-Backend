# Import SendinBlue library
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

load_dotenv()

# Create a SendinBlue API configuration
configuration = sib_api_v3_sdk.Configuration()

# Replace "<your brevo api key here>" with your actual SendinBlue API key
configuration.api_key['api-key'] = os.getenv('BREEVO_API_KEY')

# Initialize the SendinBlue API instance
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# Define the email sender function
def send_email(subject, html, to_address=None, receiver_username=None):
    # SendinBlue mailing parameters
    subject = subject
    sender = {"name": "Yash", "email": "yugitoabyss@gmail.com"}
    html_content = html

    # Define the recipient(s)
    if to_address:
        # You can add multiple email accounts to which you want to send the mail in this list of dicts
        to = [{"email": "yashyashaggarwal@gmail.com", "name": "Yash Aggarwal"}]
    else:
        to = [{"email": "yashyashaggarwal@gmail.com", "name": "Yash Aggarwal"}]

    # Create a SendSmtpEmail object
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
        return {"message": "Email sent successfully!"}
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


# # Send the email and store the response
# email_response = send_email('Hello World', "<h1>Welcome to the real world</h1>", "any", "s")
#
# # Print the status of the email sending process
# print(email_response)




# import sib_api_v3_sdk
# from sib_api_v3_sdk.rest import ApiException
#
# # Configure API key authorization: api-key
# configuration = sib_api_v3_sdk.Configuration()
# configuration.api_key['api-key'] = "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"
# api_instance = sib_api_v3_sdk.SMTPApi(sib_api_v3_sdk.ApiClient(configuration))

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

