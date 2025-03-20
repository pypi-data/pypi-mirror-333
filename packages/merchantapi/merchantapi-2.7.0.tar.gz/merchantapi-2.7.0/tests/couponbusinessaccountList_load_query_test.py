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


def test_couponbusinessaccountlist_load_query():
	"""
	Tests the CouponBusinessAccountList_Load_Query API Call
	"""

	helper.provision_store('CouponBusinessAccountList_Load_Query.xml')

	couponbusinessaccountlist_load_query_test_list_load_all()
	couponbusinessaccountlist_load_query_test_list_load_assigned()
	couponbusinessaccountlist_load_query_test_list_load_unassigned()


def couponbusinessaccountlist_load_query_test_list_load_all():
	request = merchantapi.request.CouponBusinessAccountListLoadQuery(helper.init_client())
	request.set_coupon_code('CBALLQ_1')
	request.set_assigned(True)
	request.set_unassigned(True)
	request.get_filters().like('title', 'CBALLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponBusinessAccountListLoadQuery)

	assert len(response.get_coupon_business_accounts()) == 4

	expected = {
		'CBALLQ_1': True,
		'CBALLQ_2': False,
		'CBALLQ_3': True,
		'CBALLQ_4': False
	};

	for cba in response.get_coupon_business_accounts():
		assert isinstance(cba, merchantapi.model.CouponBusinessAccount)
		assert cba.get_title() in expected.keys()
		assert cba.get_assigned() == expected[cba.get_title()]


def couponbusinessaccountlist_load_query_test_list_load_assigned():
	request = merchantapi.request.CouponBusinessAccountListLoadQuery(helper.init_client())
	request.set_coupon_code('CBALLQ_1')
	request.set_assigned(True)
	request.set_unassigned(False)
	request.get_filters().like('title', 'CBALLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponBusinessAccountListLoadQuery)

	assert len(response.get_coupon_business_accounts()) == 2


	for cba in response.get_coupon_business_accounts():
		assert isinstance(cba, merchantapi.model.CouponBusinessAccount)
		assert cba.get_title() in [ 'CBALLQ_1', 'CBALLQ_3' ]
		assert cba.get_assigned() == True


def couponbusinessaccountlist_load_query_test_list_load_unassigned():
	request = merchantapi.request.CouponBusinessAccountListLoadQuery(helper.init_client())
	request.set_coupon_code('CBALLQ_1')
	request.set_assigned(False)
	request.set_unassigned(True)
	request.get_filters().like('title', 'CBALLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CouponBusinessAccountListLoadQuery)

	assert len(response.get_coupon_business_accounts()) == 2


	for cba in response.get_coupon_business_accounts():
		assert isinstance(cba, merchantapi.model.CouponBusinessAccount)
		assert cba.get_title() in [ 'CBALLQ_2', 'CBALLQ_4' ]
		assert cba.get_assigned() == False
