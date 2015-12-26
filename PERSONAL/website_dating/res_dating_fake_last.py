from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime, timedelta
from random import randint
import random
import time

class ResDatingFakeLast(models.Model):

    _name = "res.dating.fake.last"
    
    name = fields.Char(string='First Name')
    amount = fields.Integer(string="Amount")