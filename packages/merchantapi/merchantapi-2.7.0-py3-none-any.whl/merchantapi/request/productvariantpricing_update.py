"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductVariantPricing_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productvariantpricing_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
from decimal import Decimal


class ProductVariantPricingUpdate(merchantapi.abstract.Request):
	# VARIANT_PRICING_METHOD constants.
	VARIANT_PRICING_METHOD_MASTER = 'master'
	VARIANT_PRICING_METHOD_SPECIFIC = 'specific'
	VARIANT_PRICING_METHOD_SUM = 'sum'

	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductVariantPricingUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_sku = None
		self.variant_id = None
		self.method = None
		self.price = None
		self.cost = None
		self.weight = None
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())
			elif product.get_sku():
				self.set_product_sku(product.get_sku())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'ProductVariantPricing_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_variant_id(self) -> int:
		"""
		Get Variant_ID.

		:returns: int
		"""

		return self.variant_id

	def get_method(self) -> str:
		"""
		Get Method.

		:returns: str
		"""

		return self.method

	def get_price(self) -> Decimal:
		"""
		Get Price.

		:returns: Decimal
		"""

		return self.price

	def get_cost(self) -> Decimal:
		"""
		Get Cost.

		:returns: Decimal
		"""

		return self.cost

	def get_weight(self) -> Decimal:
		"""
		Get Weight.

		:returns: Decimal
		"""

		return self.weight

	def set_product_id(self, product_id: int) -> 'ProductVariantPricingUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductVariantPricingUpdate
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductVariantPricingUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductVariantPricingUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'ProductVariantPricingUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductVariantPricingUpdate
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductVariantPricingUpdate':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductVariantPricingUpdate
		"""

		self.product_sku = product_sku
		return self

	def set_variant_id(self, variant_id: int) -> 'ProductVariantPricingUpdate':
		"""
		Set Variant_ID.

		:param variant_id: int
		:returns: ProductVariantPricingUpdate
		"""

		self.variant_id = variant_id
		return self

	def set_method(self, method: str) -> 'ProductVariantPricingUpdate':
		"""
		Set Method.

		:param method: str
		:returns: ProductVariantPricingUpdate
		"""

		self.method = method
		return self

	def set_price(self, price) -> 'ProductVariantPricingUpdate':
		"""
		Set Price.

		:param price: str|float|Decimal
		:returns: ProductVariantPricingUpdate
		"""

		self.price = Decimal(price)
		return self

	def set_cost(self, cost) -> 'ProductVariantPricingUpdate':
		"""
		Set Cost.

		:param cost: str|float|Decimal
		:returns: ProductVariantPricingUpdate
		"""

		self.cost = Decimal(cost)
		return self

	def set_weight(self, weight) -> 'ProductVariantPricingUpdate':
		"""
		Set Weight.

		:param weight: str|float|Decimal
		:returns: ProductVariantPricingUpdate
		"""

		self.weight = Decimal(weight)
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductVariantPricingUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductVariantPricingUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductVariantPricingUpdate(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.product_id is not None:
			data['Product_ID'] = self.product_id
		elif self.edit_product is not None:
			data['Edit_Product'] = self.edit_product
		elif self.product_code is not None:
			data['Product_Code'] = self.product_code
		elif self.product_sku is not None:
			data['Product_SKU'] = self.product_sku

		data['Variant_ID'] = self.variant_id
		data['Method'] = self.method
		if self.price is not None:
			data['Price'] = self.price
		if self.cost is not None:
			data['Cost'] = self.cost
		if self.weight is not None:
			data['Weight'] = self.weight
		return data
