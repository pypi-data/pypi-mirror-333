from odoo import models, fields, _


class PhotovoltaicModule(models.Model):
    _sql_constraints = [
        ('uniq_product_id', 'unique(product_id)', _('There is a module already assigned to this product'))
    ] # This turns the many2one into a one2one

    _name = 'photovoltaic.module'
    _description = 'Photovoltaic Module'
    _rec_name = 'model'
    _inherit = ['mail.thread']

    manufacturer = fields.Many2one(
        comodel_name="res.partner",
        string="Manufacturer",
        tracking=True
    )

    product_id = fields.Many2one(
        'product.template',
        string='Producto'
    )

    model = fields.Char(
        string='Model'
    )

    max_voltage = fields.Float(
        string='Maximum voltage (V)'
    )

    max_current = fields.Float(
        string='Maximum current (A)'
    )

    short_circuit_current = fields.Float(
        string='Short-circuit current (A)'
    )

    power = fields.Float(
        string='Power (W)'
    )

    open_circuit_voltage = fields.Float(
        string='Open-circuit voltage (V)'
    )

    temperature_coeficient = fields.Float(
        string='Temperature Coefficient [mV/ºC].'
    )

    tonc = fields.Float(
        string='TONC'
    )

    min_temperature = fields.Float(
        string='Min temperature'
    )

    max_temperature = fields.Float(
        string='Max temperature'
    )

    min_ambient_temperature = fields.Float(
        string='Min ambient temperature'
    )

    max_ambient_temperature = fields.Float(
        string='Max ambient temperature'
    )

    uoc = fields.Float(
        string='UOC (Min temp)'
    )

    umpp_min = fields.Float(
        string='UMPP (Min temp)'
    )

    umpp_max = fields.Float(
        string='UMPP (Max temp)'
    )

    maximum_system_voltage = fields.Float(
        string='Maximum system voltage '
    )

    maximum_fuse_rating = fields.Float(
        string='Maximum fuse rating'
    )

    module_tag = fields.Many2one( #Required computed field to allow filtering by config value in domain
        comodel_name='product.category',
        compute='_compute_module_tag',
        default=lambda self: self._default_module_tag(),
        store=False
    )

    def _compute_module_tag(self):
        for record in self:
            module_tag = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_module_tag'))
            if module_tag > 0:
                self.module_tag = module_tag
            else:
                self.module_tag = False

    def _default_module_tag(self):
        module_tag = int(self.env['ir.config_parameter'].sudo().get_param('photovoltaic_module_tag'))
        if module_tag > 0:
            return module_tag
        else:
            return False
