from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class psms_conf(models.Model):

    _name = "psms.conf"
    
    name = fields.Char(required=True, string='Gateway Name')
    username = fields.Char(required='True', string='API Username')
    password = fields.Char(required='True', string='API Password')
    from_number = fields.Char(required='True', string='From Number')

class psms_compose(models.TransientModel):

    _name = "psms.compose"
    
    record_id = fields.Integer()
    model_id = fields.Char()
    sms_gateway = fields.Many2one('psms.conf', required=True, string='Account/Number')
    to_number = fields.Char(required=True, string='To Mobile Number', readonly=True)
    sms_content = fields.Text('SMS Content')
    field_id = fields.Char('Field ID')
    
    
    @api.one
    def send_sms(self):
    
        format_number = self.to_number
        format_number = format_number.replace(" ", "")
        format_number = format_number.replace("+", "")
        
        smsglobal_url = "http://www.smsglobal.com/http-api.php?action=sendsms&user=" + self.sms_gateway.username + "&password=" + self.sms_gateway.password + "&from=" + self.sms_gateway.from_number + "&to=" + format_number + "&text=" + self.sms_content
        r = requests.get(smsglobal_url)
        
        my_model = self.env['ir.model'].search([('model','=',self.model_id)])
        my_field = self.env['ir.model.fields'].search([('name','=',self.field_id)])
        psms_history = self.env['psms.history'].create({'field_id':my_field[0].id, 'record_id': self.record_id,'model_id':my_model[0].id,'from_mobile':self.sms_gateway.from_number,'to_mobile':self.to_number,'sms_content':self.sms_content,'status_string':r.text, 'direction':'O','my_date':datetime.utcnow()})
     
class psms_history(models.Model):

    _name = "psms.history"
    
    record_id = fields.Integer(readonly=True, string="Record")
    model_id = fields.Many2one('ir.model', readonly=True, string="Model")
    model_name = fields.Char(string="Model Name", related='model_id.model')
    field_id = fields.Many2one('ir.model.fields', readonly=True, string="Field")
    from_mobile = fields.Char(string="From Mobile Number", readonly=True)
    to_mobile = fields.Char(string="To Mobile Number", readonly=True)
    sms_content = fields.Text(string="SMS Message", readonly=True)
    record_name = fields.Char(string="Record Name", compute="_rec_nam")
    status_string = fields.Char(string="Status Code", readonly=True)
    direction = fields.Selection((("I","INBOUND"),("O","OUTBOUND")), string="Direction", readonly=True)
    my_date = fields.Datetime(string="Date", readonly=True, help="The date and time the sms is received or sent")
    status_mini = fields.Char(compute="_short_status", string="Status")

    @api.one
    @api.depends('record_id', 'model_id')
    def _rec_nam(self):
        my_record = self.env[self.model_id.model].search([('id','=',self.record_id)])
        self.record_name = my_record.name
        

    @api.one
    @api.depends('status_string')
    def _short_status(self):
        self.status_mini = self.status_string.split(';', 1)[0];