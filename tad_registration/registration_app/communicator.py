import requests
import json
import datetime
TIME_FORMAT = '%Y-%m-%d'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
BASE_URL = 'http://cloudinvoice.herokuapp.com/'
AUTH_CREDENTIALS = ('NICE', 'TRY')
class Communicator():
    """
    Class which will handle communication with other systems. Also handles communications to users (emails)
    """
    def __init__(self, registration):
        self._registration = registration

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
        """
        Sends invoice to cloudinvoicer. Saves invoice id from response to model
        """
        def construt_both_days_row(participants):
            ret = {
                'product_number': 1000,
                'name': 'Both days',
                'unit_price': 200,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret

        def construct_both_days_member_row(participants):
            ret = {
                'product_number': 1001,
                'name': 'Both days (member)',
                'unit_price': 180,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret

        def construct_conference_day_row(participants):
            ret = {
                'product_number': 1002,
                'name': 'Conference day',
                'unit_price': 140,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret
        def construct_conference_day_member_row(participants):
            ret = {
                'product_number': 1003,
                'name': 'Conference day (member)',
                'unit_price': 130,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret

        def construct_student_row(participants):
            ret = {
                'product_number': 1004,
                'name': 'Conference day (student)',
                'unit_price': 10,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret
        if self._registration.invoice_customer_id <= 0:
            raise ValueError('Registration must have invoice_customer_id before sending invoice')

        now = datetime.datetime.now()
        two_weeks = now + datetime.timedelta(days=14)
        payload = {}
        payload['invoice_date'] = now.strftime(TIME_FORMAT)
        payload['due_date'] = two_weeks.strftime(TIME_FORMAT)
        payload['customer_id'] = self._registration.invoice_customer_id
        if self._registration.billingtype_set.get().reference != '':
            payload['your_reference'] = self._registration.billingtype_set.get().reference
        payload['invoice_rows'] = []
        row_constructors = {
            'both_days': construt_both_days_row,
            'both_days_member': construct_both_days_member_row,
            'conference_day': construct_conference_day_row,
            'conference_day_member': construct_conference_day_member_row,
            'student': construct_student_row
        }

        for p_type in row_constructors.keys():
            participants = self._registration.participant_set.filter(participation_choice=p_type)
            if len(participants) > 0:
                row = row_constructors[p_type](participants)
                payload['invoice_rows'].append(row)

        response = requests.post(url = BASE_URL + 'invoices', data=json.dumps(payload), headers=HEADERS, auth=AUTH_CREDENTIALS)
        self._registration.invoice_invoice_id = response.json()['id']
        self._registration.save()


