import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class MyController(http.Controller):

    @http.route('/takeaway', auth='public', website=True)
    def rpoms_takeaway(self):
        return "type in suburb"

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
        return http.request.render('restaurant_pos_online_menu_server.product_page', {'categories': http.request.env['pos.category'].sudo().search([('publish_menu','=',True)])})

    @http.route('/takeaway/<country>/<state>/<suburb>/<restaurant>', type="http", auth="public", website=True)
    def rpoms_restaurant_info(self, country, state, suburb, restaurant):
        return restaurant

