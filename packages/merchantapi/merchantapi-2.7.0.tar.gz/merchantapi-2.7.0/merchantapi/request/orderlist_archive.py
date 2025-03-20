"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request OrderList_Archive. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/orderlist_archive
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class OrderListArchive(merchantapi.abstract.Request):
	def __init__(self, client: Client = None):
		"""
		OrderListArchive Constructor.

		:param client: Client
		"""

		super().__init__(client)
		self.delete_payment_data = None
		self.delete_shipping_labels = None
		self.order_ids = []

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'OrderList_Archive'

	def get_delete_payment_data(self) -> bool:
		"""
		Get Delete_Payment_Data.

		:returns: bool
		"""

		return self.delete_payment_data

	def get_delete_shipping_labels(self) -> bool:
		"""
		Get Delete_Shipping_Labels.

		:returns: bool
		"""

		return self.delete_shipping_labels

	def get_order_ids(self):
		"""
		Get Order_IDs.

		:returns: list
		"""

		return self.order_ids

	def set_delete_payment_data(self, delete_payment_data: bool) -> 'OrderListArchive':
		"""
		Set Delete_Payment_Data.

		:param delete_payment_data: bool
		:returns: OrderListArchive
		"""

		self.delete_payment_data = delete_payment_data
		return self

	def set_delete_shipping_labels(self, delete_shipping_labels: bool) -> 'OrderListArchive':
		"""
		Set Delete_Shipping_Labels.

		:param delete_shipping_labels: bool
		:returns: OrderListArchive
		"""

		self.delete_shipping_labels = delete_shipping_labels
		return self
	
	def add_order_id(self, order_id) -> 'OrderListArchive':
		"""
		Add Order_IDs.

		:param order_id: int
		:returns: {OrderListArchive}
		"""

		self.order_ids.append(order_id)
		return self

	def add_order(self, order: merchantapi.model.Order) -> 'OrderListArchive':
		"""
		Add Order model.

		:param order: Order
		:raises Exception:
		:returns: OrderListArchive
		"""
		if not isinstance(order, merchantapi.model.Order):
			raise Exception('Expected an instance of Order')

		if order.get_id():
			self.order_ids.append(order.get_id())

		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.OrderListArchive':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'OrderListArchive':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.OrderListArchive(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.delete_payment_data is not None:
			data['Delete_Payment_Data'] = self.delete_payment_data
		if self.delete_shipping_labels is not None:
			data['Delete_Shipping_Labels'] = self.delete_shipping_labels
		data['Order_IDs'] = self.order_ids
		return data
