from odoo import models, fields, api, _


class PhotovoltaicProductionBill(models.Model):
    _name = 'photovoltaic.production.bill'
    _description = 'Photovoltaic Production Bill'
    _sql_constraints = [(
        'uniq_bill_number',
        'unique(bill_number, m_type)',
        _('There already is a bill with this bill number and M type!')
    )]

    bill_date = fields.Date()

    production_year = fields.Integer()
    production_month = fields.Integer()
    production_date = fields.Char(compute='_compute_production_date', store=True, string='Production Month')

    plant = fields.Many2one('photovoltaic.power.station', ondelete='restrict')

    billed_production = fields.Integer()
    price = fields.Float()

    m_type = fields.Selection([
        ('1', 'M+1'),
        ('3', 'M+3'),
        ('11', 'M+11'),
    ])
    bill_number = fields.Char(name='Número de la factura')
    name = fields.Char(related='bill_number')

    @api.depends('production_year', 'production_month')
    def _compute_production_date(self):
        for record in self:
            record.production_date = f'{record.production_year}/{record.production_month:02}'
