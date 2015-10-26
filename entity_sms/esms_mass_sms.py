from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class esms_mass_sms(models.Model):

    _name = "esms.mass.sms"
    
    from_mobile = fields.Many2one('esms.verified.numbers', required=True, string="From Mobile", domain="[('mobile_verified','=','True')]")
    selected_records = fields.Many2many('res.partner', required=True, string="Selected Records", domain="[('sms_opt_out','=',False)]")
    message_text = fields.Text(string="Message Text", required=True)
    total_count = fields.Integer(string="Total", compute="_total_count")
    fail_count = fields.Integer(string="Failed", compute="_fail_count")
    queue_count = fields.Integer(string="Queue", compute="_queue_count")
    sent_count = fields.Integer(string="Sent", compute="_sent_count")
    delivered_count = fields.Integer(string="Received", compute="_delivered_count")
    mass_sms_state = fields.Selection((('draft','Draft'),('sent','Sent')), readonly=True, string="State", default="draft")
    
    @api.one
    @api.depends('selected_records')
    def _total_count(self):
        self.total_count = len(self.selected_records)

    @api.one
    def _fail_count(self):
        self.fail_count = self.env['esms.history'].search_count([('mass_sms_id','=','self.id'), ('status_code','=','failed')])
        
    @api.one
    def _queue_count(self):
        self.queue_count = self.env['esms.history'].search_count([('mass_sms_id','=','self.id'), ('status_code','=','queued')])

    @api.one
    def _sent_count(self):
        self.sent_count = self.env['esms.history'].search_count([('mass_sms_id','=','self.id'), ('status_code','=','successful')])

    @api.one
    def _delivered_count(self):
        self.delivered_count = self.env['esms.history'].search_count([('mass_sms_id','=','self.id'), ('status_code','=','DELIVRD')])
    
    @api.one
    def send_mass_sms(self):
        self.mass_sms_state = "sent"
        for rec in self.selected_records:
            message_final = self.message_text + "\nReply STOP to stop receiving sms"
            gateway_model = self.from_mobile.account_id.account_gateway.gateway_model_name
	    my_sms = self.env[gateway_model].send_message(self.from_mobile.account_id.id, self.from_mobile.mobile_number, rec.mobile_e164, message_final, "esms.mass.sms", self.id, "mobile")
            my_model = self.env['ir.model'].search([('model','=','res.partner')])
            
            #unlike single sms we record down failed attempts to send since mass sms works in a "best try" matter, while single sms works in a "try again" matter.
            esms_history = self.env['esms.history'].create({'mass_sms_id': self.id, 'record_id': rec.id,'model_id':my_model[0].id,'account_id':self.from_mobile.account_id.id,'from_mobile':self.from_mobile.mobile_number,'to_mobile':rec.mobile_e164,'sms_content':message_final,'status_string':my_sms.response_string, 'direction':'O','my_date':datetime.utcnow(), 'status_code':my_sms.delivary_state, 'sms_gateway_message_id':my_sms.message_id, 'gateway_id': self.from_mobile.account_id.account_gateway.id})