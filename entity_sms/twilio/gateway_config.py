from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime
from lxml import etree
from openerp.http import request

class sms_response():
     delivary_state = ""
     response_string = ""
     human_read_error = ""

class twilio_core(models.Model):

    _name = "esms.twilio"
    
    api_url = fields.Char(string='API URL')
    
    def send_message(self, sms_gateway_id, from_number, to_number, sms_content, my_model_name='', my_record_id=0, my_field_name=''):
        sms_account = self.env['esms.accounts'].search([('id','=',sms_gateway_id)])
        
        #format the from number before sending
        format_from = self.env.user.partner_id.mobile
        if " " in format_from: format_from.replace(" ", "")
        
        #format the to number before sending
        format_to = to_number
        if " " in format_to: format_to.replace(" ", "")
                
        #send the sms/mms        
        payload = {'From': str(from_number), 'To': str(format_to), 'Body': str(sms_content), 'StatusCallback': request.httprequest.host_url + "sms/twilio/receipt"}
        response_string = requests.post("https://api.twilio.com/2010-04-01/Accounts/" + str(sms_account.twilio_account_sid) + "/Messages", data=payload, auth=(str(sms_account.twilio_account_sid), str(sms_account.twilio_auth_token)))

        #Analyse the reponse string and determine if it sent successfully other wise return a human readable error message   
        human_read_error = ""
        root = etree.fromstring(str(response_string.text))
        my_elements_human = root.xpath('/TwilioResponse/RestException/Message')
        if len(my_elements_human) != 0:
	    human_read_error = my_elements_human[0].text
        
        #The message id is important for delivary reports also set delivary_state=successful
	sms_gateway_message_id = ""
	delivary_state = "failed"
	my_elements = root.xpath('//Sid')
	if len(my_elements) != 0:
	    sms_gateway_message_id = my_elements[0].text
            delivary_state = "successful"
        
        #only record the sent sms/mms if it was successfully sent, multi send sms records it inconsiderate
        if delivary_state == "successful":
            my_model = self.env['ir.model'].search([('model','=',my_model_name)])
	    my_field = self.env['ir.model.fields'].search([('name','=',my_field_name)])
            esms_history = self.env['esms.history'].create({'field_id':my_field[0].id, 'record_id': my_record_id,'model_id':my_model[0].id,'account_id':sms_account.id,'from_mobile':self.env.user.partner_id.mobile,'to_mobile':to_number,'sms_content':sms_content,'status_string':response_string.text, 'direction':'O','my_date':datetime.utcnow(), 'status_code':delivary_state, 'sms_gateway_message_id':sms_gateway_message_id})
        
        #send a repsonse back saying how the sending went
        my_sms_response = sms_response()
        my_sms_response.delivary_state = delivary_state
        my_sms_response.response_string = response_string.text
        my_sms_response.human_read_error = human_read_error
        return my_sms_response

class smsglobal_conf(models.Model):

    _inherit = "esms.accounts"
    
    twilio_account_sid = fields.Char(string='Account SID')
    twilio_auth_token = fields.Char(string='Auth Token')