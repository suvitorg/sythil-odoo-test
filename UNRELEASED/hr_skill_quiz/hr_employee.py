from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class Employee(models.Model):

    _inherit = "hr.employee"
    
    skill_ids = fields.One2many('hr.skill.comp', 'employee_id', string="Skills", help="List of skills this employee possess")