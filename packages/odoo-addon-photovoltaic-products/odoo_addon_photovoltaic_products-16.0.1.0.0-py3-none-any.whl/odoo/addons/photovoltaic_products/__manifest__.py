{
    'name': 'Photovoltaic Products',
    'version': '16.0.1.0.0',
    'depends': ['product'],
    'author': 'Librecoop',
    'license': 'LGPL-3',
    'category': 'Sales',
    'description': 'Manage the creation of photovoltaic products',
    'installable': True,
    'auto_install': False,
    'application': False,
    'data': [
        'security/ir.model.access.csv',
        "views/photovoltaic_inverter.xml",
        "views/photovoltaic_module.xml",
        "views/product_template.xml",
    ],
}
