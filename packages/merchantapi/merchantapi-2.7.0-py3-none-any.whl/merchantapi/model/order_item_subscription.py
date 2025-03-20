"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

OrderItemSubscription data model.
"""

from .base_subscription import BaseSubscription
from .product_subscription_term import ProductSubscriptionTerm
from .subscription_option import SubscriptionOption

class OrderItemSubscription(BaseSubscription):
	def __init__(self, data: dict = None):
		"""
		OrderItemSubscription Constructor

		:param data: dict
		"""

		super().__init__(data)
		if self.has_field('productsubscriptionterm'):
			value = self.get_field('productsubscriptionterm')
			if isinstance(value, dict):
				if not isinstance(value, ProductSubscriptionTerm):
					self.set_field('productsubscriptionterm', ProductSubscriptionTerm(value))
			else:
				raise Exception('Expected ProductSubscriptionTerm or a dict')

		if self.has_field('options'):
			value = self.get_field('options')
			if isinstance(value, list):
				for i, e in enumerate(value):
					if isinstance(e, dict):
						if not isinstance(e, SubscriptionOption):
							value[i] = SubscriptionOption(e)
					else:
						raise Exception('Expected list of SubscriptionOption or dict')
			else:
				raise Exception('Expected list of SubscriptionOption or dict')

	def get_method(self) -> str:
		"""
		Get method.

		:returns: string
		"""

		return self.get_field('method')

	def get_product_subscription_term(self):
		"""
		Get productsubscriptionterm.

		:returns: ProductSubscriptionTerm|None
		"""

		return self.get_field('productsubscriptionterm', None)

	def get_options(self):
		"""
		Get options.

		:returns: List of SubscriptionOption
		"""

		return self.get_field('options', [])

	def to_dict(self) -> dict:
		"""
		Reduce the model to a dict.
		"""

		ret = self.copy()

		if 'productsubscriptionterm' in ret and isinstance(ret['productsubscriptionterm'], ProductSubscriptionTerm):
			ret['productsubscriptionterm'] = ret['productsubscriptionterm'].to_dict()

		if 'options' in ret and isinstance(ret['options'], list):
			for i, e in enumerate(ret['options']):
				if isinstance(e, SubscriptionOption):
					ret['options'][i] = ret['options'][i].to_dict()

		return ret
