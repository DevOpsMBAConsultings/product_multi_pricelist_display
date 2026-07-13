from odoo import models, fields, api
from lxml import etree

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _setup_fields(self):
        cls = type(self)
        try:
            self.env.cr.execute("SELECT 1 FROM pg_catalog.pg_class WHERE relname = 'product_pricelist'")
            if self.env.cr.fetchone():
                self.env.cr.execute("SELECT id, name FROM product_pricelist WHERE display_in_product_list = true")
                pricelists = self.env.cr.fetchall()
                for pricelist_id, pricelist_name in pricelists:
                    field_name = f"price_pricelist_{pricelist_id}"
                    if field_name not in cls._fields:
                        field = fields.Float(
                            string=f"Price ({pricelist_name})",
                            compute="_compute_pricelist_prices",
                            store=False,
                            readonly=True,
                        )
                        cls._add_field(field_name, field)
        except Exception:
            pass
        super()._setup_fields()

    @api.depends("list_price")
    def _compute_pricelist_prices(self):
        """Compute prices from pricelists marked to display"""
        pricelists = self.env["product.pricelist"].search(
            [("display_in_product_list", "=", True)]
        )
        for template in self:
            product = template.product_variant_id
            for pricelist in pricelists:
                field_name = f"price_pricelist_{pricelist.id}"
                if product:
                    try:
                        price = pricelist._get_product_price(product, quantity=1.0)
                        template[field_name] = price
                    except Exception:
                        template[field_name] = 0.0
                else:
                    template[field_name] = 0.0

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        if view_type in ('tree', 'list'):
            doc = etree.fromstring(arch)
            target = doc.xpath("//field[@name='list_price']") or doc.xpath("//field[@name='lst_price']") or doc.xpath("//field[@name='name']")
            if target:
                pricelists = self.env["product.pricelist"].search(
                    [("display_in_product_list", "=", True)]
                )
                for pricelist in pricelists:
                    field_name = f"price_pricelist_{pricelist.id}"
                    if not doc.xpath(f"//field[@name='{field_name}']"):
                        new_field = etree.Element('field', name=field_name, optional="show")
                        target[0].addnext(new_field)
                arch = etree.tostring(doc, encoding='unicode')
        return arch, view


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _setup_fields(self):
        cls = type(self)
        try:
            self.env.cr.execute("SELECT 1 FROM pg_catalog.pg_class WHERE relname = 'product_pricelist'")
            if self.env.cr.fetchone():
                self.env.cr.execute("SELECT id, name FROM product_pricelist WHERE display_in_product_list = true")
                pricelists = self.env.cr.fetchall()
                for pricelist_id, pricelist_name in pricelists:
                    field_name = f"price_pricelist_{pricelist_id}"
                    if field_name not in cls._fields:
                        field = fields.Float(
                            string=f"Price ({pricelist_name})",
                            compute="_compute_pricelist_prices",
                            store=False,
                            readonly=True,
                        )
                        cls._add_field(field_name, field)
        except Exception:
            pass
        super()._setup_fields()

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
                    price = pricelist._get_product_price(product, quantity=1.0)
                    product[field_name] = price
                except Exception:
                    product[field_name] = 0.0

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        if view_type in ('tree', 'list'):
            doc = etree.fromstring(arch)
            target = doc.xpath("//field[@name='list_price']") or doc.xpath("//field[@name='lst_price']") or doc.xpath("//field[@name='name']")
            if target:
                pricelists = self.env["product.pricelist"].search(
                    [("display_in_product_list", "=", True)]
                )
                for pricelist in pricelists:
                    field_name = f"price_pricelist_{pricelist.id}"
                    if not doc.xpath(f"//field[@name='{field_name}']"):
                        new_field = etree.Element('field', name=field_name, optional="show")
                        target[0].addnext(new_field)
                arch = etree.tostring(doc, encoding='unicode')
        return arch, view


