# -*- coding: utf-8 -*-
{
    "name": "sale_order_metadata",
    "summary": """
        Add metadata to sale order""",
    "author": "Coopdevs Treball SCCL",
    "website": "",
    "category": "sale",
    "version": "16.0.0.1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "sale", "metadata"],
    # always loaded
    "data": ["security/ir.model.access.csv", "views/sale_order.xml"],
    # only loaded in demonstration mode
}
