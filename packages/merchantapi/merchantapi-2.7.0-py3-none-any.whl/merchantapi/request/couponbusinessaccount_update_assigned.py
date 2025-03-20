"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request CouponBusinessAccount_Update_Assigned. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/couponbusinessaccount_update_assigned
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class CouponBusinessAccountUpdateAssigned(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, coupon: merchantapi.model.Coupon = None):
		"""
		CouponBusinessAccountUpdateAssigned Constructor.

		:param client: Client
		:param coupon: Coupon
		"""

		super().__init__(client)
		self.coupon_id = None
		self.edit_coupon = None
		self.coupon_code = None
		self.business_account_id = None
		self.edit_business_account = None
		self.business_account_title = None
		self.assigned = None
		if isinstance(coupon, merchantapi.model.Coupon):
			if coupon.get_id():
				self.set_coupon_id(coupon.get_id())
			elif coupon.get_code():
				self.set_edit_coupon(coupon.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'CouponBusinessAccount_Update_Assigned'

	def get_coupon_id(self) -> int:
		"""
		Get Coupon_ID.

		:returns: int
		"""

		return self.coupon_id

	def get_edit_coupon(self) -> str:
		"""
		Get Edit_Coupon.

		:returns: str
		"""

		return self.edit_coupon

	def get_coupon_code(self) -> str:
		"""
		Get Coupon_Code.

		:returns: str
		"""

		return self.coupon_code

	def get_business_account_id(self) -> int:
		"""
		Get BusinessAccount_ID.

		:returns: int
		"""

		return self.business_account_id

	def get_edit_business_account(self) -> str:
		"""
		Get Edit_BusinessAccount.

		:returns: str
		"""

		return self.edit_business_account

	def get_business_account_title(self) -> str:
		"""
		Get BusinessAccount_Title.

		:returns: str
		"""

		return self.business_account_title

	def get_assigned(self) -> bool:
		"""
		Get Assigned.

		:returns: bool
		"""

		return self.assigned

	def set_coupon_id(self, coupon_id: int) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set Coupon_ID.

		:param coupon_id: int
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.coupon_id = coupon_id
		return self

	def set_edit_coupon(self, edit_coupon: str) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set Edit_Coupon.

		:param edit_coupon: str
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.edit_coupon = edit_coupon
		return self

	def set_coupon_code(self, coupon_code: str) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set Coupon_Code.

		:param coupon_code: str
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.coupon_code = coupon_code
		return self

	def set_business_account_id(self, business_account_id: int) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_ID.

		:param business_account_id: int
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.business_account_id = business_account_id
		return self

	def set_edit_business_account(self, edit_business_account: str) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set Edit_BusinessAccount.

		:param edit_business_account: str
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.edit_business_account = edit_business_account
		return self

	def set_business_account_title(self, business_account_title: str) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set BusinessAccount_Title.

		:param business_account_title: str
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.business_account_title = business_account_title
		return self

	def set_assigned(self, assigned: bool) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Set Assigned.

		:param assigned: bool
		:returns: CouponBusinessAccountUpdateAssigned
		"""

		self.assigned = assigned
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.CouponBusinessAccountUpdateAssigned':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'CouponBusinessAccountUpdateAssigned':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.CouponBusinessAccountUpdateAssigned(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.coupon_id is not None:
			data['Coupon_ID'] = self.coupon_id
		elif self.edit_coupon is not None:
			data['Edit_Coupon'] = self.edit_coupon
		elif self.coupon_code is not None:
			data['Coupon_Code'] = self.coupon_code

		if self.business_account_id is not None:
			data['BusinessAccount_ID'] = self.business_account_id
		elif self.edit_business_account is not None:
			data['Edit_BusinessAccount'] = self.edit_business_account
		elif self.business_account_title is not None:
			data['BusinessAccount_Title'] = self.business_account_title

		if self.assigned is not None:
			data['Assigned'] = self.assigned
		return data
