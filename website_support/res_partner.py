from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class ResPartnerTicket(models.Model):

    _inherit = "res.partner"
    
    support_ticket_ids = fields.One2many('website.support.ticket', 'partner_id', string='Tickets')
    support_ticket_count = fields.Integer(string="Ticket Count")