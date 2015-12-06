from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class SkillComp(models.Model):

    _name = 'hr.skill.comp'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    skill_id = fields.Many2one('hr.skill', string="Skill")
    competence = fields.Integer(string="Competence")
    quiz_id = fields.Many2one('quiz.quiz', string="Quiz")