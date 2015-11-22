import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class MyController(http.Controller):

    @http.route('/takeaway', auth='public', website=True)
    def rpoms_takeaway(self):
        return http.request.render('restaurant_pos_online_menu_server.rpoms_search', {})

    @http.route('/takeaway/suburbsearch', auth='public', website=True)
    def rpoms_suburb_list(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        suburbs = http.request.env['res.better.zip'].sudo().search([('restaurant_count','>=',1), ('city','ilike',values['q'] + "%")])
        return http.request.render('restaurant_pos_online_menu_server.rpoms_suburb_list', {'suburbs':suburbs})

    @http.route('/takeaway/locations', auth='public', website=True)
    def rpoms_countries(self):
        countries = http.request.env['res.country'].sudo().search([('restaurant_count','>',0)])
        return http.request.render('restaurant_pos_online_menu_server.rpoms_countries', {'countries': countries})

    @http.route('/takeaway/locations/<country>', auth='public', website=True)
    def rpoms_states(self, country):
        states = http.request.env['res.country.state'].sudo().search([('country_id.name','=',country),('restaurant_count','>=',1)])
        return http.request.render('restaurant_pos_online_menu_server.rpoms_states', {'country': country,'states':states})


    @http.route('/takeaway/locations/<country>/<state>', auth='public', website=True)
    def rpoms_suburbs(self, country, state):
        suburbs = http.request.env['res.better.zip'].sudo().search([('country_id.name','=',country),('state_id.name','=',state), ('restaurant_count','>=',1)])
        return http.request.render('restaurant_pos_online_menu_server.rpoms_suburbs', {'country':country, 'state':state, 'suburbs': suburbs})

    @http.route('/takeaway/<country>/<state>/<suburb>', type="http", auth="public", website=True)
    def rpoms_restaurants(self, country, state, suburb):
        my_suburb = http.request.env['res.better.zip'].sudo().search([('country_id.name','=',country),('state_id.name','=',state),('city','=',suburb)])[0]
        
        #Get a list of restaurants that deliver to this suburb
        
        restaurants = http.request.env['rpoms.restaurant'].sudo().search([('delivary_suburbs', '=', my_suburb.id)])
        
        return http.request.render('restaurant_pos_online_menu_server.rpoms_restaurant_list', {'restaurants': restaurants})

    
    @http.route('/takeaway/<country>/<state>/<suburb>/<restaurant>', type="http", auth="public", website=True)
    def rpoms_restaurant_pro(self, country, state, suburb, restaurant):
        restaurant = http.request.env['rpoms.restaurant'].sudo().search([('location_id.country_id.name', '=', country), ('location_id.state_id.name', '=', state), ('location_id.city', '=', suburb), ('slug', '=', restaurant)])
        
        return http.request.render('restaurant_pos_online_menu_server.product_page', {'restaurant': restaurant})
