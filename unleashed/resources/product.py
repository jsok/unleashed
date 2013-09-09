from unleashed.resources import UnleashedResource, UnleashedResourceCollection
from unleashed.resources import fields

from unleashed.resources.product_group import ProductGroup
from unleashed.resources.sell_price_tier import SellPriceTier
from unleashed.resources.supplier import Supplier
from unleashed.resources.unit_of_measure import UnitOfMeasure


class Product(UnleashedResource):
    __endpoint__ = 'Products'

    AverageLandPrice = fields.FieldNullableDecimal()
    Barcode = fields.FieldString()
    BinLocation = fields.FieldString()
    CanAutoAssemble = fields.FieldBoolean()
    CreatedBy = fields.FieldString()
    DefaultPurchasePrice = fields.FieldNullableDecimal()
    DefaultSellPrice = fields.FieldNullableDecimal()
    Depth = fields.FieldNullableDecimal()
    Guid = fields.FieldGuid(required=True)
    Height = fields.FieldNullableDecimal()
    IsAssembledProduct = fields.FieldBoolean()
    IsComponent = fields.FieldBoolean()
    LastCost = fields.FieldNullableDecimal()
    LastModifiedOn = fields.FieldNullableDateTime()
    MaxStockAlertLevel = fields.FieldNullableDecimal()
    MinStockAlertLevel = fields.FieldNullableDecimal()
    NeverDiminishing = fields.FieldNullableBoolean()
    Notes = fields.FieldString()
    Obsolete = fields.FieldBoolean()
    PackSize = fields.FieldNullableDecimal()
    ProductCode = fields.FieldString(length=100, required=True)
    ProductDescription = fields.FieldString(length=500, required=True)
    ProductGroup = ProductGroup()
    ReOrderPoint = fields.FieldNullableDecimal()
    SellPriceTier1 = SellPriceTier()
    SellPriceTier2 = SellPriceTier()
    SellPriceTier3 = SellPriceTier()
    SellPriceTier4 = SellPriceTier()
    SellPriceTier5 = SellPriceTier()
    SellPriceTier6 = SellPriceTier()
    SellPriceTier7 = SellPriceTier()
    SellPriceTier8 = SellPriceTier()
    SellPriceTier9 = SellPriceTier()
    SellPriceTier10 = SellPriceTier()
    SourceId = fields.FieldString()
    SourceVariantParentId = fields.FieldString()
    Supplier = Supplier()
    Taxable = fields.FieldNullableBoolean()
    TaxableSales = fields.FieldNullableBoolean()
    UnitOfMeasure = UnitOfMeasure()
    Weight = fields.FieldNullableDecimal()
    Width = fields.FieldNullableDecimal()
    XeroSalesAccount = fields.FieldString(length=50)
    XeroSalesTaxCode = fields.FieldString(length=50)
    XeroSalesTaxRate = fields.FieldNullableDecimal()
    XeroTaxCode = fields.FieldString(length=50)
    XeroTaxRate = fields.FieldNullableDecimal()

    def query__by_id(self):
        query = "{endpoint}/{guid}".format(
            endpoint=Product.ENDPOINT,
            guid=self.Guid.value
        )
        return query


class ProductList(UnleashedResourceCollection):
    ENDPOINT = 'Products'
    COLLECTION_FOR = Product

    def __init__(self):
        super(ProductList, self).__init__(paginated=True)

    def set_pagesize(self, pagesize):
        self.pagesize = pagesize

    def query__list(self):
        query = "{endpoint}/1?pagesize={pagesize}".format(
            endpoint=ProductList.ENDPOINT,
            pagesize=self.pagesize
        )
        return query