from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from openerp.http import request
from datetime import datetime
from openerp.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class etq_results(models.Model):

    _name = "etq.result"
    
    exam_id = fields.Many2one('etq.exam', string="Exam")
    results = fields.One2many('etq.result.question', 'result_id', string="Results")
    
class etq_result_question(models.Model):

    _name = "etq.result.question"
    
    result_id = fields.Many2one('etq.result', string="Result")
    question = fields.Many2one('etq.question', string="Question")
    correct = fields.Boolean(string="Correct")