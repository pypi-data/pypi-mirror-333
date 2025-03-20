"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

API Response for Branch_Create.

:see: https://docs.miva.com/json-api/functions/branch_create
"""

from merchantapi.abstract import Request, Response
from merchantapi.client import BaseClient as Client
from requests.models import Response as HttpResponse
import merchantapi.model

class BranchCreate(Response):
	def __init__(self, request: Request, http_response: HttpResponse, data: dict):
		"""
		BranchCreate Constructor.

		:param request: Request
		:param http_response: requests.models.Response
		:param data: dict
		"""

		super().__init__(request, http_response, data)
		if not self.is_success():
			return

		if 'data' in self.data:
			self.data['data'] = merchantapi.model.Branch(self.data['data'])

	def get_completed(self):
		"""
		Get completed.

		:returns: bool
		"""

		if 'completed' in self.data:
			return self.data['completed']
		return False

	def get_branch_create_session_id(self):
		"""
		Get branch_create_session_id.

		:returns: string
		"""

		if 'branch_create_session_id' in self.data:
			return self.data['branch_create_session_id']
		return None

	def get_branch(self) -> merchantapi.model.Branch:
		"""
		Get branch.

		:returns: Branch
		"""

		return {} if 'data' not in self.data else self.data['data']
