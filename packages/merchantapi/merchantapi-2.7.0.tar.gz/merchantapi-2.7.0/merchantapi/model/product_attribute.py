"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ProductAttribute data model.
"""

from merchantapi.abstract import Model
from .product_option import ProductOption
from decimal import Decimal

class ProductAttribute(Model):
	# PRODUCT_ATTRIBUTE_TYPE constants.
	PRODUCT_ATTRIBUTE_TYPE_CHECKBOX = 'checkbox'
	PRODUCT_ATTRIBUTE_TYPE_RADIO = 'radio'
	PRODUCT_ATTRIBUTE_TYPE_TEXT = 'text'
	PRODUCT_ATTRIBUTE_TYPE_SELECT = 'select'
	PRODUCT_ATTRIBUTE_TYPE_MEMO = 'memo'
	PRODUCT_ATTRIBUTE_TYPE_TEMPLATE = 'template'
	PRODUCT_ATTRIBUTE_TYPE_SWATCH_SELECT = 'swatch-select'

	def __init__(self, data: dict = None):
		"""
		ProductAttribute Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('attributes'):
			value = self.get_field('attributes')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductAttribute):
							value[i] = ProductAttribute(e)
					else:
						raise Exception('Expected list of ProductAttribute or dict')
			else:
				raise Exception('Expected list of ProductAttribute or dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, ProductOption):
							value[i] = ProductOption(e)
					else:
						raise Exception('Expected list of ProductOption or dict')
			else:
				raise Exception('Expected list of ProductOption or dict')

		if 'price' in self: self['price'] = Decimal(self['price'])
		if 'cost' in self: self['cost'] = Decimal(self['cost'])
		if 'weight' in self: self['weight'] = Decimal(self['weight'])

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_default_id(self) -> int:
		"""
		Get default_id.

		:returns: int
		"""

		return self.get_field('default_id', 0)

	def get_display_order(self) -> int:
		"""
		Get disp_order.

		:returns: int
		"""

		if self.has_field('disp_order'):
			return self.get_field('disp_order', 0)
		elif self.has_field('disporder'):
			return self.get_field('disporder', 0)

		return 0

	def get_attribute_template_id(self) -> int:
		"""
		Get attemp_id.

		:returns: int
		"""

		return self.get_field('attemp_id', 0)

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_type(self) -> str:
		"""
		Get type.

		:returns: string
		"""

		return self.get_field('type')

	def get_prompt(self) -> str:
		"""
		Get prompt.

		:returns: string
		"""

		return self.get_field('prompt')

	def get_price(self) -> Decimal:
		"""
		Get price.

		:returns: Decimal
		"""

		return self.get_field('price', Decimal(0.00))

	def get_formatted_price(self) -> str:
		"""
		Get formatted_price.

		:returns: string
		"""

		return self.get_field('formatted_price')

	def get_cost(self) -> Decimal:
		"""
		Get cost.

		:returns: Decimal
		"""

		return self.get_field('cost', Decimal(0.00))

	def get_formatted_cost(self) -> str:
		"""
		Get formatted_cost.

		:returns: string
		"""

		return self.get_field('formatted_cost')

	def get_weight(self) -> Decimal:
		"""
		Get weight.

		:returns: Decimal
		"""

		return self.get_field('weight', Decimal(0.00))

	def get_formatted_weight(self) -> str:
		"""
		Get formatted_weight.

		:returns: string
		"""

		return self.get_field('formatted_weight')

	def get_required(self) -> bool:
		"""
		Get required.

		:returns: bool
		"""

		return self.get_field('required', False)

	def get_inventory(self) -> bool:
		"""
		Get inventory.

		:returns: bool
		"""

		return self.get_field('inventory', False)

	def get_image(self) -> str:
		"""
		Get image.

		:returns: string
		"""

		return self.get_field('image')

	def get_template_attributes(self):
		"""
		Get attributes.

		:returns: List of ProductAttribute
		"""

		return self.get_field('attributes', [])

	def get_options(self):
		"""
		Get options.

		:returns: List of ProductOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'attributes' in ret and isinstance(ret['attributes'], list):
			for i, e in enumerate(ret['attributes']):
				if isinstance(e, ProductAttribute):
					ret['attributes'][i] = ret['attributes'][i].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, ProductOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret
