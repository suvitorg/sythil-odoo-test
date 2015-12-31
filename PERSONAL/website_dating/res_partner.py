from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class ResPartnerWebsiteDating(models.Model):

    _inherit = "res.partner"

    dating = fields.Boolean(string="Dating")
    fake_profile = fields.Boolean(string="Fake Profile")
    birth_date = fields.Date(string="DOB")
    age = fields.Integer(string="Age", readonly=True)
    gender = fields.Many2one('res.partner.gender', string="Gender")
    gender_pref = fields.Many2many('res.partner.gender', string="Gender Preference")
    min_age_pref = fields.Integer(string="Min Age Preference")
    max_age_pref = fields.Integer(string="Max Age Preference")
    location_string = fields.Char(string="Location", compute="_compute_location", store=True)
    interest_list = fields.Many2many('res.partner.interests', string="Interest List")
    dating_matches = fields.Text(string="Dating Matches")
    profile_visibility = fields.Selection([('public','Public'), ('members_only','Members Only'), ('not_listed','Not Listed')], default="members_only", string="Profile Visibility", help="Public: can be viewed by anyone on the internet\nMembers Only: Can only be viewed by people who have an account\nNot Listed: Profile will only be visiable to members you have contacted")
    
    @api.one
    def find_dating_matches(self):
        domain_string = ""
        #domain_string = "["
        
        #only dating members
        domain_string += "('dating','=','True')"
        
        #within age pref age range
        domain_string += ", ('age','>=','" + str(self.min_age_pref) + "')"
        domain_string += ", ('age','<=','" + str(self.max_age_pref) + "')"
        
        #other person seeking your age group
        
        
        #gender preference
        
        
        #domain_string += "]"
        
        temp_s = ""
        for mat in self.env['res.partner'].search([('dating','=','True'), ('age','>=','29'), ('age','<=','58')]):
            temp_s += str(mat.name)
        self.dating_matches = temp_s

    @api.one
    @api.depends('country_id.name','state_id.name','city')
    def _compute_location(self):
        slocation = ""
        if self.country_id:
            slocation += self.country_id.name + ", "
            
        if self.state_id:
	    slocation += self.state_id.name + ", "
	    
	if self.city:
	    slocation += self.city + ", "
	    
	self.location_string = slocation
        
    @api.onchange('birth_date')
    @api.one
    def update_ages_onchange(self):
        if self.birth_date:
            d1 = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
            d2 = date.today()
            self.age = relativedelta(d2, d1).years
            
    @api.model
    def update_ages(self):
        for rec in self.env['res.partner'].search([]):
            if rec.birth_date:
                d1 = datetime.strptime(rec.birth_date, "%Y-%m-%d").date()
                d2 = date.today()
                rec.age = relativedelta(d2, d1).years
                
class ResPartnerWebsiteDatingGender(models.Model):

    _name = "res.partner.gender"

    name = fields.Char(string="Gender")
    
class ResPartnerInterests(models.Model):

    _name = "res.partner.interests"

    name = fields.Char(string="Name")
    interest_category_id = fields.Many2one('res.partner.interest.categories', string="Interest Category")
    
class ResPartnerInterestCategories(models.Model):

    _name = "res.partner.interest.categories"

    name = fields.Char(string="Name")
    interest_list = fields.One2many('res.partner.interests', 'interest_category_id', string="Interest List")