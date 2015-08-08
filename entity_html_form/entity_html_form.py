from openerp import models, fields, api
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class ehtml_gen(models.Model):

    _name = "ehtml.formgen"

    name = fields.Char(string="Form Name", required=True)
    model_id = fields.Many2one('ir.model', string="Model", required=True)
    fields_ids = fields.One2many('ehtml.fieldentry', 'html_id', string="HTML Fields")
    output_html = fields.Text(string='Embed Code')
    required_fields = fields.Text(readonly=True)
    defaults_values = fields.One2many('ehtml.fielddefault', 'html_id', string="Default Values", help="Sets the value of an field before it gets inserted into the database")
    return_url = fields.Char(string="Return URL", help="The URL that the user will be redirected to after submitting the form", required=True)
    
    @api.onchange('model_id')
    @api.one
    def change_model(self):
        #delete all existing fields
        for field_entry in self.fields_ids:
            field_entry.unlink()
        
        #get all fields that are required
        model_fields = self.env['ir.model.fields'].search([('model_id','=', self.model_id.id)])
        
        self.required_fields = ""
        for model_field in model_fields:
            if (model_field.required == True):
                self.required_fields += str(model_field.field_description) + " (" + str(model_field.name) + ")\n"
        
        
    @api.one
    def generate_form(self):
        html_output = ""
        html_output += '<div id="ehtml_form">' + "\n"
        html_output += '<form method="POST" action="' + request.httprequest.host_url + 'form/myinsert">' + "\n"
        for fe in self.fields_ids:              
            html_output += '<label for="' + fe.html_name + '">' + fe.field_id.field_description
                
            if fe.field_id.required == True:
                html_output += ' *'
                
            html_output += '</label><br/>\n'
                
            if fe.html_field_type == "text":
                html_output += '<input type="text" id="' + fe.html_name + '" name="' + fe.html_name + '"'
                    
                if fe.field_id.size > 0:
                    html_output += ' maxlength="' + fe.field_id.size + '"'
                    
                if fe.field_id.required == True:
                    html_output += ' required'
                
                html_output += '/><br>\n'
                    
            if fe.html_field_type == "textarea":
                html_output += '<textarea id="' + fe.html_name + '" name="' + fe.html_name + '"'
                   
                if fe.field_id.required == True:
    	            html_output += ' required'
    	            
    	        html_output += '></textarea><br>\n'
    	        
    	    if fe.html_field_type == "number":
	        html_output += '<input type="number" id="' + fe.html_name + '" name="' + fe.html_name + '"'
		    
	        if fe.field_id.required == True:
	            html_output += ' required'        
		    	            
    	        html_output += '/><br>\n'
    	    
    	    html_output += "<br>\n"
    	html_output += '<input type="hidden" name="form_id" value="' + str(self.id) + '"/>' + "\n"
    	html_output += '<input type="submit" value="Submit Forms"/>' + "\n"
    	html_output += "</form>\n"
        html_output += "</div>"
        self.output_html = html_output
        
class ehtml_field_entry(models.Model):

    _name = "ehtml.fieldentry"

    html_id = fields.Many2one('ehtml.formgen')
    field_id = fields.Many2one('ir.model.fields', domain="['|',('ttype','=','char'),'|',('ttype','=','text'),('ttype','=','integer'),('name','!=','create_date'),('name','!=','create_uid'),('name','!=','id'),('name','!=','write_date'),('name','!=','write_uid')]", string="Form Fields")
    html_name = fields.Char(string="HTML Field Name")
    html_field_type = fields.Selection((('text','Textbox'),('textarea','Textarea'),('number','Number')), string="HTML Field Type")
    
    @api.onchange('field_id')
    def update_html_name(self):
        self.html_name = self.field_id.name
        
        if (self.field_id.ttype == "char"):
            self.html_field_type = "text"
            
        if (self.field_id.ttype == "text"):
	    self.html_field_type = "textarea"
        
        if (self.field_id.ttype == "integer"):
            self.html_field_type = "number"
        
class ehtml_field_default(models.Model):

    _name = "ehtml.fielddefault"

    html_id = fields.Many2one('ehtml.formgen')
    field_id = fields.Many2one('ir.model.fields', string="Form Fields")
    default_value = fields.Char(string="Default Value")
    
class ehtml_history(models.Model):

    _name = "ehtml.history"

    html_id = fields.Many2one('ehtml.formgen', string="HTML Form", readonly=True)
    ref_url = fields.Char(string="Reference URL", readonly=True)
    record_id = fields.Integer(string="Record ID", readonly=True)
    form_name = fields.Char(string="Form Name", related="html_id.name")
    insert_data = fields.One2many('ehtml.fieldinsert', 'html_id', string="HTML Fields", readonly=True)
    
class ehtml_field_insert(models.Model):

    _name = "ehtml.fieldinsert"

    html_id = fields.Many2one('ehtml.history')
    field_id = fields.Many2one('ir.model.fields', string="Field")
    insert_value = fields.Char(string="Insert Value")
    