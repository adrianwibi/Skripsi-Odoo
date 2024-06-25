# -*- coding: utf-8 -*-
{
    'name': "E-Learning",

    'summary': """
        Sistem Absensi Mahasiswa""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Adrian Wibisono",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Education',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/default_groups.xml',
        'data/matkul_data.xml',
        'views/matkul_views.xml',
        'views/attendance_views.xml',
    ],  
    "qweb": [
        "static/src/xml/*.xml",
    ],
    
    'installable': True,
    'application': True,
    # only loaded in demonstration mode
    
}