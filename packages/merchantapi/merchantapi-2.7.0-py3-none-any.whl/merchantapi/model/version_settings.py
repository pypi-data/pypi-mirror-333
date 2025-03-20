"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

VersionSettings data model.
"""

from .variable_value import VariableValue

class VersionSettings(VariableValue):
	def __init__(self, data = None):
		"""
		VersionSettings Constructor

		:param data: mixed
		"""

		super().__init__(data)

	def has_item(self, item: str) -> bool:
		"""
		Check if an item exists in the dictionary

		:param item: {string}
		:returns: bool
		"""

		return self.has_property(item)
	
	def item_has_property(self, item: str, item_property: str) -> bool:
		"""
		Check if an item has a property

		:param item: {string}
		:param item_property: {string}
		:returns: bool
		"""
		
		return self.has_sub_property(item, item_property)

	def get_item(self, item: str):
		"""
		Get a items dictionary.

		:param item: str
		:returns: dict
		"""

		return self.get_property(item)

	def get_item_property(self, item: str, item_property: str):
		"""
		Get a items dictionary.

		:param item: str
		:param item_property: str
		:returns: dict
		"""

		return self.get_sub_property(item, item_property)


	def set_item(self, item: str, value: dict) -> 'VersionSettings':
		"""
		Set a item settings dictionary

		:param item: str
		:param value: dict
		:returns: VersionSettings
		"""

		return self.set_property(item, value)

	def set_item_property(self, item: str, item_property: str, value) -> 'VersionSettings':
		"""
		Set a item property value for a specific item

		:param item: str
		:param item_property: str
		:param value: mixed
		:returns: VersionSettings
		"""

		return self.set_sub_property(item, item_property, value)
