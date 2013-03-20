import requests
import json
# DEBUG
from models import Registration
# END DEBUG
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
BASE_URL = 'http://cloudinvoice.herokuapp.com/'
AUTH_CREDENTIALS = ('Nice', 'Try')
class Communicator():
    """
    Class which will handle communication with other systems. Also handles communications to users (emails)
    """
    def __init__(self, registration=None):
        self._registration = Registration.objects.get(pk=1)

    def send_customer_registration(self):
        """
        Sends customer registration to cloudinvoicer. Saves customer id from response to model
        """
        def add_email_payload(payload):
            billing_type = self._registration.billingtype_set.get()
            payload['email'] = billing_type.normalbillingtype.email_address

        def add_post_payload(payload):
            billing_type = self._registration.billingtype_set.get()
            post_type = billing_type.postbillingtype
            payload['street_address'] = post_type.address
            payload['zip'] = post_type.postal_code
            payload['city'] = post_type.post_office

        payload = {}
        payload['name'] = self._registration.contact_person
        payload['contact_person'] = self._registration.billingtype_set.get().recipient
        {'post': add_post_payload, 'email': add_email_payload}[self._registration.billing_type](payload)
        response = requests.post(url = BASE_URL + 'customers', data=json.dumps(payload), headers=HEADERS, auth=AUTH_CREDENTIALS)
        self._registration.invoice_customer_id = response.json()['id']
        self._registration.save()

    def send_invoice_registration(self):
        pass
