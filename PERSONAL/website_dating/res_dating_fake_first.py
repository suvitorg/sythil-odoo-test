from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime, timedelta
from random import randint
import random
import time

class ResDatingFakeFirst(models.Model):

    _name = "res.dating.fake.first"
    
    name = fields.Char(string='First Name')
    gender = fields.Char(string="Gender")
    amount = fields.Integer(string="Amount")