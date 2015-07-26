from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)

import werkzeug
import werkzeug.urls
import random

from openerp import http, SUPERUSER_ID
from openerp.http import request
from openerp.tools.translate import _
from geopy.geocoders import Nominatim

class osmer(models.Model):

    _inherit = "event.event"

    osmer_secret = fields.Char()
 
    @api.multi
    def open_map(self):
        self.ensure_one()
        rand_number = random.randint(1, 1000000)
        map_url = request.httprequest.host_url + "osmer_map?secret=" + str(rand_number)
        self.write({'osmer_secret':rand_number})
        return {
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : map_url
               }        

class MyController(http.Controller):

    @http.route('/osmer_map',type="http")
    def some_code(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        my_string = ""
        my_string += "<link rel=\"stylesheet\" href=\"http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.css\" />\n"
        my_string += "<script src=\"http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.3/leaflet.js\"></script>\n"
        my_string += "<div id=\"map\" style=\"width: 400px; height: 400px\"></div>\n"
	my_string += "<script>\n"
	my_string += "var map = L.map('map').setView([-37.82118, 144.96323], 13);\n"
	my_string += "L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {\n"
	my_string += "maxZoom: 18,\n"
	my_string += "attribution: 'Map data copyright <a href=\"http://openstreetmap.org\">OpenStreetMap</a> contributors, ' +\n"
	my_string += "'<a href=\"http://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, ' +\n"
	my_string += "'Imagery copyright <a href=\"http://mapbox.com\">Mapbox</a>',\n"
	my_string += "id: 'examples.map-i875mjb7'\n"
	my_string += "}).addTo(map);\n"

        my_events_ids = request.registry['event.event'].search(request.cr, SUPERUSER_ID, [('osmer_secret','=',values['secret'])],limit=1)
	
	if len(my_events_ids) == 0:
	    return "Map does not exist"
	my_events = request.registry['event.event'].browse(request.cr, SUPERUSER_ID, my_events_ids)
        my_events[0].osmer_secret = ""
        my_events[0].osmer_url = ""

        geolocator = Nominatim()
        for reg in my_events[0].registration_ids:
            location_string = ""
            
            if reg.partner_id.street != False:
                location_string += reg.partner_id.street
            
            if reg.partner_id.city != False:
                location_string += ", " + reg.partner_id.city
            
            if reg.partner_id.state_id.name != False:
                location_string += ", " + reg.partner_id.state_id.name
            
            if reg.partner_id.country_id.name != False:
                location_string += ", " + reg.partner_id.country_id.name
            
            try:
                location = geolocator.geocode(location_string)
                my_string += "L.marker([" + str(location.latitude) + ", " + str(location.longitude) + "]).addTo(map).bindPopup(\"<b>" + reg.partner_id.name + "</b><br>" + str(location_string) + "\").openPopup();\n"
            except:
                _logger.error("Failed to geocode")

	my_string += "</script>"
        return my_string
        
        
