from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class sms_response():
     response_string = ""
     response_code = ""

class smsglobal_core(models.Model):

    _name = "esms.smsglobal"
    
    api_url = fields.Char(string='API URL')
    
    def send_sms(self, sms_gateway_id, to_number, sms_content, my_model_name, my_record_id, my_field_name):
        sms_account = self.env['esms.accounts'].search([('id','=',sms_gateway_id)])
       
        gateway_name = "SMSGLOBAL"
        format_number = to_number
        if " " in format_number: format_number.replace(" ", "")
        if "+" in format_number: format_number = format_number.replace("+", "")
        smsglobal_url = "http://www.smsglobal.com/http-api.php?action=sendsms&user=" + sms_account.smsglobal_username + "&password=" + sms_account.smsglobal_password + "&from=" + self.env.user.partner_id.mobile + "&to=" + format_number + "&text=" + sms_content
        response_string = requests.get(smsglobal_url)
        if response_string.text == "ERROR: 88":
            response_code = "INSUFFICIENT CREDIT"
        elif "ERROR: 40" in response_string.text:
            response_code = "BAD CREDENTIALS"
        elif "ERROR" in response_string.text:
            response_code = "FAILED DELIVERY"
        else:
            response_code = "SUCCESSFUL"
       
        sms_gateway_message_id = response_string.text.split('SMSGlobalMsgID:')[1]
              
        my_model = self.env['ir.model'].search([('model','=',my_model_name)])
        my_field = self.env['ir.model.fields'].search([('name','=',my_field_name)])
        if response_code == "SUCCESSFUL":
            esms_history = self.env['esms.history'].create({'field_id':my_field[0].id, 'record_id': my_record_id,'model_id':my_model[0].id,'from_mobile':self.env.user.partner_id.mobile,'to_mobile':to_number,'sms_content':sms_content,'status_string':response_string.text, 'gateway_name': gateway_name, 'direction':'O','my_date':datetime.utcnow(), 'status_code':'successful', 'sms_gateway_message_id':sms_gateway_message_id})
        
        my_sms_response = sms_response()
        my_sms_response.response_string = response_string.text
        my_sms_response.response_code = response_code
        
        return my_sms_response


class smsglobal_conf(models.Model):

    _inherit = "esms.accounts"
    
    smsglobal_username = fields.Char(string='API Username')
    smsglobal_password = fields.Char(string='API Password')