from odoo import models, fields, api
from lxml import etree


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _temp_get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == 'list':
            arch_el = etree.fromstring(res['arch'])
            target = arch_el.xpath("//field[@name='list_price']") or arch_el.xpath("//field[@name='lst_price']") or arch_el.xpath("//field[@name='name']")
            if target:
                pricelists = self.env["product.pricelist"].search(
                    [("display_in_product_list", "=", True)]
                )
                for pricelist in pricelists:
                    field_name = f"price_pricelist_{pricelist.id}"
                    if not arch_el.xpath(f"//field[@name='{field_name}']"):
                        new_field = etree.Element('field', name=field_name, optional="show")
                        target[0].addnext(new_field)
                        
                        # Add field definition to the view metadata
                        if 'models' in res and self._name in res['models'] and field_name not in res['models'][self._name]:
                            res['models'][self._name][field_name] = {
                                'type': 'float',
                                'string': f"Price ({pricelist.name})",
                                'readonly': True,
                                'sortable': False,
                                'searchable': False,
                                'store': False,
                            }
                res['arch'] = etree.tostring(arch_el, encoding='unicode')
        return res

    def read(self, fields=None, load='_classic_read'):
        if fields:
            pricelist_fields = [f for f in fields if f.startswith('price_pricelist_')]
            standard_fields = [f for f in fields if not f.startswith('price_pricelist_')]
            
            res = super().read(standard_fields, load=load)
            
            if pricelist_fields:
                pricelist_ids = [int(f.replace('price_pricelist_', '')) for f in pricelist_fields]
                pricelists = self.env['product.pricelist'].browse(pricelist_ids)
                pricelist_map = {p.id: p for p in pricelists}
                
                for record_dict in res:
                    record = self.browse(record_dict['id'])
                    product = record.product_variant_id
                    for f in pricelist_fields:
                        p_id = int(f.replace('price_pricelist_', ''))
                        pricelist = pricelist_map.get(p_id)
                        if pricelist and product:
                            try:
                                record_dict[f] = pricelist._get_product_price(product, quantity=1.0)
                            except Exception:
                                record_dict[f] = 0.0
                        else:
                            record_dict[f] = 0.0
            return res
        return super().read(fields, load=load)


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def _temp_get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == 'list':
            arch_el = etree.fromstring(res['arch'])
            target = arch_el.xpath("//field[@name='list_price']") or arch_el.xpath("//field[@name='lst_price']") or arch_el.xpath("//field[@name='name']")
            if target:
                pricelists = self.env["product.pricelist"].search(
                    [("display_in_product_list", "=", True)]
                )
                for pricelist in pricelists:
                    field_name = f"price_pricelist_{pricelist.id}"
                    if not arch_el.xpath(f"//field[@name='{field_name}']"):
                        new_field = etree.Element('field', name=field_name, optional="show")
                        target[0].addnext(new_field)
                        
                        # Add field definition to the view metadata
                        if 'models' in res and self._name in res['models'] and field_name not in res['models'][self._name]:
                            res['models'][self._name][field_name] = {
                                'type': 'float',
                                'string': f"Price ({pricelist.name})",
                                'readonly': True,
                                'sortable': False,
                                'searchable': False,
                                'store': False,
                            }
                res['arch'] = etree.tostring(arch_el, encoding='unicode')
        return res

    def read(self, fields=None, load='_classic_read'):
        if fields:
            pricelist_fields = [f for f in fields if f.startswith('price_pricelist_')]
            standard_fields = [f for f in fields if not f.startswith('price_pricelist_')]
            
            res = super().read(standard_fields, load=load)
            
            if pricelist_fields:
                pricelist_ids = [int(f.replace('price_pricelist_', '')) for f in pricelist_fields]
                pricelists = self.env['product.pricelist'].browse(pricelist_ids)
                pricelist_map = {p.id: p for p in pricelists}
                
                for record_dict in res:
                    product = self.browse(record_dict['id'])
                    for f in pricelist_fields:
                        p_id = int(f.replace('price_pricelist_', ''))
                        pricelist = pricelist_map.get(p_id)
                        if pricelist and product:
                            try:
                                record_dict[f] = pricelist._get_product_price(product, quantity=1.0)
                            except Exception:
                                record_dict[f] = 0.0
                        else:
                            record_dict[f] = 0.0
            return res
        return super().read(fields, load=load)
