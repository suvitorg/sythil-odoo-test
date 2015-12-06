from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from datetime import datetime

class Skill(models.Model):
    _name = 'hr.skill'
    _parent_store = True
    _order = 'parent_left'

    name = fields.Char(string="Name", required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    parent_id = fields.Many2one('hr.skill', 'Parent', ondelete='cascade')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)
    child_ids = fields.One2many('hr.skill', 'parent_id', string="Child Skills")
    employee_ids = fields.One2many('hr.skill.comp','skill_id',string="Employees")
    calc_comp = fields.Integer(string="Combined Competence" store=True)

    @api.multi
    def name_get(self):
        res = []
        for skill in self:
            names = []
            current = skill
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((skill.id, ' / '.join(reversed(names))))
        return res
