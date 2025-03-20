"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ChangesetChange data model.
"""

from merchantapi.abstract import Model

class ChangesetChange(Model):
	def __init__(self, data: dict = None):
		"""
		ChangesetChange Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_item_type(self) -> str:
		"""
		Get item_type.

		:returns: string
		"""

		return self.get_field('item_type')

	def get_item_id(self) -> int:
		"""
		Get item_id.

		:returns: int
		"""

		return self.get_field('item_id', 0)

	def get_item_user_id(self) -> int:
		"""
		Get item_user_id.

		:returns: int
		"""

		return self.get_field('item_user_id', 0)

	def get_item_user_name(self) -> str:
		"""
		Get item_user_name.

		:returns: string
		"""

		return self.get_field('item_user_name')

	def get_item_user_icon(self) -> str:
		"""
		Get item_user_icon.

		:returns: string
		"""

		return self.get_field('item_user_icon')

	def get_item_version_id(self) -> int:
		"""
		Get item_version_id.

		:returns: int
		"""

		return self.get_field('item_version_id', 0)

	def get_item_identifier(self) -> str:
		"""
		Get item_identifier.

		:returns: string
		"""

		return self.get_field('item_identifier')

	def get_item_change_type(self) -> str:
		"""
		Get item_change_type.

		:returns: string
		"""

		return self.get_field('item_change_type')
