import hashlib
import json
import re
import requests
from django.conf import settings


MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

def check_email_format(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError("String is not a valid email address")
    return email

def subscriber_hash(member_email):
    check_email_format(member_email)
    member_email = member_email.lower().encode()
    mail = hashlib.md5(member_email)
    return mail.hexdigest()

class MailchimpEmailing(object):
    def __init__(self):
        super(MailchimpEmailing, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(dc=MAILCHIMP_DATA_CENTER)
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = '{api_url}/lists/{list_id}'.format(api_url=self.api_url, list_id=self.list_id)

    def get_members_endpoint(self):
        return self.list_endpoint + "/members"

    def check_sub_status(self, email):
        hashed_email = subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        req = requests.get(endpoint, auth=("", self.key))
        return req.status_code, req.json()

    def change_sub_status(self, email, status='unsubscribed'):
        hashed_email = subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        data = {
            "email_address":email,
            "status": self.check_validity_status(status)
        }
        req = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return req.status_code, req.json()

    def check_validity_status(self, status):
        options = ['subscribed','unsubscribed','cleaned','pending']
        if status not in options:
            raise ValueError("Not a valid status for emails")
        return status

    def add_email_subscription(self, email):
        # status = "subscribed"
        # self.check_validity_status(status)
        # data = {
        #      "email_address": email,
        #      "status": status
        # }
        # endpoint = self.get_members_endpoint()
        # req = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        # return req.json()
        return self.change_sub_status(email, status='subscribed')

    def subscribe_user(self, email):
        return self.change_sub_status(email, status='subscribed')

    def unsubscribe_user(self, email):
        return self.change_sub_status(email, status='unsubscribed')

    def pending_user(self, email):
        return self.change_sub_status(email, status='pending')

    ##Add guest useraccounts to emailing subscription
