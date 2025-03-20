"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderDiscountTotal data model.
"""

from merchantapi.abstract import Model
from decimal import Decimal

class OrderDiscountTotal(Model):
	def __init__(self, data: dict = None):
		"""
		OrderDiscountTotal Constructor

		:param data: dict
		"""

		super().__init__(data)

		if 'total' in self: self['total'] = Decimal(self['total'])

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_price_group_id(self) -> int:
		"""
		Get pgrp_id.

		:returns: int
		"""

		return self.get_field('pgrp_id', 0)

	def get_name(self) -> str:
		"""
		Get name.

		:returns: string
		"""

		return self.get_field('name')

	def get_description(self) -> str:
		"""
		Get descrip.

		:returns: string
		"""

		return self.get_field('descrip')

	def get_total(self) -> Decimal:
		"""
		Get total.

		:returns: Decimal
		"""

		return self.get_field('total', Decimal(0.00))
