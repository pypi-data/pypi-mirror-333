from odoo import models, fields, api, _


class PhotovoltaicInverter(models.Model):
    _sql_constraints = [
        ('uniq_product_id', 'unique(product_id)', _('There is an inverter already assigned to this product'))
    ] # This turns the many2one into a one2one

    _name = 'photovoltaic.inverter'
    _description = 'Photovoltaic Inverter'
    _rec_name = 'model'
    _inherit = ['mail.thread']

    manufacturer = fields.Many2one(
        comodel_name="res.partner",
        string="Manufacturer",
        tracking=True
    )

    model = fields.Char(
        string='Model'
    )

    rated_power_ac = fields.Float(
        string='Rated power AC (W)'
    )

    maximum_power_dc = fields.Float(
        string='Maximum power DC (W)'
    )

    startup_voltage_dc = fields.Float(
        string='Start-up voltage DC (V)'
    )

    lower_voltage_limit_mpp = fields.Float(
        string='Lower voltage limit MPP (V)'
    )

    upper_voltage_limit_mpp = fields.Float(
        string='Upper voltage limit MPP (V)'
    )

    max_voltage_dc = fields.Float(
        string="Max voltage DC (V)"
    )

    in_dc = fields.Float(
        string="In DC (A)"
    )

    maximun_current_dc = fields.Float(
        string="Maximum current DC (A)"
    )

    vac = fields.Float(
        string="Vac (V)"
    )

    rated_power_ac = fields.Float(
        string="Rated power AC (W)"
    )

    maximun_current_ac = fields.Float(
        string="Maximum current AC (A)"
    )

    power_factor = fields.Float(
        string="Power factor"
    )

    number_of_phases = fields.Selection(
        [('three-phase', 'Three-phase'),
        ('single-phase', 'Single-phase')],
        string='Number of phases'
    )

    type = fields.Selection(
        [
            ('central', 'Central'),
            ('Multistring', 'Multistring')
        ]
    )

    number_of_mppt_trackers = fields.Float(
        string='Number of MPPT trackers'
    )

    maximum_current_per_mppt = fields.Float(
        string='Maximum current per MPPT (A)'
    )

    maximum_icc_per_mppt = fields.Float(
        string='Maximum Icc per MPPT (A)'
    )

    pv_inputs_per_mppt = fields.Float(
        string='Number of PV inputs per MPPT'
    )

    total_pv_inputes = fields.Float(
        string='Number of total PV inputs'
    )

    connectivity = fields.Char(
        string='Connectivity/communications'
    )

    monitoring_portal = fields.Char(
        string='Monitoring portal'
    )

    product_id = fields.Many2one(
        'product.template',
        string='Producto'
    )

    inverter_tag = fields.Many2one( #Recuired computed field to allow filtering by config value in domain
        comodel_name='product.category',
        compute='_compute_inverter_tag',
        default=lambda self: self._default_inverter_tag(),
        store=False
    )

    def _compute_inverter_tag(self):
        inverter_tag = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_inverter_tag'))
        if inverter_tag > 0:
            self.inverter_tag = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_inverter_tag'))
        else:
            self.inverter_tag = False

    def _default_inverter_tag(self):
        inverter_tag = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_inverter_tag'))
        if inverter_tag > 0:
            return inverter_tag
        else:
            return False     
