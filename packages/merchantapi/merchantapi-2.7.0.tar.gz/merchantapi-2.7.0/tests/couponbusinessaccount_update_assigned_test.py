"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
from . import helper


def test_couponbusinessaccount_update_assigned():
	"""
	Tests the CouponBusinessAccount_Update_Assigned API Call
	"""

	helper.provision_store('CouponBusinessAccount_Update_Assigned.xml')

	couponbusinessaccount_update_assigned_test_assignment()
	couponbusinessaccount_update_assigned_test_unassignment()


def couponbusinessaccount_update_assigned_test_assignment():
	coupon = helper.get_coupon('CBAUA_1')

	assert coupon is not None

	request = merchantapi.request.CouponBusinessAccountUpdateAssigned(helper.init_client(), coupon)
	request.set_business_account_title('CBAUA_1')
	request.set_assigned(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponBusinessAccountUpdateAssigned)

	check = helper.get_coupon_business_accounts('CBAUA_1', 'CBAUA_1', True, False)

	assert len(check) == 1


def couponbusinessaccount_update_assigned_test_unassignment():
	coupon = helper.get_coupon('CBAUA_1')

	assert coupon is not None

	request = merchantapi.request.CouponBusinessAccountUpdateAssigned(helper.init_client(), coupon)
	request.set_business_account_title('CBAUA_2')
	request.set_assigned(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponBusinessAccountUpdateAssigned)

	check = helper.get_coupon_business_accounts('CBAUA_1', 'CBAUA_2', False, True)

	assert len(check) == 1
