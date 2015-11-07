import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class MyController(http.Controller):

    @http.route('/takeaway', type="http", auth="public", website=True)
    def takeaway(self, **kw):
        return http.request.render('restaurant_pos_online_menu_server.product_page', {'categories': request.env['pos.category'].search([('publish_menu','=',True)])})
