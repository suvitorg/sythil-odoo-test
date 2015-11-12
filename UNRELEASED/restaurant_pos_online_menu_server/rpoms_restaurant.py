from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import math

class rpoms_restaurant(models.Model):

    _name = "rpoms.restaurant"
    
    name = fields.Char(string='Restaurant Name')
    location_id = fields.Many2one('res.better.zip',string="Location")
    street = fields.Char(string="Street Address")
    latitude = fields.Float(string="Latitude", readonly=True)
    longitude = fields.Float(string="Longitude", readonly=True)
    delivary_radius_kilometers = fields.Float(string="Delivary Radius(Kilometers)")
    delivary_suburbs = fields.Many2many('res.better.zip', string="Delivary Suburbs")
    
    @api.model
    def create(self, values):
        new_rec = super(rpoms_restaurant, self).create(values)
        
        if new_rec.location_id:
            #recalculate country count
            self.env['res.country'].browse(new_rec.location_id.country_id.id).restaurant_count = self.env['rpoms.restaurant'].search_count([('location_id.country_id.id','=',new_rec.location_id.country_id.id)])
    
            #recalculate state count
            self.env['res.country.state'].browse(new_rec.location_id.state_id.id).restaurant_count = self.env['rpoms.restaurant'].search_count([('location_id.state_id.id','=',new_rec.location_id.state_id.id)])

            #recalculate suburb count
            self.env['res.better.zip'].browse(new_rec.location_id.id).restaurant_count = self.env['rpoms.restaurant'].search_count([('location_id','=',new_rec.location_id.id)])
        
            geolocator = Nominatim()
            location_string = ""
            
            if new_rec.street != False:
                location_string += new_rec.street
            
            if new_rec.location_id.city != False:
                location_string += ", " + new_rec.location_id.city
            
            if new_rec.location_id.state_id.name != False:
                location_string += ", " + new_rec.location_id.state_id.name
            
            if new_rec.location_id.country_id.name != False:
                location_string += ", " + new_rec.location_id.country_id.name
            
            try:
                location = geolocator.geocode(location_string)
                new_rec.longitude = str(location.longitude)
                new_rec.latitude = str(location.latitude)
            except:
                _logger.error("Failed to geocode")
            
            mylon = float(new_rec.longitude)
            mylat = float(new_rec.latitude)
            dist = new_rec.delivary_radius_kilometers * 0.621371
            lon_min = mylon-dist/abs(math.cos(math.radians(mylat))*69);
            lon_max = mylon+dist/abs(math.cos(math.radians(mylat))*69);
            lat_min = mylat-(dist/69);
            lat_max = mylat+(dist/69);
            del_suburbs = self.env['res.better.zip'].search([('longitude','>=',lon_min), ('longitude','<=',lon_max), ('latitude','<=',lat_min), ('latitude','>=',lat_max)])
            
            for subby in del_suburbs:
                new_rec.delivary_suburbs = [(4, subby.id)]
            
        return new_rec
            