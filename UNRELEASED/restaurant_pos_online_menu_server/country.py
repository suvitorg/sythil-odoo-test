from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class rpoms_country(models.Model):

    _inherit = "res.country"
    
    restaurant_count = fields.Integer(string='Restaurant Count')
