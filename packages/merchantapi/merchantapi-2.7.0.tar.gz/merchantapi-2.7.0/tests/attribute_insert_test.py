"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import decimal
from . import helper


def test_attribute_insert():
	"""
	Tests the Attribute_Insert API Call
	"""

	helper.provision_store('Attribute_Insert.xml')

	attribute_insert_test_insertion()
	attribute_insert_test_high_precision_insertion()


def attribute_insert_test_insertion():
	request = merchantapi.request.AttributeInsert(helper.init_client())

	request.set_product_code("AttributeInsertTest_1")
	request.set_code('TestInsert1')
	request.set_prompt('TestInsert1')
	request.set_type('checkbox')
	request.set_image('')
	request.set_price(2.00)
	request.set_cost(1.00)
	request.set_weight(3.00)
	request.set_copy(False)
	request.set_required(False)
	request.set_inventory(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeInsert)

	assert isinstance(response.get_product_attribute(), merchantapi.model.ProductAttribute)
	assert response.get_product_attribute().get_code() == 'TestInsert1'
	assert response.get_product_attribute().get_prompt() == 'TestInsert1'
	assert response.get_product_attribute().get_price() == 2.00
	assert response.get_product_attribute().get_cost() == 1.00
	assert response.get_product_attribute().get_weight() == 3.00
	assert response.get_product_attribute().get_formatted_weight() == '3.00 lb'
	assert response.get_product_attribute().get_type() == 'checkbox'

	check = helper.get_product_attribute('AttributeInsertTest_1', 'TestInsert1')

	assert check is not None
	assert check.get_id() == response.get_product_attribute().get_id()
	assert check.get_code() == 'TestInsert1'
	assert check.get_prompt() == 'TestInsert1'
	assert check.get_price() == 2.00
	assert check.get_cost() == 1.00
	assert check.get_weight() == 3.00
	assert check.get_formatted_price() == '$2.00'
	assert check.get_formatted_cost() == '$1.00'
	assert check.get_formatted_weight() == '3.00 lb'
	assert check.get_type() == 'checkbox'


def attribute_insert_test_high_precision_insertion():
	request = merchantapi.request.AttributeInsert(helper.init_client())

	request.set_product_code("AttributeInsertTest_HP")
	request.set_code('AttributeInsertTest_HP')
	request.set_prompt('AttributeInsertTest_HP')
	request.set_type('checkbox')
	request.set_image('')
	request.set_price(1.12345678)
	request.set_cost(2.12345678)
	request.set_weight(3.12345678)
	request.set_copy(False)
	request.set_required(False)
	request.set_inventory(False)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeInsert)

	assert isinstance(response.get_product_attribute(), merchantapi.model.ProductAttribute)
	assert response.get_product_attribute().get_code() == 'AttributeInsertTest_HP'
	assert response.get_product_attribute().get_prompt() == 'AttributeInsertTest_HP'
	assert response.get_product_attribute().get_price() == 1.12345678
	assert response.get_product_attribute().get_cost() == 2.12345678
	assert response.get_product_attribute().get_weight() == 3.12345678
	assert response.get_product_attribute().get_formatted_price() == '$1.12345678'
	assert response.get_product_attribute().get_formatted_cost() == '$2.12345678'
	assert response.get_product_attribute().get_formatted_weight() == '3.12345678 lb'
	assert response.get_product_attribute().get_type() == 'checkbox'

	check = helper.get_product_attribute('AttributeInsertTest_HP', 'AttributeInsertTest_HP')

	assert check is not None
	assert check.get_id() == response.get_product_attribute().get_id()
	assert check.get_code() == 'AttributeInsertTest_HP'
	assert check.get_prompt() == 'AttributeInsertTest_HP'
	assert check.get_price() == 1.12345678
	assert check.get_cost() == 2.12345678
	assert check.get_weight() == 3.12345678
	assert check.get_formatted_price() == '$1.12345678'
	assert check.get_formatted_cost() == '$2.12345678'
	assert check.get_formatted_weight() == '3.12345678 lb'
	assert check.get_type() == 'checkbox'