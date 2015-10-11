from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime
from openerp.http import request
from openerp.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class website_support_help_groups(models.Model):

    _name = "website.support.help.groups"
    
    name = fields.Char(string="Help Group")
    page_ids = fields.One2many('website.support.help.page','group_id',string="Pages")
    page_count = fields.Integer(string="Number of Pages", computed='_page_count')
    
    @api.one
    @api.depends('page_ids')
    def _page_count(self):
        self.page_count = self.env['website.support.help.page'].search_count([('group_id','=',self.id)])
    
class website_support_help_page(models.Model):

    _name = "website.support.help.page"
    _order = "name asc"
    
    name = fields.Char(string='Page Name')
    url = fields.Char(string="Page URL")
    group_id = fields.Many2one('website.support.help.groups')
    
    @api.one
    @api.onchange('name')
    def _page_url(self):
        self.url = request.httprequest.host_url + 'support/help/' + slugify(self.name)

def slugify(s, max_length=None):
    """ Transform a string to a slug that can be used in a url path.

    This method will first try to do the job with python-slugify if present.
    Otherwise it will process string by stripping leading and ending spaces,
    converting unicode chars to ascii, lowering all chars and replacing spaces
    and underscore with hyphen "-".

    :param s: str
    :param max_length: int
    :rtype: str
    """
    s = ustr(s)
    uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub('[\W_]', ' ', uni).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)

    return slug[:max_length]
