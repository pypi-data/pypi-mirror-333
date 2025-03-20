"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Page_Delete. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/page_delete
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageDelete(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageDelete Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.page_id = None
		self.edit_page = None
		self.page_code = None
		self.branch_id = None
		self.edit_branch = None
		self.branch_name = None
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_page_id(page.get_id())
			elif page.get_code():
				self.set_edit_page(page.get_code())
			elif page.get_code():
				self.set_page_code(page.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Page_Delete'

	def get_page_id(self) -> int:
		"""
		Get Page_ID.

		:returns: int
		"""

		return self.page_id

	def get_edit_page(self) -> str:
		"""
		Get Edit_Page.

		:returns: str
		"""

		return self.edit_page

	def get_page_code(self) -> str:
		"""
		Get Page_Code.

		:returns: str
		"""

		return self.page_code

	def get_branch_id(self) -> int:
		"""
		Get Branch_ID.

		:returns: int
		"""

		return self.branch_id

	def get_edit_branch(self) -> str:
		"""
		Get Edit_Branch.

		:returns: str
		"""

		return self.edit_branch

	def get_branch_name(self) -> str:
		"""
		Get Branch_Name.

		:returns: str
		"""

		return self.branch_name

	def set_page_id(self, page_id: int) -> 'PageDelete':
		"""
		Set Page_ID.

		:param page_id: int
		:returns: PageDelete
		"""

		self.page_id = page_id
		return self

	def set_edit_page(self, edit_page: str) -> 'PageDelete':
		"""
		Set Edit_Page.

		:param edit_page: str
		:returns: PageDelete
		"""

		self.edit_page = edit_page
		return self

	def set_page_code(self, page_code: str) -> 'PageDelete':
		"""
		Set Page_Code.

		:param page_code: str
		:returns: PageDelete
		"""

		self.page_code = page_code
		return self

	def set_branch_id(self, branch_id: int) -> 'PageDelete':
		"""
		Set Branch_ID.

		:param branch_id: int
		:returns: PageDelete
		"""

		self.branch_id = branch_id
		return self

	def set_edit_branch(self, edit_branch: str) -> 'PageDelete':
		"""
		Set Edit_Branch.

		:param edit_branch: str
		:returns: PageDelete
		"""

		self.edit_branch = edit_branch
		return self

	def set_branch_name(self, branch_name: str) -> 'PageDelete':
		"""
		Set Branch_Name.

		:param branch_name: str
		:returns: PageDelete
		"""

		self.branch_name = branch_name
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageDelete':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageDelete':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageDelete(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.page_id is not None:
			data['Page_ID'] = self.page_id
		elif self.edit_page is not None:
			data['Edit_Page'] = self.edit_page
		elif self.page_code is not None:
			data['Page_Code'] = self.page_code

		if self.branch_id is not None:
			data['Branch_ID'] = self.branch_id
		elif self.edit_branch is not None:
			data['Edit_Branch'] = self.edit_branch
		elif self.branch_name is not None:
			data['Branch_Name'] = self.branch_name

		return data
