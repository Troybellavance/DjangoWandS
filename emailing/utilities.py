import json
import requests
from django.conf import settings


MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)



class MailchimpEmailing(object):
    def __init__(self):
        super(MailchimpEmailing, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(api_url=self.api_url, list_id=self.list_id)

    def check_if_subscribed(self, email):
        endpoint = self.api_url
        req = requests.get(endpoint, auth=("", self.key))
        return req.json()

    def check_validity_status(self, status):
        options = ['subscribed','unsubscribed','cleaned','pending']
        if status not in options:
            raise ValueError("Not a valid status for emails")
        return status

    def add_email_subscription(self, email):
        status = "subscribed"
        self.check_validity_status(status)
        data = {
             "email_address": email,
             "status": status
        }
        endpoint = self.list_endpoint + "/members"
        req = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        return req.json()
