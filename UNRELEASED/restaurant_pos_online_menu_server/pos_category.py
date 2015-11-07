from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime


class rpoms_pos_category(models.Model):

    _inherit = "pos.category"
    
    product_ids = fields.One2many('product.template', 'pos_categ_id', string='Products')
    modifier_groups = fields.One2many('rpoms.modifier.groups', 'category_id', string='Modifiers Groups')
    publish_menu = fields.Boolean(string="Online Menu")
    description = fields.Text(string="Description")
    
class rpoms_modifier_groups(models.Model):

    _name = "rpoms.modifier.groups"
    
    category_id = fields.Many2one('pos.category', string="POS Category")
    name = fields.Char(string="Name")
    select_type = fields.Selection((('single','Single'),('multi','Multi')))
    description = fields.Text(string="Description")
    modifiers = fields.One2many('rpoms.modifier.groups.modifier', 'modifier_group_id',string="Modifiers")

class rpoms_modifier_groups_modifier(models.Model):

    _name = "rpoms.modifier.groups.modifier"
    
    modifier_group_id = fields.Many2one('rpoms.modifier.groups', string="Modifier Group")
    name = fields.Char(string="Name")
    price = fields.Float(string="Price")