import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)

class MyController(http.Controller):

    @http.route('/sms/twilio/receipt', type="http", auth="public")
    def sms_twilio_receipt(self, **kwargs):
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        #map the POSTed delivary code to the esms delivary states 
        delivary_state = ""
        if values['MessageStatus'] == "failed":
            delivary_state = "failed"
        elif values['MessageStatus'] == "sent":
	    delivary_state = "successful"
        elif values['MessageStatus'] == "delivered":
            delivary_state = "DELIVRD"
        elif values['MessageStatus'] == "undelivered":
	    delivary_state = "UNDELIV"
        
        #fetch the sms which has the POSTed Sid AND is a twilio sms
        attach_obj = request.registry['esms.history']
	rs = attach_obj.search(request.cr, SUPERUSER_ID, [('sms_gateway_message_id','=',values['MessageSid']), ('account_id.account_gateway.gateway_model_name','=','esms.twilio')], limit=1)
	sms_message = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        
        #update the sms
        sms_message.status_code = delivary_state
        sms_message.delivary_error_string = values['ErrorCode']
        
        return "OK"