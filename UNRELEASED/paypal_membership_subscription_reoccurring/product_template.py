from openerp import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)

class product_template_pmsr(models.Model):

    _inherit = "product.template"

    paypal_subscription_id = fields.Char(string="Paypal Subscription ID")
    trail_period_duration = field.Integer(string="Trail Period Duration")
    trail_period_unit = fields.Selection((('DAY','Days'), ('MONTH','Months')), string="Trail Period Unit")
    membership_period_amount = field.Integer(string="Membership Period Amount")
    membership_period_frequency = fields.Selection((('MONTH','Monthly')), string="Membership Period Frequency")