# -*- coding: utf-8 -*
from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from random import randint
import random
import time

class ResDating(models.Model):

    _name = "res.dating"
    
    country_id = fields.Many2one('res.country', string='Country')
    state_id = fields.Many2one('res.country.state', string="State")
    people_per_suburb = fields.Integer(string="People per suburb", default="10")
    min_age = fields.Integer(string="Min Age", default="18")
    max_age = fields.Integer(string="Max Age", default="60")

    @api.one
    def delete_fake_profiles(self):
        for fake in self.env['res.partner'].search([('fake_profile','=',True)]):
            fake.unlink()
    
    @api.one
    def create_fake_profiles(self):
        calc_min_days = 365 * self.min_age
        calc_max_days = 365 * self.max_age
                
        my_delta_young_time = datetime.utcnow() - timedelta(days=calc_min_days)
        my_delta_old_time = datetime.utcnow() - timedelta(days=calc_max_days)	        

        suburb_list = self.env['res.better.zip'].search([('country_id','=',self.country_id.id),('state_id','=',self.state_id.id)])

        male_gender_id = self.env['res.partner.gender'].search([('name','=','Male')])[0].id
        female_gender_id = self.env['res.partner.gender'].search([('name','=','Female')])[0].id
        transmale_gender_id = self.env['res.partner.gender'].search([('name','=','Transgender')])[0].id

        for suburb in suburb_list:
            for i in range(0, self.people_per_suburb):
	    
	        #random name and with it gender
                first_name = self.env['res.dating.fake.first'].browse(randint(0, 4999))
                last_name = self.env['res.dating.fake.last'].browse(randint(0, 4999))
                gender = self.env['res.partner.gender'].search([('name','=',first_name.gender)])[0].id

                #random age
	        birth_date = my_delta_old_time + timedelta(seconds=randint(0, int((my_delta_young_time - my_delta_old_time).total_seconds())))
		age = relativedelta(date.today(), birth_date).years

                #random age pref
                min_age_pref = randint(self.min_age, self.max_age)
                max_age_pref = randint(min_age_pref, self.max_age)
                
                #create the partner
                new_partner = self.env['res.partner'].create({'dating':'True', 'fake_profile':'True', 'birth_date': birth_date, 'firstname':first_name.name, 'lastname':last_name.name,'gender':gender, 'country_id':suburb.country_id.id, 'state_id':suburb.state_id.id, 'city':suburb.city,'zip':suburb.name, 'age':age,'min_age_pref':min_age_pref,'max_age_pref':max_age_pref})
                
                #random gender pref
                rand_gender_pref = randint(1, 100)
                if rand_gender_pref <= 80:
                    #80% chance of being straight
                    if first_name.gender == "Male":
                        new_partner.gender_pref = [(4, female_gender_id)]
                    elif first_name.gender == "Female":
                        new_partner.gender_pref = [(4, male_gender_id)]
                elif rand_gender_pref <= 90:
                    #10% chance of being gay
                    if first_name.gender == "Male":
                        new_partner.gender_pref = [(4, male_gender_id)]
                    elif first_name.gender == "Female":
                        new_partner.gender_pref = [(4, female_gender_id)]    
                elif rand_gender_pref <= 100:
                    #10% chance of being bi
                    new_partner.gender_pref = [(4, male_gender_id)]
                    new_partner.gender_pref = [(4, female_gender_id)]
                    
                        
        
