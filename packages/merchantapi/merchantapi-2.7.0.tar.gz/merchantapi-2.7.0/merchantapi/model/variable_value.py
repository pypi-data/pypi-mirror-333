"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

VariableValue data model.
"""

class VariableValue():
	def __init__(self, data = None):
		"""
		VariableValue Constructor

		:param data: dict
		"""

		self.data = data

	def __delitem__(self, key):
		"""
		Allows for array access deletion on the object when list or dict

		:returns: void
		"""

		if self.is_dict() or (self.is_list() and isinstance(value, int)):
			del self.data[key]

	def __getitem__(self, key):
		"""
		Allows for array access reading on the object when list or dict

		:returns: void
		"""
		if self.is_dict() or (self.is_list() and isinstance(value, int)):
			return self.data[key] if key in self.data else None
		return None

	def __setitem__(self, key, value):
		"""
		Allows for array access writing on the object when list or dict

		:returns: void
		"""
		if self.is_dict() or (self.is_list() and isinstance(value, int)):
			self.data[key] = value

	def is_scalar(self) -> bool:
		"""
		Check if the underlying data is a scalar value

		:returns: bool
		"""

		return not isinstance(self.data, dict) and not isinstance(self.data, list)

	def is_list(self) -> bool:
		"""
		Check if the underlying data is a list

		:returns: bool
		"""

		return isinstance(self.data, list)

	def is_dict(self) -> bool:
		"""
		Check if the underlying data is a dictionary

		:returns: bool
		"""

		return isinstance(self.data, dict)

	def has_property(self, property: str) -> bool:
		"""
		Check if a property exists in the dictionary

		:param property: {string}
		:returns: bool
		"""

		return self.is_dict() and property in self.data;
	
	def has_sub_property(self, property: str, sub_property: str) -> bool:
		"""
		Check if an dictionary property has a sub property

		:param property: {string}
		:param sub_property: {string}
		:returns: bool
		"""
		
		if not self.is_dict() or not self.has_property(property):
			return False

		return sub_property in self.data[property];

	def get_property(self, property: str):
		"""
		Get a property if it exists.

		:param property: str
		:returns: dict
		"""

		return self.data[property] if self.is_dict() and self.has_property(property) else None

	def get_sub_property(self, property: str, sub_property: str):
		"""
		Get a sub-property.

		:param property: str
		:param sub_property: str
		:returns: dict
		"""

		return self.data[property][sub_property] if self.is_dict() and self.has_sub_property(property, sub_property) else None

	def get_data(self):
		"""
		Get the underlying data

		:returns: mixed
		"""

		return self.data

	def set_data(self, data) -> 'VariableValue':
		"""
		Get the underlying data
		
		:param data: mixed
		:returns: VariableValue
		"""

		self.data = data
		return self

	def to_dict(self):
		"""
		Reduce the model to a dict.
		"""

		return self.data


	def set_property(self, property: str, value) -> 'VariableValue':
		"""
		Set a dictionary property

		:param property: str
		:param value: mixed
		:returns: VariableValue
		"""

		if self.is_dict():
			self.data[property] = value		
		return self

	def set_sub_property(self, property: str, sub_property: str, value) -> 'VariableValue':
		"""
		Set a sub-property

		:param property: str
		:param sub_property: str
		:param value: mixed
		:returns: VariableValue
		"""

		if self.is_dict():
			if not self.has_property(property):
				self.data[property] = {}

			self.data[property][sub_property] = value
		return self
