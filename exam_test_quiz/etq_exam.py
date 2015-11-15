from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from openerp.http import request
from datetime import datetime
from openerp.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class etq_exam(models.Model):

    _name = "etq.exam"
    
    name = fields.Char(string="Name")
    slug = fields.Char(string="Slug", compute="slug_me")
    show_correct_questions = fields.Boolean(string="Show Correct Answers?")
    questions = fields.One2many('etq.question','exam_id', string="Questions")

    @api.multi
    def view_quiz(self):
        quiz_url = request.httprequest.host_url + "exam/" + str(self.slug)
        return {
                  'type'     : 'ir.actions.act_url',
                  'target'   : 'new',
                  'url'      : quiz_url
               }        
       
    @api.depends('name')
    def slug_me(self):
        if self.name:
            s = ustr(self.name)
            uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
            slug = re.sub('[\W_]', ' ', uni).strip().lower()
            slug = re.sub('[-\s]+', '-', slug)
            
            self.slug = slug
    
class etq_question(models.Model):

    _name = "etq.question"
    
    exam_id = fields.Many2one('etq.exam',string="Exam ID")
    question = fields.Char(string="Question")
    question_options = fields.One2many('etq.question.option','question_id',string="Options")
    num_options = fields.Integer(string="Options",compute="calc_options")
    num_correct = fields.Integer(string="Correct Options",compute="calc_correct")

    @api.one
    @api.depends('question_options')
    def calc_options(self):
        self.num_options = self.question_options.search_count([('question_id','=',self.id)])
    
    @api.one
    @api.depends('question_options')
    def calc_correct(self):
        self.num_correct = self.question_options.search_count([('question_id','=',self.id), ('correct','=',True)])
    
class etq_question_options(models.Model):

    _name = "etq.question.option"
    
    question_id = fields.Many2one('etq.question',string="Question ID")
    option = fields.Char(string="Option")
    correct = fields.Boolean(string="Correct")