"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderPart data model.
"""

from merchantapi.abstract import Model
from decimal import Decimal

class OrderPart(Model):
	def __init__(self, data: dict = None):
		"""
		OrderPart Constructor

		:param data: dict
		"""

		super().__init__(data)

		if 'price' in self: self['price'] = Decimal(self['price'])

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_sku(self) -> str:
		"""
		Get sku.

		:returns: string
		"""

		return self.get_field('sku')

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_total_quantity(self) -> int:
		"""
		Get total_quantity.

		:returns: int
		"""

		return self.get_field('total_quantity', 0)

	def get_price(self) -> Decimal:
		"""
		Get price.

		:returns: Decimal
		"""

		return self.get_field('price', Decimal(0.00))
