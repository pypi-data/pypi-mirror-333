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


def test_orderlist_archive():
	"""
	Tests the OrderList_Archive API Call
	"""

	helper.provision_store('OrderList_Archive.xml')

	orderlist_archive_test_archive()


def orderlist_archive_test_archive():
	loadrequest = merchantapi.request.OrderListLoadQuery(helper.init_client())
	loadrequest.filters.is_in('id', '675000,675001,675002')
	loadresponse = loadrequest.send()

	helper.validate_response_success(loadresponse, merchantapi.response.OrderListLoadQuery)

	assert len(loadresponse.get_orders()) == 3

	request = merchantapi.request.OrderListArchive(helper.init_client())

	request.add_order_id(675003)
	request.set_delete_payment_data(True)
	request.set_delete_shipping_labels(True)

	for o in loadresponse.get_orders():
		request.add_order(o)
	
	response = request.send()

	helper.validate_response_success(response, merchantapi.response.OrderListArchive)

	assert response.get_processed() == 4
