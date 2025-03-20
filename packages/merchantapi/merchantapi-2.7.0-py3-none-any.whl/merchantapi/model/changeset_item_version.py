"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ChangesetItemVersion data model.
"""

from merchantapi.abstract import Model
from .module import Module

class ChangesetItemVersion(Model):
	def __init__(self, data: dict = None):
		"""
		ChangesetItemVersion Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('module'):
			value = self.get_field('module')
			if isinstance(value, dict):
				if not isinstance(value, Module):
					self.set_field('module', Module(value))
			else:
				raise Exception('Expected Module or a dict')

	def get_id(self) -> int:
		"""
		Get id.

		:returns: int
		"""

		return self.get_field('id', 0)

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_user_id(self) -> int:
		"""
		Get user_id.

		:returns: int
		"""

		return self.get_field('user_id', 0)

	def get_user_name(self) -> str:
		"""
		Get user_name.

		:returns: string
		"""

		return self.get_field('user_name')

	def get_user_icon(self) -> str:
		"""
		Get user_icon.

		:returns: string
		"""

		return self.get_field('user_icon')

	def get_code(self) -> str:
		"""
		Get code.

		:returns: string
		"""

		return self.get_field('code')

	def get_module_code(self) -> str:
		"""
		Get mod_code.

		:returns: string
		"""

		return self.get_field('mod_code')

	def get_module(self):
		"""
		Get module.

		:returns: Module|None
		"""

		return self.get_field('module', None)

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'module' in ret and isinstance(ret['module'], Module):
			ret['module'] = ret['module'].to_dict()

		return ret
