"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

BaseSubscription data model.
"""

from merchantapi.abstract import Model

class BaseSubscription(Model):
	def __init__(self, data: dict = None):
		"""
		BaseSubscription Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_order_id(self) -> int:
		"""
		Get order_id.

		:returns: int
		"""

		return self.get_field('order_id', 0)

	def get_line_id(self) -> int:
		"""
		Get line_id.

		:returns: int
		"""

		return self.get_field('line_id', 0)

	def get_customer_id(self) -> int:
		"""
		Get cust_id.

		:returns: int
		"""

		return self.get_field('cust_id', 0)

	def get_customer_payment_card_id(self) -> int:
		"""
		Get custpc_id.

		:returns: int
		"""

		return self.get_field('custpc_id', 0)

	def get_product_id(self) -> int:
		"""
		Get product_id.

		:returns: int
		"""

		return self.get_field('product_id', 0)

	def get_subscription_term_id(self) -> int:
		"""
		Get subterm_id.

		:returns: int
		"""

		return self.get_field('subterm_id', 0)

	def get_address_id(self) -> int:
		"""
		Get addr_id.

		:returns: int
		"""

		return self.get_field('addr_id', 0)

	def get_ship_id(self) -> int:
		"""
		Get ship_id.

		:returns: int
		"""

		return self.get_field('ship_id', 0)

	def get_ship_data(self) -> str:
		"""
		Get ship_data.

		:returns: string
		"""

		return self.get_field('ship_data')

	def get_quantity(self) -> int:
		"""
		Get quantity.

		:returns: int
		"""

		return self.get_field('quantity', 0)

	def get_term_remaining(self) -> int:
		"""
		Get termrem.

		:returns: int
		"""

		return self.get_field('termrem', 0)

	def get_term_processed(self) -> int:
		"""
		Get termproc.

		:returns: int
		"""

		return self.get_field('termproc', 0)

	def get_first_date(self) -> int:
		"""
		Get firstdate.

		:returns: int
		"""

		return self.get_timestamp_field('firstdate')

	def get_last_date(self) -> int:
		"""
		Get lastdate.

		:returns: int
		"""

		return self.get_timestamp_field('lastdate')

	def get_next_date(self) -> int:
		"""
		Get nextdate.

		:returns: int
		"""

		return self.get_timestamp_field('nextdate')

	def get_status(self) -> str:
		"""
		Get status.

		:returns: string
		"""

		return self.get_field('status')

	def get_message(self) -> str:
		"""
		Get message.

		:returns: string
		"""

		return self.get_field('message')

	def get_cancel_date(self) -> int:
		"""
		Get cncldate.

		:returns: int
		"""

		return self.get_timestamp_field('cncldate')

	def get_tax(self) -> float:
		"""
		Get tax.

		:returns: float
		"""

		return self.get_field('tax', 0.00)

	def get_formatted_tax(self) -> str:
		"""
		Get formatted_tax.

		:returns: string
		"""

		return self.get_field('formatted_tax')

	def get_shipping(self) -> float:
		"""
		Get shipping.

		:returns: float
		"""

		return self.get_field('shipping', 0.00)

	def get_formatted_shipping(self) -> str:
		"""
		Get formatted_shipping.

		:returns: string
		"""

		return self.get_field('formatted_shipping')

	def get_subtotal(self) -> float:
		"""
		Get subtotal.

		:returns: float
		"""

		return self.get_field('subtotal', 0.00)

	def get_formatted_subtotal(self) -> str:
		"""
		Get formatted_subtotal.

		:returns: string
		"""

		return self.get_field('formatted_subtotal')

	def get_total(self) -> float:
		"""
		Get total.

		:returns: float
		"""

		return self.get_field('total', 0.00)

	def get_formatted_total(self) -> str:
		"""
		Get formatted_total.

		:returns: string
		"""

		return self.get_field('formatted_total')

	def get_authorization_failure_count(self) -> int:
		"""
		Get authfails.

		:returns: int
		"""

		return self.get_field('authfails', 0)

	def get_last_authorization_failure(self) -> int:
		"""
		Get lastafail.

		:returns: int
		"""

		return self.get_timestamp_field('lastafail')
