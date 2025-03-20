from odoo import models, api, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inverter_ids = fields.One2many(comodel_name='photovoltaic.inverter', inverse_name='product_id')
    inverter_id = fields.Many2one(comodel_name='photovoltaic.inverter', compute='_compute_inverter', store=True)

    manufacturer = fields.Many2one(related='inverter_id.manufacturer')
    model = fields.Char(related='inverter_id.model')
    rated_power_ac = fields.Float(related='inverter_id.rated_power_ac')
    maximum_power_dc = fields.Float(related='inverter_id.maximum_power_dc')
    startup_voltage_dc = fields.Float(related='inverter_id.startup_voltage_dc')
    lower_voltage_limit_mpp = fields.Float(related='inverter_id.lower_voltage_limit_mpp')
    upper_voltage_limit_mpp = fields.Float(related='inverter_id.upper_voltage_limit_mpp')
    max_voltage_dc = fields.Float(related='inverter_id.max_voltage_dc')
    in_dc = fields.Float(related='inverter_id.in_dc')
    maximun_current_dc = fields.Float(related='inverter_id.maximun_current_dc')
    vac = fields.Float(related='inverter_id.vac')
    rated_power_ac = fields.Float(related='inverter_id.rated_power_ac')
    maximun_current_ac = fields.Float(related='inverter_id.maximun_current_ac')
    power_factor = fields.Float(related='inverter_id.power_factor')
    number_of_phases = fields.Selection(related='inverter_id.number_of_phases')
    inverter_type = fields.Selection(related='inverter_id.type')
    number_of_mppt_trackers = fields.Float(related='inverter_id.number_of_mppt_trackers')
    maximum_current_per_mppt = fields.Float(related='inverter_id.maximum_current_per_mppt')
    maximum_icc_per_mppt = fields.Float(related='inverter_id.maximum_icc_per_mppt')
    pv_inputs_per_mppt = fields.Float(related='inverter_id.pv_inputs_per_mppt')
    total_pv_inputes = fields.Float(related='inverter_id.total_pv_inputes')
    connectivity = fields.Char(related='inverter_id.connectivity')
    monitoring_portal = fields.Char(related='inverter_id.monitoring_portal')
    
    
    module_ids = fields.One2many(comodel_name='photovoltaic.module', inverse_name='product_id')
    module_id = fields.Many2one(comodel_name='photovoltaic.module', compute='_compute_module', store=True)


    manufacturer = fields.Many2one(related='module_id.manufacturer')
    model = fields.Char(related='module_id.model')
    max_voltage = fields.Float(related='module_id.max_voltage')
    max_current = fields.Float(related='module_id.max_current')
    short_circuit_current = fields.Float(related='module_id.short_circuit_current')
    power = fields.Float(related='module_id.power')
    open_circuit_voltage = fields.Float(related='module_id.open_circuit_voltage')
    temperature_coeficient = fields.Float(related='module_id.temperature_coeficient')
    tonc = fields.Float(related='module_id.tonc')
    min_temperature = fields.Float(related='module_id.min_temperature')
    max_temperature = fields.Float(related='module_id.max_temperature')
    min_ambient_temperature = fields.Float(related='module_id.min_ambient_temperature')
    max_ambient_temperature = fields.Float(related='module_id.max_ambient_temperature')
    uoc = fields.Float(related='module_id.uoc')
    umpp_min = fields.Float(related='module_id.umpp_min')
    umpp_max = fields.Float(related='module_id.umpp_max')
    maximum_system_voltage = fields.Float(related='module_id.maximum_system_voltage')
    maximum_fuse_rating = fields.Float(related='module_id.maximum_fuse_rating')

    @api.depends('module_ids')
    def _compute_module(self):
        for record in self:
            if len(record.module_ids) > 0:
                record.module_id = record.module_ids[0]
            else:
                record.module_id = None

    @api.depends('inverter_ids')
    def _compute_inverter(self):
        for record in self:
            if len(record.inverter_ids) > 0:
                record.inverter_id = record.inverter_ids[0]
            else:
                record.inverter_id = None
