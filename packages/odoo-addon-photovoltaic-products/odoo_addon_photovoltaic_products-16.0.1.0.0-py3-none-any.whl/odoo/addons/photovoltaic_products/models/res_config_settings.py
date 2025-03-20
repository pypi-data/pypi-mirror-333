from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    photovoltaic_inverter_tag = fields.Many2one(
        string='Inverter category',
        comodel_name='product.category',
        ondelete='set null'
    )

    photovoltaic_module_tag = fields.Many2one(
        string='Module category',
        comodel_name='product.category',
        ondelete='set null'
    )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        params = self.env['ir.config_parameter'].sudo()
        photovoltaic_inverter_tag = params.get_param('photovoltaic_inverter_tag', default=False)
        photovoltaic_module_tag = params.get_param('photovoltaic_module_tag', default=False)
        res.update(
            photovoltaic_inverter_tag=int(photovoltaic_inverter_tag),
            photovoltaic_module_tag=int(photovoltaic_module_tag),
        )
        return res

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("photovoltaic_inverter_tag", self.photovoltaic_inverter_tag.id)
        self.env['ir.config_parameter'].sudo().set_param("photovoltaic_module_tag", self.photovoltaic_module_tag.id)
