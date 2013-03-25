# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Registration'
        db.create_table(u'registration_app_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact_person', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('organisation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('billing_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('invoice_customer_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('invoice_invoice_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'registration_app', ['Registration'])

        # Adding model 'Participant'
        db.create_table(u'registration_app_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('participation_choice', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('conference_dinner', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('special_diet', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('t_shirt_size', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('twitter_account', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('other_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration_app.Registration'])),
        ))
        db.send_create_signal(u'registration_app', ['Participant'])

        # Adding model 'BillingType'
        db.create_table(u'registration_app_billingtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('vat_no', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('recipient', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration_app.Registration'])),
        ))
        db.send_create_signal(u'registration_app', ['BillingType'])

        # Adding model 'NormalBillingType'
        db.create_table(u'registration_app_normalbillingtype', (
            (u'billingtype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration_app.BillingType'], unique=True, primary_key=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'registration_app', ['NormalBillingType'])

        # Adding model 'PostBillingType'
        db.create_table(u'registration_app_postbillingtype', (
            (u'billingtype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration_app.BillingType'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('post_office', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('extra_info', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'registration_app', ['PostBillingType'])

        # Adding model 'EBillingType'
        db.create_table(u'registration_app_ebillingtype', (
            (u'billingtype_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration_app.BillingType'], unique=True, primary_key=True)),
            ('billing_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('operator', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'registration_app', ['EBillingType'])


    def backwards(self, orm):
        # Deleting model 'Registration'
        db.delete_table(u'registration_app_registration')

        # Deleting model 'Participant'
        db.delete_table(u'registration_app_participant')

        # Deleting model 'BillingType'
        db.delete_table(u'registration_app_billingtype')

        # Deleting model 'NormalBillingType'
        db.delete_table(u'registration_app_normalbillingtype')

        # Deleting model 'PostBillingType'
        db.delete_table(u'registration_app_postbillingtype')

        # Deleting model 'EBillingType'
        db.delete_table(u'registration_app_ebillingtype')


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
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['registration_app']