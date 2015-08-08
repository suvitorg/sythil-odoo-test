import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)
import werkzeug

class MyController(http.Controller):

    @http.route('/form/myinsert',type="http", auth="public")
    def my_insert(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        
        history_obj = request.registry['ehtml.history']
        attach_obj = request.registry['ehtml.formgen']
	rs = attach_obj.search(request.cr, SUPERUSER_ID, [('id','=',values['form_id'])],limit=1)
	rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        
        #the referral string is what the campaign looks for
        secure_values = {}
        history_values = {}
        
        ref_url = request.httprequest.headers['Referer']
        new_history_id = history_obj.create(request.cr, SUPERUSER_ID, {'ref_url':ref_url, 'html_id': values['form_id']})
        new_history = history_obj.browse(request.cr, SUPERUSER_ID, new_history_id)
        
        #populate an array which has ONLY the fields that are in the form (prevent injection)
        for fi in rl[0].fields_ids:
            secure_values[fi.field_id.name] = values[fi.html_name]
            new_history[0].insert_data.create({'html_id': new_history_id, 'field_id':fi.field_id.id, 'insert_value':values[fi.html_name]})

        #default values
        for df in rl[0].defaults_values:
            secure_values[df.field_id.name] = df.default_value
            new_history[0].insert_data.create({'html_id': new_history_id, 'field_id':df.field_id.id, 'insert_value':df.default_value})
        
        new_entity_id = request.registry[rl[0].model_id.model].create(request.cr, SUPERUSER_ID, secure_values)
        new_history[0].record_id = new_entity_id
        
        return werkzeug.utils.redirect(rl[0].return_url)
    
    @http.route('/form/myinsertjson',type="http")
    def some_json(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
            
        attach_obj = request.registry['html.formgen']
	rs = attach_obj.search(request.cr, SUPERUSER_ID, [('id','=',values['form_id'])],limit=1)
	rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        
        #the referral string is what the campaign looks for
        secure_values = {}
        secure_values['name'] = 'Web Lead'
        secure_values['referred'] = request.httprequest.headers['Referer']
        
        #populate an array which has ONLY the fields that are in the form (prevent injection)
        for fi in rl[0].fields_ids:
            secure_values[fi.name] = values[fi.name]
        
        new_lead_id = request.registry['crm.lead'].create(request.cr, SUPERUSER_ID, secure_values)
        
        request.cr.execute('INSERT INTO crm_lead_category_rel VALUES(' + str(new_lead_id) + ',' + str(rl[0].tag_id.id) + ')')
        
        return_string = values['callback'] + "({'mytext':'success'});"
        
        return return_string
        
    @http.route('/form/autocomplete',type="http")
    def some_autocomplete(self, **kwargs):
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        _logger.error(values['q'])
        _logger.error(values['f'])
        
        return_string = ""
        attach_obj = request.registry['res.country']
        rs = attach_obj.search(request.cr, SUPERUSER_ID, [('name','=ilike',values['q'] + "%")],limit=5)
        rl = attach_obj.browse(request.cr, SUPERUSER_ID, rs)
        for ri in rl:
            return_string += "{'label':'" +  ri.name  + "'},"
        return_string = return_string[:-1]
        
        return_string = values['callback'] + "(" + return_string + ");"
        _logger.error(return_string)
        return return_string