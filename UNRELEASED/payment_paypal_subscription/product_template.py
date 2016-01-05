from openerp import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import requests
import logging
_logger = logging.getLogger(__name__)

class ProductTemplatePaymentPaypalSubscription(models.Model):

    _inherit = "product.template"

    payment_aquirer_id = fields.Many2one("payment.aquirer", string="Paypal Account")
    paypal_subscription_id = fields.Integer(string="Paypal Subscription ID", readonly=True)
    subscription_peroids = fields.One2many('product.subscription.cycle', 'product_id', string="Subscription Peroids")
    type = fields.Selection(selection_add=[('paypal_subscription','Subscription(Paypal)')])
    
    @api.one
    def create_paypal_subscription(self):
        
        payload = {'name': str(self.name),'description': str(self.description_purchase), 'type':'fixed', 'payment_definitions': my_payments}
        response_string = requests.post("https://api.sandbox.paypal.com/v1/payments/billing-plans", data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))

 class ProductSubscriptionCycle(models.Model):

    _name = "product.subscription.cycle"

    product_id = fields.Many2one("product.template", string="Product")
    subscription_peroids = fields.One2many('product.subscription.cycle', 'product_id', string="Subscription Peroids")
    type = fields.Selection(selection_add=[('paypal_subscription','Subscription(Paypal)')])   	