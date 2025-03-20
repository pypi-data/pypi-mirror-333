"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ModuleChange data model.
"""

from merchantapi.abstract import Model
from .variable_value import VariableValue

class ModuleChange(Model):
	def __init__(self, data: dict = None):
		"""
		ModuleChange Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('Module_Data'):
			value = self.get_field('Module_Data')
			if not isinstance(value, VariableValue):
				self.set_field('Module_Data', VariableValue(value))

	def get_module_code(self) -> str:
		"""
		Get Module_Code.

		:returns: string
		"""

		return self.get_field('Module_Code')

	def get_module_operation(self) -> str:
		"""
		Get Module_Operation.

		:returns: string
		"""

		return self.get_field('Module_Operation')

	def get_module_data(self):
		"""
		Get Module_Data.

		:returns: VariableValue|None
		"""

		return self.get_field('Module_Data', None)

	def set_module_code(self, module_code: str) -> 'ModuleChange':
		"""
		Set Module_Code.

		:param module_code: string
		:returns: ModuleChange
		"""

		return self.set_field('Module_Code', module_code)

	def set_module_operation(self, module_operation: str) -> 'ModuleChange':
		"""
		Set Module_Operation.

		:param module_operation: string
		:returns: ModuleChange
		"""

		return self.set_field('Module_Operation', module_operation)

	def set_module_data(self, module_data) -> 'ModuleChange':
		"""
		Set Module_Data.

		:param module_data: VariableValue|dict
		:returns: ModuleChange
		:raises Exception:
		"""

		if module_data is None or isinstance(module_data, VariableValue):
			return self.set_field('Module_Data', module_data)
		return self.set_field('Module_Data', VariableValue(module_data))

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'Module_Data' in ret and isinstance(ret['Module_Data'], VariableValue):
			ret['Module_Data'] = ret['Module_Data'].to_dict()

		return ret
