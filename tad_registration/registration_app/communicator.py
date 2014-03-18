import requests
import json
import datetime
import tad_registration.settings as settings

from django.core.mail import EmailMessage, send_mail

TIME_FORMAT = '%Y-%m-%d'
HEADERS = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
BASE_URL = 'http://cloudinvoice.herokuapp.com/'
AUTH_CREDENTIALS = settings.CLOUDINVOICE_CREDENTIALS
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

        def add_ebilling_payload(payload):
            billing_type = self._registration.billingtype_set.get()
            e_billing = billing_type.ebillingtype
            payload['edi_address'] = e_billing.billing_address
            payload['edi_operator'] = e_billing.operator

        payload = {}
        payload['name'] = self._registration.contact_person
        payload['contact_person'] = self._registration.billingtype_set.get().recipient
        {'post': add_post_payload, 'email': add_email_payload, 'ebilling': add_ebilling_payload}[self._registration.billing_type](payload)
        response = requests.post(url = BASE_URL + 'customers', data=json.dumps(payload), headers=HEADERS, auth=AUTH_CREDENTIALS)
        if response.status_code == 201:
            self._registration.invoice_customer_id = response.json()['id']
            self._registration.save()
        else:
            raise RuntimeError("Invalid status code")

    def send_invoice_registration(self):
        """
        Sends invoice to cloudinvoicer. Saves invoice id from response to model
        """
        def construt_both_days_row(participants):
            ret = {
                'product_number': 1000,
                'name': 'Both days',
                'unit_price': 220,
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
                'unit_price': 160,
                'vat_percent': 0,
                'amount': len(participants)
            }
            return ret
        def construct_conference_day_member_row(participants):
            ret = {
                'product_number': 1003,
                'name': 'Conference day (member)',
                'unit_price': 125,
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

        def construct_extra_billing_row():
            ret = {
                'product_number': 1005,
                'name': 'Invoice cost',
                'unit_price': 5,
                'vat_percent': 0,
                'amount': 1
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

        if self._registration.billing_type != 'email':
            payload['invoice_rows'].append(construct_extra_billing_row())

        response = requests.post(url = BASE_URL + 'invoices', data=json.dumps(payload), headers=HEADERS, auth=AUTH_CREDENTIALS)
        if response.status_code == 201:
            self._registration.invoice_invoice_id = response.json()['id']
            self._registration.save()
        else:
            raise RuntimeError("Invalid status code")

    def _download_invoice(self):
        invoice_id = self._registration.invoice_invoice_id
        pdf_location = '{url}invoices/{invoice_id}.pdf'.format(url=BASE_URL, invoice_id=invoice_id) 
        response = requests.get(url = pdf_location, headers=HEADERS, auth=AUTH_CREDENTIALS)
        if response.status_code == 200:
            return response.content
        else:
            raise RuntimeError("Invalid status code")

    def send_invoice_email(self):
        """
        Sends email about registration to user. Expects that billing_type is email and email is set
        """
        to = self._registration.billingtype_set.get().normalbillingtype.email_address
        subject = 'Your registration for Turku Agile Day 2014'
        message = 'Thank you for your registration to Turku Agile Day 2014! Your registration has been successfully recorded.\n\nAttached is an invoice for the participation fee. If you need the invoice as either e-invoice or via traditional post, please inform us at invoicing@turkuagileday.fi. A handling fee of 5 EUR is applied for e-invoices and paper invoices sent via post.\n\nIf you have any questions about the event or your registration, please don\'t hesitate to contact us at info@turkuagileday.fi!\n\nYours,\n-- \nTurku Agile Day team\ninfo@turkuagileday.fi'

        invoice = self._download_invoice()
        email = EmailMessage(subject, message, 'registration@turkuagileday.fi', (to, ))
        email.attach('tad_invoice.pdf', invoice, 'application/pdf')
        email.send()

    def send_notification_email(self):
        """
        Sends notification mail to NOTIFICATION_RECEIVERS
        """

        to = self._registration.email_address
        subject = 'Your registration for Turku Agile Day 2014'
        message = 'Thank you for your registration to Turku Agile Day 2014! Your registration has been successfully recorded.\n\nThe invoice for your registration will be sent to you separately via the method of your choice.\n\nIf you have any questions about the event or your registration, please don\'t hesitate to contact us at info@turkuagileday.fi!\n\nYours,\n-- \nTurku Agile Day team\ninfo@turkuagileday.fi'
        email = EmailMessage(subject, message, 'registration@turkuagileday.fi', (to, ))
        email.send()

        invoice = self._download_invoice()
        subject = 'Message from TAD-registration system'
        message = 'Turku Agile Day registration system received invoice which requires your attention!'
        email = EmailMessage(subject, message, 'registration@turkuagileday.fi', settings.NOTIFICATION_RECEIVERS)
        email.attach('tad_invoice.pdf', invoice, 'application/pdf')
        email.send()
