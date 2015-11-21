import openerp.http as http
from openerp.http import request, SUPERUSER_ID
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)
import werkzeug
import json

class MyController(http.Controller):

    @http.route('/support/help', type="http", auth="public", website=True)
    def support_help(self, **kw):
        return http.request.render('website_support.support_help_pages', {'help_groups': http.request.env['website.support.help.groups'].sudo().search([])})
        
    @http.route('/support/ticket/submit', type="http", auth="public", website=True)
    def support_submit_ticket(self, **kw):
        return http.request.render('website_support.support_submit_ticket', {'categories': http.request.env['website.support.ticket.categories'].sudo().search([]), 'person_name': http.request.env.user.name, 'email': http.request.env.user.email})


    @http.route('/support/ticket/process', type="http", auth="user", website=True)
    def support_process_ticket(self, **kwargs):
        
        values = {}
	for field_name, field_value in kwargs.items():
            values[field_name] = field_value
        
        if http.request.env.user.id:
            new_ticket_id = request.env['website.support.ticket'].create({'person_name':values['person_name'],'category':values['category'], 'email':values['email'], 'description':values['description'], 'subject':values['subject'], 'partner_id':http.request.env.user.partner_id.id})
            #Send a message to all followers of this partner that they have sent a new ticket
            #http.request.env['res.partner'].browse(http.request.env.user.partner_id.id).message_post(body="Customer " + http.request.env.user.partner_id.name + " has sent in a new support ticket", subject="New Support Ticket")
        else:
            new_ticket_id = request.env['website.support.ticket'].create({'person_name':values['person_name'],'category':values['category'], 'email':values['email'], 'description':values['description'], 'subject':values['subject']})
        
        return werkzeug.utils.redirect("/support/ticket/thanks")
        
        
    @http.route('/support/ticket/thanks', type="http", auth="public", website=True)
    def support_ticket_thanks(self, **kw):
        return http.request.render('website_support.support_thank_you', {})

    @http.route('/support/ticket/view', type="http", auth="user", website=True)
    def support_ticket_view_list(self, **kw):
        #Only show tickets from this user
        support_tickets = http.request.env['website.support.ticket'].search([('partner_id','=',http.request.env.user.partner_id.id)])
        return http.request.render('website_support.support_ticket_view_list', {'support_tickets':support_tickets,'ticket_count':len(support_tickets)})

    @http.route('/support/ticket/view/<ticket>', type="http", auth="user", website=True)
    def support_ticket_view(self, ticket):
        #only let the user this ticket is assigned to view this ticket
        support_ticket = http.request.env['website.support.ticket'].search([('partner_id','=',http.request.env.user.partner_id.id), ('id','=',ticket) ])[0]        
        return http.request.render('website_support.support_ticket_view', {'support_ticket':support_ticket})

    @http.route('/support/ticket/comment',type="http", auth="user")
    def support_ticket_comment(self, **kw):

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        
        ticket = http.request.env['website.support.ticket'].search([('id','=',values['ticket_id'])])
        
        #check if this user owns this ticket
        if ticket.partner_id.id != http.request.env.user.partner_id.id:
            return "You do not have permission to submit this commment"
        else:
            http.request.env['website.support.ticket.message'].create({'ticket_id':ticket.id,'content':values['comment']})
        
        return werkzeug.utils.redirect("/support/ticket/view/" + str(ticket.id))
        

    @http.route('/support/help/auto-complete',type="http", auth="user")
    def support_help_autocomplete(self, **kw):

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value
        
        return_string = ""
        
        my_return = []
        
        help_pages = request.env['website.support.help.page'].search([('name','=ilike',"%" + values['term'] + "%")],limit=5)
        
        for help_page in help_pages:
            return_item = {"label": help_page.name,"value": help_page.url}
            my_return.append(return_item) 
        
        return json.JSONEncoder().encode(my_return)
