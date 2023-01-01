# -*- coding: utf-8 -*-
{
    'name': "Vendor Based Pricing",

    'summary': """
        1) Populate Purchase Order lines/products from Vendor(res.partner).
        2) Receipt Creation based on the planned date of each purchase line.""",

    'description': """
        1) Populate Purchase Order lines/products from Vendor(res.partner).
            ● Add option to add multiple products and quantities on a vendor.
            ● While selecting the vendor on purchase order, get all the selected products and
            quantity from the vendor and create a purchase order line.
            ● For unit price use the below formula,

            Price unit = Average of all the purchase order line’s unit price for a particular
            product that was purchased before from the same vendor.

        2) Receipt Creation based on the planned date of each purchase line.
            ● In the purchase line, Odoo by default have a field “scheduled date”
            ● Use this datetime field and while confirming purchase order create different receipts
            based on date(Consider only date and ignore time)
            For Example,
            ○ Let’s say there are 5 lines and all lines are having below scheduled dates
            ■ Product A - 13-05-2021
            ■ Product B - 13-05-2021
            ■ Product C - 15-05-2021
            ■ Product D - 16-05-2021
            ■ Product E - 16-05-2021
            When confirming this order, System should create 3 different receipts.
            Receipt 1:
            ■ Product A - 13-05-2021
            ■ Product B - 13-05-2021
            Receipt 2:
            ■ Product C - 15-05-2021
            Receipt 3:
            ■ Product D - 16-05-2021
            ■ Product E - 16-05-2021
    """,

    'author': "Jeetendra S",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Purchase',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'purchase', 'purchase_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/purchase.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/banner.jpg']
    'installable': True,
    'application': True,
    'auto_install': False,
}
