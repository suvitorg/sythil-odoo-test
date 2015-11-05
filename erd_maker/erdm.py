from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
from lxml import etree
import base64

class erdm(models.TransientModel):

    _name = "erd.maker"
    
    my_model = fields.Many2one('ir.model', required='True', string='Select Model')
    transverse_depth = fields.Integer(string="Transverse Depth", default="1")
    omit_builtin_fields = fields.Boolean(string="Omit Builtin Fields", default="True")
    output_text = fields.Html(string="Output HTML")
    output_image = fields.Binary(string="Output Image")
    current_transverse = fields.Integer(string="Current Transverse")
    table_count = 0
    table_dict = {}
 
    @api.one
    def make_erd_html(self):
        self.output_text = ""
        self.table_count = 0
        self.current_transverse = 0
        self.erd_transverse_html(self.my_model.model)
        
        for keys,values in self.table_dict.items():
            #self.output_text += str(keys)
            self.output_text += str(values)
        
        #output the table in order
        #for x in range(1, self.table_count):
        #    self.output_text += self.table_dict[str(x)]
        
    def erd_transverse_html(self, trans_model):
        self.table_count += 1
        current_table_count = self.table_count
        self.current_transverse += 1
        table_output_string = ""
        table_output_string += "<a name=\"" + str(trans_model) + "\"></a>"
        table_output_string += "<table style=\"margin:50px;width:100%;border-collapse: collapse;\">\n"
        table_output_string += "<tr><th colspan=\"3\" style=\"border: 1px solid black;padding:5px;text-align:center;\">" + trans_model + "</th></tr>\n"
        
        for field in self.env['ir.model.fields'].search([('model_id.model','=',trans_model)]):
	    if self.omit_builtin_fields == True and (field.name == "create_date" or field.name == "create_uid" or field.name == "__last_update" or field.name == "write_date" or field.name == "write_uid"):
	        continue
	    field_name = field.name
	    if (field.ttype == "many2one" or field.ttype == "one2many") and self.current_transverse <= self.transverse_depth:
	        field_name += " <a href=\"#" + str(field.relation) + "\">(" + str(field.relation) + ")</a>"
	    if field.required == True:
	        field_name += "*"
	    table_output_string += "<tr><td style=\"border: 1px solid black;padding:5px;\">" + field_name + "</td><td style=\"border: 1px solid black;padding:5px;\">" + field.ttype + "</td><td style=\"border: 1px solid black;padding:5px;\">" + field.field_description + "</td></tr>\n"
	    if (field.ttype == "many2one" or field.ttype == "one2many") and self.current_transverse <= self.transverse_depth:
	        self.erd_transverse_html(field.relation)
        self.current_transverse -= 1
        table_output_string += "</table>"
        self.table_dict[trans_model] = table_output_string
        