"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

ShippingRuleMethod data model.
"""

from merchantapi.abstract import Model

class ShippingRuleMethod(Model):
	def __init__(self, data: dict = None):
		"""
		ShippingRuleMethod Constructor

		:param data: dict
		"""

		super().__init__(data)

	def get_module_code(self) -> str:
		"""
		Get module_code.

		:returns: string
		"""

		return self.get_field('module_code')

	def get_method_code(self) -> str:
		"""
		Get method_code.

		:returns: string
		"""

		return self.get_field('method_code')

	def set_module_code(self, module_code: str) -> 'ShippingRuleMethod':
		"""
		Set module_code.

		:param module_code: string
		:returns: ShippingRuleMethod
		"""

		return self.set_field('module_code', module_code)

	def set_method_code(self, method_code: str) -> 'ShippingRuleMethod':
		"""
		Set method_code.

		:param method_code: string
		:returns: ShippingRuleMethod
		"""

		return self.set_field('method_code', method_code)
