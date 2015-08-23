from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class esms_gateways(models.Model):

    _name = "esms.gateways"
    
    name = fields.Char(required=True, string='Gateway Name')
    gateway_model_name = fields.Char(required='True', string='Gateway Model Name')

class esms_accounts(models.Model):

    _name = "esms.accounts"
    _order ="priority asc"
    
    name = fields.Char(required=True, string='Account Name')
    account_gateway = fields.Many2one('esms.gateways', required=True)
    gateway_model = fields.Char(related="account_gateway.gateway_model_name")
    priority = fields.Integer(string="Priority", default="100")

class esms_compose_multi(models.TransientModel):

    _name = "esms.compose.multi"
    
    sms_gateway = fields.Many2one('esms.accounts', required=True, string='Account/Number')
    sms_content = fields.Text('SMS Content')
    
    @api.one
    def send_sms_multi(self):
        for send_to in self._context['active_ids']:
            my_model = self._context['active_model']
            p_mobile = self.env[my_model].search([('id','=',send_to)])[0].mobile
	    gateway_model = self.sms_gateway.account_gateway.gateway_model_name
            my_sms = self.env[gateway_model].send_sms(self.sms_gateway.id, p_mobile, self.sms_content, my_model, send_to, 'mobile')


class esms_compose(models.TransientModel):

    _name = "esms.compose"
    
    error_message = fields.Char(readonly=True)
    record_id = fields.Integer()
    model_id = fields.Char()
    sms_gateway = fields.Many2one('esms.accounts', required=True, string='SMS Gateway Account')
    to_number = fields.Char(required=True, string='To Mobile Number', readonly=True)
    sms_content = fields.Text(string='SMS Content')
    field_id = fields.Char(string='Field Name')
    template_id = fields.Many2one('esms.templates', string="Template")
    
    @api.onchange('template_id')
    def load_template(self):
        if self.template_id.id != False:
            
            sms_rendered_content = self.env['esms.templates'].render_template(self.template_id.template_body, self.template_id.model_id.model, self.record_id)
    
            self.sms_content = sms_rendered_content
            self.sms_gateway = self.template_id.account_gateway.id

    @api.multi
    def send_entity(self):
        self.ensure_one()
        
        gateway_model = self.sms_gateway.account_gateway.gateway_model_name
        my_sms = self.env[gateway_model].send_message(self.sms_gateway.id, self.env.user.partner_id.mobile, self.to_number, self.sms_content, self.model_id, self.record_id, self.field_id)
        
        #use the human readable error message if present
        error_message = ""
        if my_sms.human_read_error != "":
            error_message = my_sms.human_read_error
        else:
            error_message = my_sms.response_string
            
	#display the screen with an error code if the sms/mms was not successfully sent
	if my_sms.delivary_state == "failed":
	   return {
	   'type':'ir.actions.act_window',
	   'res_model':'esms.compose',
	   'view_type':'form',
	   'view_mode':'form',
	   'target':'new',
	   'context':{'default_field_id': self.field_id,'default_sms_gateway': self.sms_gateway.id, 'default_to_number':self.to_number,'default_record_id':self.record_id,'default_model_id':self.model_id, 'default_error_message':error_message}
	   }
	   
class esms_history(models.Model):

    _name = "esms.history"
    _order = "my_date desc"
    
    record_id = fields.Integer(readonly=True, string="Record")
    account_id = fields.Many2one('esms.accounts', readonly=True, string="SMS Account")
    model_id = fields.Many2one('ir.model', readonly=True, string="Model")
    model_name = fields.Char(string="Model Name", related='model_id.model', readonly=True)
    field_id = fields.Many2one('ir.model.fields', readonly=True, string="Field")
    from_mobile = fields.Char(string="From Mobile", readonly=True)
    to_mobile = fields.Char(string="To Mobile", readonly=True)
    sms_content = fields.Text(string="SMS Message", readonly=True)
    record_name = fields.Char(string="Record Name", compute="_rec_nam")
    status_string = fields.Char(string="Response String", readonly=True)
    status_code = fields.Selection((('failed', 'Failed to Send'), ('queued', 'Queued'), ('successful', 'Sent'), ('DELIVRD', 'Delivered'), ('EXPIRED','Timed Out'), ('UNDELIV', 'Undelivered')), string='Delivary State', readonly=True)
    sms_gateway_message_id = fields.Char(string="SMS Gateway Message ID", readonly=True)
    direction = fields.Selection((("I","INBOUND"),("O","OUTBOUND")), string="Direction", readonly=True)
    my_date = fields.Datetime(string="Send/Receive Date", readonly=True, help="The date and time the sms is received or sent")
    delivary_error_string = fields.Text(string="Delivary Error")

    @api.one
    @api.depends('record_id', 'model_id')
    def _rec_nam(self):
        my_record = self.env[self.model_id.model].search([('id','=',self.record_id)])
        self.record_name = my_record.name
        

