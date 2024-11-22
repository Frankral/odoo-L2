# -*- coding: utf-8 -*-
{
    'name': "Automatisation de la facturation",

    'summary': "Module pour automatiser la facturation à partir d'une commande",
    
    "author": "Odoo",
    "license": "LGPL-3",
    "version": "17.0.1.0",

    'depends': [
        'base', 'sale_management', 'sale', 'stock', 'purchase', 'sale_stock'
    ],

    'data': [
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml'
    ],

}

