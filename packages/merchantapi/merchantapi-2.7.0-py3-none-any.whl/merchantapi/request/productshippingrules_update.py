"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request ProductShippingRules_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/productshippingrules_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class ProductShippingRulesUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductShippingRulesUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.edit_product = None
		self.product_code = None
		self.product_sku = None
		self.ships_in_own_packaging = None
		self.limit_shipping_methods = None
		self.width = None
		self.length = None
		self.height = None
		self.shipping_methods = []
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

		return 'ProductShippingRules_Update'

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

	def get_ships_in_own_packaging(self) -> bool:
		"""
		Get ShipsInOwnPackaging.

		:returns: bool
		"""

		return self.ships_in_own_packaging

	def get_limit_shipping_methods(self) -> bool:
		"""
		Get LimitShippingMethods.

		:returns: bool
		"""

		return self.limit_shipping_methods

	def get_width(self) -> float:
		"""
		Get Width.

		:returns: float
		"""

		return self.width

	def get_length(self) -> float:
		"""
		Get Length.

		:returns: float
		"""

		return self.length

	def get_height(self) -> float:
		"""
		Get Height.

		:returns: float
		"""

		return self.height

	def get_shipping_methods(self) -> list:
		"""
		Get ShippingMethods.

		:returns: List of ShippingRuleMethod
		"""

		return self.shipping_methods

	def set_product_id(self, product_id: int) -> 'ProductShippingRulesUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductShippingRulesUpdate
		"""

		self.product_id = product_id
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductShippingRulesUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductShippingRulesUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_product_code(self, product_code: str) -> 'ProductShippingRulesUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductShippingRulesUpdate
		"""

		self.product_code = product_code
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductShippingRulesUpdate':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductShippingRulesUpdate
		"""

		self.product_sku = product_sku
		return self

	def set_ships_in_own_packaging(self, ships_in_own_packaging: bool) -> 'ProductShippingRulesUpdate':
		"""
		Set ShipsInOwnPackaging.

		:param ships_in_own_packaging: bool
		:returns: ProductShippingRulesUpdate
		"""

		self.ships_in_own_packaging = ships_in_own_packaging
		return self

	def set_limit_shipping_methods(self, limit_shipping_methods: bool) -> 'ProductShippingRulesUpdate':
		"""
		Set LimitShippingMethods.

		:param limit_shipping_methods: bool
		:returns: ProductShippingRulesUpdate
		"""

		self.limit_shipping_methods = limit_shipping_methods
		return self

	def set_width(self, width: float) -> 'ProductShippingRulesUpdate':
		"""
		Set Width.

		:param width: float
		:returns: ProductShippingRulesUpdate
		"""

		self.width = width
		return self

	def set_length(self, length: float) -> 'ProductShippingRulesUpdate':
		"""
		Set Length.

		:param length: float
		:returns: ProductShippingRulesUpdate
		"""

		self.length = length
		return self

	def set_height(self, height: float) -> 'ProductShippingRulesUpdate':
		"""
		Set Height.

		:param height: float
		:returns: ProductShippingRulesUpdate
		"""

		self.height = height
		return self

	def set_shipping_methods(self, shipping_methods: list) -> 'ProductShippingRulesUpdate':
		"""
		Set ShippingMethods.

		:param shipping_methods: {ShippingRuleMethod[]}
		:raises Exception:
		:returns: ProductShippingRulesUpdate
		"""

		for e in shipping_methods:
			if not isinstance(e, merchantapi.model.ShippingRuleMethod):
				raise Exception("Expected instance of ShippingRuleMethod")
		self.shipping_methods = shipping_methods
		return self
	
	def add_shipping_method(self, shipping_method) -> 'ProductShippingRulesUpdate':
		"""
		Add ShippingMethods.

		:param shipping_method: ShippingRuleMethod 
		:raises Exception:
		:returns: {ProductShippingRulesUpdate}
		"""

		if isinstance(shipping_method, merchantapi.model.ShippingRuleMethod):
			self.shipping_methods.append(shipping_method)
		elif isinstance(shipping_method, dict):
			self.shipping_methods.append(merchantapi.model.ShippingRuleMethod(shipping_method))
		else:
			raise Exception('Expected instance of ShippingRuleMethod or dict')
		return self

	def add_shipping_methods(self, shipping_methods: list) -> 'ProductShippingRulesUpdate':
		"""
		Add many ShippingRuleMethod.

		:param shipping_methods: List of ShippingRuleMethod
		:raises Exception:
		:returns: ProductShippingRulesUpdate
		"""

		for e in shipping_methods:
			if not isinstance(e, merchantapi.model.ShippingRuleMethod):
				raise Exception('Expected instance of ShippingRuleMethod')
			self.shipping_methods.append(e)

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductShippingRulesUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductShippingRulesUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductShippingRulesUpdate(self, http_response, data)

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

		if self.ships_in_own_packaging is not None:
			data['ShipsInOwnPackaging'] = self.ships_in_own_packaging
		if self.limit_shipping_methods is not None:
			data['LimitShippingMethods'] = self.limit_shipping_methods
		if self.width is not None:
			data['Width'] = self.width
		if self.length is not None:
			data['Length'] = self.length
		if self.height is not None:
			data['Height'] = self.height
		if len(self.shipping_methods):
			data['ShippingMethods'] = []

			for f in self.shipping_methods:
				data['ShippingMethods'].append(f.to_dict())
		return data
