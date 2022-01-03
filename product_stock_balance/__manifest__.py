# -*- coding: utf-8 -*-
{
    "name": "Stocks by Locations",
    "version": "14.0.1.0.4",
    "category": "Warehouse",
    "author": "faOtools",
    "website": "https://faotools.com/apps/14.0/stocks-by-locations-500",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "sale_stock"
    ],
    "data": [
        "security/security.xml",
        "views/views.xml",
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/product_template_view.xml",
        "views/product_product_view.xml",
        "views/sale_order.xml",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        "static/src/xml/locations_hierarchy.xml"
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {},
    "summary": "The tool to make inventory data essential and comfortable for elaboration",
    "description": """
For the full details look at static/description/index.html

* Features * 




#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "36.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=72&ticket_version=14.0&url_type_id=3",
}