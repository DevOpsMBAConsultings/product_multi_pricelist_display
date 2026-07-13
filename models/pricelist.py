from odoo import models, fields


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    display_in_product_list = fields.Boolean(
        string="Display in Product List",
        default=False,
        help="If checked, this pricelist prices will be shown as columns in product list view",
    )
