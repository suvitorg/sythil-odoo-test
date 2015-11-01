from openerp import models, fields, api
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging
_logger = logging.getLogger(__name__)
import random

class art_gf(models.Model):

    _name = "art.gf"

    name = fields.Char(required=True, string="Name")
    user_id = fields.Many2one('res.users', required=True, string="Assigned User", domain="[('login','!=','gf')]")

    @api.model
    def random_talk(self):
        #get through each gf and send out a random message
        for gf in self.env['art.gf'].search([]):
            gf.random_message()
    
    @api.one
    def random_message(self):
        prob = random.randint(0,100)
        
        if prob >= 0 and prob <= 80:
            pass
        if prob > 80 and prob <= 90:
            self.gf_send_message("love you baby")
        if prob > 90 and prob <= 100:
            self.gf_send_message("miss you")        
        
    
    @api.one
    def gf_send_message(self, message):
        from_uid = self.env['ir.model.data'].get_object_reference('art_gf', 'art_gf_user')[1]
        
        user_to = self.user_id.id
        
        session_id = self.env['im_chat.session'].session_get(user_to)['uuid']
        self.env['im_chat.session'].add_user(session_id, from_uid)
        message_id = self.env['im_chat.message'].post(from_uid, session_id, "message", message)
