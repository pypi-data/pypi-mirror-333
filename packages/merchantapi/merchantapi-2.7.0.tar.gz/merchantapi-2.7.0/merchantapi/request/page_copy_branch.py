"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

Handles API Request Page_Copy_Branch. 
Scope: Store.
:see: https://docs.miva.com/json-api/functions/page_copy_branch
"""

import merchantapi.abstract
import merchantapi.model
import merchantapi.response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse


class PageCopyBranch(merchantapi.abstract.Request):
	def __init__(self, client: Client = None, page: merchantapi.model.Page = None):
		"""
		PageCopyBranch Constructor.

		:param client: Client
		:param page: Page
		"""

		super().__init__(client)
		self.source_page_id = None
		self.source_edit_page = None
		self.source_page_code = None
		self.destination_branch_id = None
		self.destination_edit_branch = None
		self.destination_branch_name = None
		self.copy_page_rules_id = None
		self.copy_page_rules_name = None
		self.changeset_notes = None
		if isinstance(page, merchantapi.model.Page):
			if page.get_id():
				self.set_source_page_id(page.get_id())
			elif page.get_code():
				self.set_source_edit_page(page.get_code())

	def get_function(self):
		"""
		Get the function of the request.

		:returns: str
		"""

		return 'Page_Copy_Branch'

	def get_source_page_id(self) -> int:
		"""
		Get Source_Page_ID.

		:returns: int
		"""

		return self.source_page_id

	def get_source_edit_page(self) -> str:
		"""
		Get Source_Edit_Page.

		:returns: str
		"""

		return self.source_edit_page

	def get_source_page_code(self) -> str:
		"""
		Get Source_Page_Code.

		:returns: str
		"""

		return self.source_page_code

	def get_destination_branch_id(self) -> int:
		"""
		Get destination_branch_id.

		:returns: int
		"""

		return self.destination_branch_id

	def get_destination_edit_branch(self) -> str:
		"""
		Get destination_edit_branch.

		:returns: str
		"""

		return self.destination_edit_branch

	def get_destination_branch_name(self) -> str:
		"""
		Get destination_branch_name.

		:returns: str
		"""

		return self.destination_branch_name

	def get_copy_page_rules_id(self) -> int:
		"""
		Get CopyPageRules_ID.

		:returns: int
		"""

		return self.copy_page_rules_id

	def get_copy_page_rules_name(self) -> str:
		"""
		Get CopyPageRules_Name.

		:returns: str
		"""

		return self.copy_page_rules_name

	def get_changeset_notes(self) -> str:
		"""
		Get Changeset_Notes.

		:returns: str
		"""

		return self.changeset_notes

	def set_source_page_id(self, source_page_id: int) -> 'PageCopyBranch':
		"""
		Set Source_Page_ID.

		:param source_page_id: int
		:returns: PageCopyBranch
		"""

		self.source_page_id = source_page_id
		return self

	def set_source_edit_page(self, source_edit_page: str) -> 'PageCopyBranch':
		"""
		Set Source_Edit_Page.

		:param source_edit_page: str
		:returns: PageCopyBranch
		"""

		self.source_edit_page = source_edit_page
		return self

	def set_source_page_code(self, source_page_code: str) -> 'PageCopyBranch':
		"""
		Set Source_Page_Code.

		:param source_page_code: str
		:returns: PageCopyBranch
		"""

		self.source_page_code = source_page_code
		return self

	def set_destination_branch_id(self, destination_branch_id: int) -> 'PageCopyBranch':
		"""
		Set destination_branch_id.

		:param destination_branch_id: int
		:returns: PageCopyBranch
		"""

		self.destination_branch_id = destination_branch_id
		return self

	def set_destination_edit_branch(self, destination_edit_branch: str) -> 'PageCopyBranch':
		"""
		Set destination_edit_branch.

		:param destination_edit_branch: str
		:returns: PageCopyBranch
		"""

		self.destination_edit_branch = destination_edit_branch
		return self

	def set_destination_branch_name(self, destination_branch_name: str) -> 'PageCopyBranch':
		"""
		Set destination_branch_name.

		:param destination_branch_name: str
		:returns: PageCopyBranch
		"""

		self.destination_branch_name = destination_branch_name
		return self

	def set_copy_page_rules_id(self, copy_page_rules_id: int) -> 'PageCopyBranch':
		"""
		Set CopyPageRules_ID.

		:param copy_page_rules_id: int
		:returns: PageCopyBranch
		"""

		self.copy_page_rules_id = copy_page_rules_id
		return self

	def set_copy_page_rules_name(self, copy_page_rules_name: str) -> 'PageCopyBranch':
		"""
		Set CopyPageRules_Name.

		:param copy_page_rules_name: str
		:returns: PageCopyBranch
		"""

		self.copy_page_rules_name = copy_page_rules_name
		return self

	def set_changeset_notes(self, changeset_notes: str) -> 'PageCopyBranch':
		"""
		Set Changeset_Notes.

		:param changeset_notes: str
		:returns: PageCopyBranch
		"""

		self.changeset_notes = changeset_notes
		return self

	# noinspection PyTypeChecker
	def send(self) -> 'merchantapi.response.PageCopyBranch':
		return super().send()

	def create_response(self, http_response: HttpResponse, data) -> 'PageCopyBranch':
		"""
		Create a response object from the response data

		:param http_response: requests.models.Response
		:param data:
		:returns: Response
		"""

		return merchantapi.response.PageCopyBranch(self, http_response, data)

	def to_dict(self) -> dict:
		"""
		Reduce the request to a dict

		:override:
		:returns: dict
		"""

		data = super().to_dict()

		if self.source_page_id is not None:
			data['Source_Page_ID'] = self.source_page_id
		elif self.source_edit_page is not None:
			data['Source_Edit_Page'] = self.source_edit_page
		elif self.source_page_code is not None:
			data['Source_Page_Code'] = self.source_page_code

		if self.destination_branch_id is not None:
			data['Dest_Branch_ID'] = self.destination_branch_id
		elif self.destination_edit_branch is not None:
			data['Dest_Edit_Branch'] = self.destination_edit_branch
		elif self.destination_branch_name is not None:
			data['Dest_Branch_Name'] = self.destination_branch_name

		if self.copy_page_rules_id is not None:
			data['CopyPageRules_ID'] = self.copy_page_rules_id
		elif self.copy_page_rules_name is not None:
			data['CopyPageRules_Name'] = self.copy_page_rules_name

		if self.changeset_notes is not None:
			data['Changeset_Notes'] = self.changeset_notes
		return data
