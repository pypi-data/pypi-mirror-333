from odoo import models, fields, api, _
import datetime
from dateutil.relativedelta import relativedelta


class PhotovoltaicProductionRegularization(models.Model):
    _name = 'photovoltaic.production.regularization'
    _description = 'Photovoltaic Production Regularization'
    _sql_constraints = [(
        'uniq_date_plant',
        'unique(production_year, production_month, plant)',
        _('There already is a regularization for this date and plant!')
    )]

    production_year = fields.Integer()
    production_month = fields.Integer()
    production_date = fields.Char(compute='_compute_production_date', store=True, string='Production Month')

    plant = fields.Many2one('photovoltaic.power.station', ondelete='restrict')

    real_production = fields.Integer(compute='_compute_production', store=True)

    bill_1 = fields.Many2one(
        'photovoltaic.production.bill',
        compute='_compute_production',
        store=True,
        string='M+1 bill',
        ondelete='cascade'
    )
    accum_1 = fields.Integer(
        compute='_compute_production',
        store=True,
        string='Accumulated M+1',
        help='red: regularization needed\ngreen: inside the margin\nblue: small negative regularization\nyellow: large negative regularization'
    )

    bill_3 = fields.Many2one(
        'photovoltaic.production.bill',
        compute='_compute_production',
        store=True,
        string='M+3 bill',
        ondelete='cascade'
    )
    accum_3 = fields.Integer(
        compute='_compute_production',
        store=True,
        string='Accumulated M+3',
        help='red: regularization needed\ngreen: inside the margin\nblue: small negative regularization\nyellow: large negative regularization'
    )

    bill_11 = fields.Many2one(
        'photovoltaic.production.bill',
        compute='_compute_production',
        store=True,
        string='M+11 bill',
        ondelete='cascade'
    )
    accum_11 = fields.Integer(
        compute='_compute_production',
        store=True,
        string='Accumulated M+11',
        help='red: regularization needed\ngreen: inside the margin\nblue: small negative regularization\nyellow: large negative regularization'
    )

    latest_production = fields.Integer(compute='_compute_production', store=True)

    r12n_1 = fields.Selection([('red', ''), ('green', ''), ('blue', ''), ('yellow', '')], compute='_compute_r12n', store=True)
    r12n_3 = fields.Selection([('red', ''), ('green', ''), ('blue', ''), ('yellow', '')], compute='_compute_r12n', store=True)
    r12n_11 = fields.Selection([('red', ''), ('green', ''), ('blue', ''), ('yellow', '')], compute='_compute_r12n', store=True)

    r12n_status = fields.Selection([('red', ''), ('green', ''), ('blue', ''), ('yellow', '')], compute='_compute_r12n', store=True)

    reclamation = fields.Boolean(help='The regularization has already been requested')
    comments = fields.Text()

    def force_recompute(self):
        for record in self:
            self.env.add_to_compute(self._fields['real_production'], record)
            self.env.add_to_compute(self._fields['r12n_status'], record)
            # only these two because their _compute functions actually update all needed fields

        return True

    @api.depends('production_year', 'production_month')
    def _compute_production_date(self):
        for record in self:
            record.production_date = f'{record.production_year}/{record.production_month:02}'

    def _get_bill(self, record, m_type):
        bills = self.env['photovoltaic.production.bill'].search([
            ('plant', '=', record.plant.id),
            ('production_year', '=', record.production_year),
            ('production_month', '=', record.production_month),
            ('m_type', '=', str(m_type))
        ], order='bill_date')

        if not bills:
            return False

        # update which is the last production only if there is a bill
        record.latest_production = m_type

        # the first of those bills
        return bills[0]

    @api.depends('production_year', 'production_month', 'plant')
    def _compute_production(self):
        for record in self:
            # 1st of the month of the production
            date = datetime.date(
                year=record.production_year,
                month=record.production_month,
                day=1
            )

            # all productions in that month
            productions = self.env['photovoltaic.production'].search([
                ('plant', '=', record.plant.id),
                ('date', '>=', fields.Date.to_date(date)),
                ('date', '<', fields.Date.to_date(date + relativedelta(months=1))),
            ])

            record.real_production = sum([p['EAct_exp'] for p in productions.read()])

            record.bill_1 = self._get_bill(record, 1)
            record.bill_3 = self._get_bill(record, 3)
            record.bill_11 = self._get_bill(record, 11)

            record.accum_1 = record.bill_1.billed_production
            if record.latest_production >= 3:
                record.accum_3 = record.accum_1 + record.bill_3.billed_production
            if record.latest_production >= 11:
                record.accum_11 = record.accum_3 + record.bill_11.billed_production

    @api.depends('real_production', 'accum_1', 'accum_3', 'accum_11', 'latest_production')
    def _compute_r12n(self):
        for record in self:
            error_margin = record.real_production * (record.plant.billing_error_margin / 100.0)

            for m in (1, 3, 11):
                prod_m_diff = record.real_production - getattr(record, f'accum_{m}')
                if prod_m_diff > error_margin:
                    setattr(record, f'r12n_{m}', 'red')
                elif prod_m_diff >= 0:
                    setattr(record, f'r12n_{m}', 'green')
                elif prod_m_diff < -error_margin:
                    setattr(record, f'r12n_{m}', 'yellow')
                else:
                    setattr(record, f'r12n_{m}', 'blue')

            if record.latest_production in (1, 3, 11):
                record.r12n_status = getattr(record, f'r12n_{record.latest_production}')
