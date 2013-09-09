from nose.tools import (
    assert_true, assert_false,
    assert_equals,
    assert_is_none,
    assert_raises
)
from unittest import TestCase, skip

import json

from unleashed.resources.fields import Field
from unleashed.resources import UnleashedResource


class DummyResource(UnleashedResource):
    __endpoint__ = "MyEndPoint"

    Foo = Field()
    Bar = Field()
    Baz = Field()


class UnleashedResourceTestCase(TestCase):
    def test_fields_accessible_as_attributes(self):
        r = DummyResource()

        assert_true(hasattr(r, 'Foo'))
        assert_true(hasattr(r, 'Bar'))
        assert_true(hasattr(r, 'Baz'))

        r.Foo = 42

    def test_fields_settable_as_attributes(self):
        r = DummyResource()
        r.Foo = 42
        r.Bar = -1

        assert_equals(r.Foo, 42)
        assert_equals(r.Bar, -1)

    def test_from_dict(self):
        r = DummyResource()

        dict_value = {
            'Foo': 1,
            'Bar': 2,
            'Baz': 3
        }

        r.from_dict(dict_value)

        assert_equals(r.Foo, 1)
        assert_equals(r.Bar, 2)
        assert_equals(r.Baz, 3)

    def test_to_dict(self):
        r = DummyResource()
        r.Foo = 1
        r.Bar = 2
        r.Baz = 3

        dict_val = r.to_dict()

        assert_equals(
            dict_val,
            {
                'Foo': 1,
                'Bar': 2,
                'Baz': 3
            }
        )


class ProductResourceTestCase(TestCase):

    def test_get_product(self):
        from unleashed.resources.product import Product

        p = Product()
        product_dict = json.loads(test_product_json)
        p.from_dict(product_dict)

        assert_equals(p.ProductCode, '_TEST01')
        print p.LastModifiedOn
        # assert_equals(p.ProductGroup.GroupName.value, '_Test')
        # assert_equals(p.SellPriceTier1.Name, 'RRP')
        # assert_equals(p.SellPriceTier1.Value, '15.0000')


test_product_json = """
{
    "ProductCode": "_TEST01",
    "ProductDescription": "Test Item 01",
    "Barcode": null,
    "PackSize": null,
    "Width": null,
    "Height": null,
    "Depth": null,
    "Weight": null,
    "MinStockAlertLevel": null,
    "MaxStockAlertLevel": null,
    "ReOrderPoint": null,
    "UnitOfMeasure": null,
    "NeverDiminishing": false,
    "LastCost": null,
    "DefaultPurchasePrice": 5,
    "DefaultSellPrice": 10,
    "AverageLandPrice": null,
    "Obsolete": false,
    "Notes": null,
    "SellPriceTier1": {
        "Name": "RRP",
        "Value": "15.0000"
    },
    "SellPriceTier2": {
        "Name": "",
        "Value": "0.0000"
    },
    "SellPriceTier3": {
        "Name": "Sell Price Tier 3",
        "Value": "0.0000"
    },
    "SellPriceTier4": {
        "Name": "Sell Price Tier 4",
        "Value": "0.0000"
    },
    "SellPriceTier5": {
        "Name": "Sell Price Tier 5",
        "Value": "0.0000"
    },
    "SellPriceTier6": {
        "Name": "Sell Price Tier 6",
        "Value": "0.0000"
    },
    "SellPriceTier7": {
        "Name": "Sell Price Tier 7",
        "Value": "0.0000"
    },
    "SellPriceTier8": {
        "Name": "Sell Price Tier 8",
        "Value": "0.0000"
    },
    "SellPriceTier9": {
        "Name": "Sell Price Tier 9",
        "Value": "0.0000"
    },
    "SellPriceTier10": {
        "Name": "Sell Price Tier 10",
        "Value": "0.0000"
    },
    "Taxable": false,
    "XeroTaxCode": "EXEMPTEXPENSES",
    "XeroTaxRate": 0,
    "TaxableSales": true,
    "XeroSalesTaxCode": "OUTPUT",
    "XeroSalesTaxRate": 0.1,
    "IsComponent": false,
    "IsAssembledProduct": false,
    "CanAutoAssemble": false,
    "ProductGroup": {
        "Guid": "e76c9496-1571-4ee7-bf75-334ccbf45d29",
        "GroupName": "_Test"
    },
    "XeroSalesAccount": null,
    "BinLocation": null,
    "Supplier": null,
    "SourceId": null,
    "CreatedBy": "admin@example.com",
    "SourceVariantParentId": null,
    "Guid": "76b4e5d4-ff42-4785-93c5-a69a2980752d",
    "LastModifiedOn": "/Date(1378686019420)/"
}"""