# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Registration.organisation'
        db.alter_column(u'registration_app_registration', 'organisation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Registration.organisation'
        raise RuntimeError("Cannot reverse this migration. 'Registration.organisation' and its values cannot be restored.")

    models = {
        u'registration_app.billingtype': {
            'Meta': {'object_name': 'BillingType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipient': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration_app.Registration']"}),
            'vat_no': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'registration_app.ebillingtype': {
            'Meta': {'object_name': 'EBillingType', '_ormbases': [u'registration_app.BillingType']},
            'billing_address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'billingtype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration_app.BillingType']", 'unique': 'True', 'primary_key': 'True'}),
            'operator': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'registration_app.normalbillingtype': {
            'Meta': {'object_name': 'NormalBillingType', '_ormbases': [u'registration_app.BillingType']},
            u'billingtype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration_app.BillingType']", 'unique': 'True', 'primary_key': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'})
        },
        u'registration_app.participant': {
            'Meta': {'object_name': 'Participant'},
            'conference_dinner': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'other_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'participation_choice': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration_app.Registration']"}),
            'special_diet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            't_shirt_size': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_account': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'registration_app.postbillingtype': {
            'Meta': {'object_name': 'PostBillingType', '_ormbases': [u'registration_app.BillingType']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'billingtype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration_app.BillingType']", 'unique': 'True', 'primary_key': 'True'}),
            'extra_info': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'post_office': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'registration_app.registration': {
            'Meta': {'object_name': 'Registration'},
            'billing_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_person': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_customer_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_invoice_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['registration_app']