from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class rpom_product_template(models.Model):

    _inherit = "product.template"

    rpom_publish_online = fields.Boolean(string="Online Directory")
