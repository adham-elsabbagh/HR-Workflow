# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import except_orm, Warning, RedirectWarning, UserError, ValidationError
import odoo.addons.decimal_precision as dp


READONLY_STATES = {
    'approve': [('readonly', True)],
    'refuse': [('readonly', True)],
    'confirm': [('readonly', True)],
    'process': [('readonly', True)],
    'done': [('readonly', True)],
    'request': [('readonly', True)],
}


class hr_exit_reenter(models.Model):
    _name = 'hr.exit'


    @api.model
    def _get_employee(self):
        result = False
        employee_ids = self.env['hr.employee'].search([('user_id', '=', self.env.uid)])
        if employee_ids:
            result = employee_ids[0]
        return result

    @api.one
    def _get_current_user(self):
        self.current_user = False
        if (self.employee_id and self.employee_id.parent_id and self.employee_id.parent_id.user_id) and self.employee_id.parent_id.user_id.id == self.env.uid:
            self.current_user = True

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, readonly=False,
                                  states=READONLY_STATES,default=_get_employee)
    exit_date_from = fields.Date(string='Exit Date From', required=True,readonly=False, copy=False,
                                 states=READONLY_STATES, )
    exit_date_to = fields.Date(string='Exit Date To', required=False, readonly=False,copy=False,
                               states=READONLY_STATES, )
    iqama_renewal_date = fields.Date(string='Iqama renew date', required=False, readonly=False,copy=False,
                                     states=READONLY_STATES, )
    duration = fields.Integer(string="Duration", required=False,
                              states=READONLY_STATES, )
    type = fields.Selection(string="", selection=[('single', 'Single'), ('multi', 'Multi'), ], required=True,
                            states=READONLY_STATES, )
    notes = fields.Text(string="Notes", required=False,
                        states=READONLY_STATES, )
    confirmed_date = fields.Datetime(string='Confirmed Date', readonly=True, )
    approved_date = fields.Datetime(string='Approved Date', readonly=True, )
    refused_date = fields.Datetime(string='Refused Date', readonly=True, )
    process_date = fields.Datetime(string='Processing Date', readonly=True, )
    done_date = fields.Datetime(string='Processing Date', readonly=True, )
    name = fields.Char(string='Serial')
    reason = fields.Text(string="Reason", required=False,
                         states={'refuse': [('readonly', True)],'done': [('readonly', True)], })
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True, )
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True, )
    refused_by = fields.Many2one('res.users', string='Refused By', readonly=True, )
    done_by = fields.Many2one('res.users', string='Done By', readonly=True, )
    process_by = fields.Many2one('res.users', string='Process By', readonly=True, )
    current_user = fields.Boolean(string='Current User', readonly=True, compute='_get_current_user')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('request', 'Waiting for Confirm'),
        ('confirm', 'Waiting for Approval'),
        ('approve', 'Approved'),
        ('refuse', 'Refused'),
        ('process', 'Processing'),
        ('done', 'Done'),
    ],
        'Status', readonly=True, track_visibility='onchange', default='draft')




    @api.model
    def create(self, values):
        values['name'] = self.env['ir.sequence'].next_by_code('hr.exit') or 'New'
        return super(hr_exit_reenter, self).create(values)


    @api.multi
    def action_request(self):
        if not self.employee_id.parent_id: return self.action_confirm()
        return self.write({'state': 'request'})

    @api.multi
    def action_confirm(self):
        return self.write({'state': 'confirm', 'confirmed_by': self.env.uid, 'confirmed_date': fields.date.today()})

    @api.multi
    def action_approve(self):
        return self.write({'state': 'approve', 'approved_by': self.env.uid, 'approved_date': fields.date.today()})

    @api.multi
    def action_refuse(self):
        return self.write({'state': 'refuse', 'refused_by': self.env.uid, 'refused_date': fields.date.today()})

    @api.multi
    def action_process(self):
        return self.write({'state': 'process', 'process_by': self.env.uid, 'process_date': fields.date.today()})

    @api.multi
    def action_done(self):
        return self.write({'state': 'done', 'done_by': self.env.uid, 'done_date': fields.date.today()})

    @api.multi
    def unlink(self):
        if self.state not in ('draft'):
            raise Warning(_('You cannot delete an Exit which is not draft.'))
        return super(hr_exit_reenter, self).unlink()

    @api.multi
    def on_change_date_from_to(self, exit_date_from, exit_date_to):
        if (exit_date_from and exit_date_to) and exit_date_from > exit_date_to:
            raise except_orm(_('Invalid Date!'), _('The Exit Date From should be less than or equal Exit Date To'))
        return True
