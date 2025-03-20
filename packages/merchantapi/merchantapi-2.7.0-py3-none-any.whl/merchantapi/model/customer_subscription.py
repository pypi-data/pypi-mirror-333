"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

CustomerSubscription data model.
"""

from .subscription import Subscription

class CustomerSubscription(Subscription):
	def __init__(self, data: dict = None):
		"""
		CustomerSubscription Constructor

		:param data: dict
		"""

		super().__init__(data)
