"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Product_Update. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/product_update
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
from decimal import Decimal


class ProductUpdate(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, product: merchantapi.model.Product = None):
		"""
		ProductUpdate Constructor.

		:param client: Client
		:param product: Product
		"""

		super().__init__(client)
		self.product_id = None
		self.product_code = None
		self.edit_product = None
		self.product_sku = None
		self.product_name = None
		self.product_description = None
		self.product_canonical_category_code = None
		self.product_alternate_display_page = None
		self.product_page_title = None
		self.product_thumbnail = None
		self.product_image = None
		self.product_price = None
		self.product_cost = None
		self.product_weight = None
		self.product_inventory = None
		self.product_taxable = None
		self.product_active = None
		self.custom_field_values = merchantapi.model.CustomFieldValues()
		if isinstance(product, merchantapi.model.Product):
			if product.get_id():
				self.set_product_id(product.get_id())
			elif product.get_code():
				self.set_edit_product(product.get_code())

			self.set_product_code(product.get_code())
			self.set_product_sku(product.get_sku())
			self.set_product_name(product.get_name())
			self.set_product_description(product.get_description())
			self.set_product_canonical_category_code(product.get_canonical_category_code())
			self.set_product_alternate_display_page(product.get_page_code())
			self.set_product_page_title(product.get_page_title())
			self.set_product_thumbnail(product.get_thumbnail())
			self.set_product_image(product.get_image())
			self.set_product_price(product.get_price())
			self.set_product_cost(product.get_cost())
			self.set_product_weight(product.get_weight())
			self.set_product_inventory(product.get_product_inventory())
			self.set_product_taxable(product.get_taxable())
			self.set_product_active(product.get_active())

			if product.get_custom_field_values():
				self.set_custom_field_values(product.get_custom_field_values())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Product_Update'

	def get_product_id(self) -> int:
		"""
		Get Product_ID.

		:returns: int
		"""

		return self.product_id

	def get_product_code(self) -> str:
		"""
		Get Product_Code.

		:returns: str
		"""

		return self.product_code

	def get_edit_product(self) -> str:
		"""
		Get Edit_Product.

		:returns: str
		"""

		return self.edit_product

	def get_product_sku(self) -> str:
		"""
		Get Product_SKU.

		:returns: str
		"""

		return self.product_sku

	def get_product_name(self) -> str:
		"""
		Get Product_Name.

		:returns: str
		"""

		return self.product_name

	def get_product_description(self) -> str:
		"""
		Get Product_Description.

		:returns: str
		"""

		return self.product_description

	def get_product_canonical_category_code(self) -> str:
		"""
		Get Product_Canonical_Category_Code.

		:returns: str
		"""

		return self.product_canonical_category_code

	def get_product_alternate_display_page(self) -> str:
		"""
		Get Product_Alternate_Display_Page.

		:returns: str
		"""

		return self.product_alternate_display_page

	def get_product_page_title(self) -> str:
		"""
		Get Product_Page_Title.

		:returns: str
		"""

		return self.product_page_title

	def get_product_thumbnail(self) -> str:
		"""
		Get Product_Thumbnail.

		:returns: str
		"""

		return self.product_thumbnail

	def get_product_image(self) -> str:
		"""
		Get Product_Image.

		:returns: str
		"""

		return self.product_image

	def get_product_price(self) -> Decimal:
		"""
		Get Product_Price.

		:returns: Decimal
		"""

		return self.product_price

	def get_product_cost(self) -> Decimal:
		"""
		Get Product_Cost.

		:returns: Decimal
		"""

		return self.product_cost

	def get_product_weight(self) -> Decimal:
		"""
		Get Product_Weight.

		:returns: Decimal
		"""

		return self.product_weight

	def get_product_inventory(self) -> int:
		"""
		Get Product_Inventory.

		:returns: int
		"""

		return self.product_inventory

	def get_product_taxable(self) -> bool:
		"""
		Get Product_Taxable.

		:returns: bool
		"""

		return self.product_taxable

	def get_product_active(self) -> bool:
		"""
		Get Product_Active.

		:returns: bool
		"""

		return self.product_active

	def get_custom_field_values(self) -> merchantapi.model.CustomFieldValues:
		"""
		Get CustomField_Values.

		:returns: CustomFieldValues}|None
		"""

		return self.custom_field_values

	def set_product_id(self, product_id: int) -> 'ProductUpdate':
		"""
		Set Product_ID.

		:param product_id: int
		:returns: ProductUpdate
		"""

		self.product_id = product_id
		return self

	def set_product_code(self, product_code: str) -> 'ProductUpdate':
		"""
		Set Product_Code.

		:param product_code: str
		:returns: ProductUpdate
		"""

		self.product_code = product_code
		return self

	def set_edit_product(self, edit_product: str) -> 'ProductUpdate':
		"""
		Set Edit_Product.

		:param edit_product: str
		:returns: ProductUpdate
		"""

		self.edit_product = edit_product
		return self

	def set_product_sku(self, product_sku: str) -> 'ProductUpdate':
		"""
		Set Product_SKU.

		:param product_sku: str
		:returns: ProductUpdate
		"""

		self.product_sku = product_sku
		return self

	def set_product_name(self, product_name: str) -> 'ProductUpdate':
		"""
		Set Product_Name.

		:param product_name: str
		:returns: ProductUpdate
		"""

		self.product_name = product_name
		return self

	def set_product_description(self, product_description: str) -> 'ProductUpdate':
		"""
		Set Product_Description.

		:param product_description: str
		:returns: ProductUpdate
		"""

		self.product_description = product_description
		return self

	def set_product_canonical_category_code(self, product_canonical_category_code: str) -> 'ProductUpdate':
		"""
		Set Product_Canonical_Category_Code.

		:param product_canonical_category_code: str
		:returns: ProductUpdate
		"""

		self.product_canonical_category_code = product_canonical_category_code
		return self

	def set_product_alternate_display_page(self, product_alternate_display_page: str) -> 'ProductUpdate':
		"""
		Set Product_Alternate_Display_Page.

		:param product_alternate_display_page: str
		:returns: ProductUpdate
		"""

		self.product_alternate_display_page = product_alternate_display_page
		return self

	def set_product_page_title(self, product_page_title: str) -> 'ProductUpdate':
		"""
		Set Product_Page_Title.

		:param product_page_title: str
		:returns: ProductUpdate
		"""

		self.product_page_title = product_page_title
		return self

	def set_product_thumbnail(self, product_thumbnail: str) -> 'ProductUpdate':
		"""
		Set Product_Thumbnail.

		:param product_thumbnail: str
		:returns: ProductUpdate
		"""

		self.product_thumbnail = product_thumbnail
		return self

	def set_product_image(self, product_image: str) -> 'ProductUpdate':
		"""
		Set Product_Image.

		:param product_image: str
		:returns: ProductUpdate
		"""

		self.product_image = product_image
		return self

	def set_product_price(self, product_price) -> 'ProductUpdate':
		"""
		Set Product_Price.

		:param product_price: str|float|Decimal
		:returns: ProductUpdate
		"""

		self.product_price = Decimal(product_price)
		return self

	def set_product_cost(self, product_cost) -> 'ProductUpdate':
		"""
		Set Product_Cost.

		:param product_cost: str|float|Decimal
		:returns: ProductUpdate
		"""

		self.product_cost = Decimal(product_cost)
		return self

	def set_product_weight(self, product_weight) -> 'ProductUpdate':
		"""
		Set Product_Weight.

		:param product_weight: str|float|Decimal
		:returns: ProductUpdate
		"""

		self.product_weight = Decimal(product_weight)
		return self

	def set_product_inventory(self, product_inventory: int) -> 'ProductUpdate':
		"""
		Set Product_Inventory.

		:param product_inventory: int
		:returns: ProductUpdate
		"""

		self.product_inventory = product_inventory
		return self

	def set_product_taxable(self, product_taxable: bool) -> 'ProductUpdate':
		"""
		Set Product_Taxable.

		:param product_taxable: bool
		:returns: ProductUpdate
		"""

		self.product_taxable = product_taxable
		return self

	def set_product_active(self, product_active: bool) -> 'ProductUpdate':
		"""
		Set Product_Active.

		:param product_active: bool
		:returns: ProductUpdate
		"""

		self.product_active = product_active
		return self

	def set_custom_field_values(self, custom_field_values: merchantapi.model.CustomFieldValues) -> 'ProductUpdate':
		"""
		Set CustomField_Values.

		:param custom_field_values: CustomFieldValues}|None
		:raises Exception:
		:returns: ProductUpdate
		"""

		if not isinstance(custom_field_values, merchantapi.model.CustomFieldValues):
			raise Exception("Expected instance of CustomFieldValues")
		self.custom_field_values = custom_field_values
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.ProductUpdate':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'ProductUpdate':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.ProductUpdate(self, http_response, data)

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

		if self.product_code is not None:
			data['Product_Code'] = self.product_code
		if self.product_sku is not None:
			data['Product_SKU'] = self.product_sku
		if self.product_name is not None:
			data['Product_Name'] = self.product_name
		if self.product_description is not None:
			data['Product_Description'] = self.product_description
		if self.product_canonical_category_code is not None:
			data['Product_Canonical_Category_Code'] = self.product_canonical_category_code
		if self.product_alternate_display_page is not None:
			data['Product_Alternate_Display_Page'] = self.product_alternate_display_page
		if self.product_page_title is not None:
			data['Product_Page_Title'] = self.product_page_title
		if self.product_thumbnail is not None:
			data['Product_Thumbnail'] = self.product_thumbnail
		if self.product_image is not None:
			data['Product_Image'] = self.product_image
		if self.product_price is not None:
			data['Product_Price'] = self.product_price
		if self.product_cost is not None:
			data['Product_Cost'] = self.product_cost
		if self.product_weight is not None:
			data['Product_Weight'] = self.product_weight
		if self.product_inventory is not None:
			data['Product_Inventory'] = self.product_inventory
		if self.product_taxable is not None:
			data['Product_Taxable'] = self.product_taxable
		if self.product_active is not None:
			data['Product_Active'] = self.product_active
		if self.custom_field_values is not None:
			data['CustomField_Values'] = self.custom_field_values.to_dict()
		return data
