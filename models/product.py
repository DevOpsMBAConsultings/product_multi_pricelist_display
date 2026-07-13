from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.depends("list_price")
    def _compute_pricelist_prices(self):
        """Compute prices from pricelists marked to display"""
        pricelists = self.env["product.pricelist"].search(
            [("display_in_product_list", "=", True)]
        )

        for product in self:
            for pricelist in pricelists:
                field_name = f"price_pricelist_{pricelist.id}"
                try:
                    price = pricelist.get_product_price(product, quantity=1.0)
                    product[field_name] = price
                except Exception:
                    product[field_name] = 0.0

    def _get_pricelist_fields(self):
        """Get dynamic field definitions for pricelists"""
        pricelists = self.env["product.pricelist"].search(
            [("display_in_product_list", "=", True)]
        )
        fields_dict = {}
        for pricelist in pricelists:
            field_name = f"price_pricelist_{pricelist.id}"
            fields_dict[field_name] = fields.Float(
                string=f"Price ({pricelist.name})",
                compute="_compute_pricelist_prices",
                store=False,
            )
        return fields_dict

    @api.model
    def fields_get(self, allfields=None, **kwargs):
        res = super().fields_get(allfields, **kwargs)
        pricelist_fields = self._get_pricelist_fields()
        res.update(pricelist_fields)
        return res
