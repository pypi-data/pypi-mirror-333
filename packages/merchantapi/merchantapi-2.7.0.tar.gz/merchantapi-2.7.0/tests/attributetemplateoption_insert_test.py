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


def test_attribute_template_option_insert():
	"""
	Tests the AttributeTemplateOption_Insert API Call
	"""

	helper.provision_store('AttributeTemplateOption_Insert.xml')

	attribute_template_option_insert_test_insertion()
	attribute_template_option_insert_test_high_precision_insertion()


def attribute_template_option_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateOptionInsert(helper.init_client())

	request.set_attribute_template_code('ATOI_Template_1')
	request.set_attribute_template_attribute_code('ATOI_Attribute_1')
	request.set_code('ATOI_Option_1')
	request.set_prompt('ATOI_Option_1')
	request.set_price(2.22)
	request.set_cost(3.33)
	request.set_weight(4.44)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionInsert)

	assert isinstance(response.get_attribute_template_option(), merchantapi.model.AttributeTemplateOption)
	assert response.get_attribute_template_option().get_code() == 'ATOI_Option_1'
	assert response.get_attribute_template_option().get_prompt() == 'ATOI_Option_1'
	assert response.get_attribute_template_option().get_price() == 2.22
	assert response.get_attribute_template_option().get_cost() == 3.33
	assert response.get_attribute_template_option().get_weight() == 4.44
	assert response.get_attribute_template_option().get_formatted_price() == '$2.22'
	assert response.get_attribute_template_option().get_formatted_cost() == '$3.33'
	assert response.get_attribute_template_option().get_formatted_weight() == '4.44 lb'

	check = helper.get_attribute_template_option('ATOI_Template_1', 'ATOI_Attribute_1', 'ATOI_Option_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_option().get_id()
	assert check.get_code() == 'ATOI_Option_1'
	assert check.get_prompt() == 'ATOI_Option_1'
	assert check.get_price() == 2.22
	assert check.get_formatted_price() == '$2.22'
	assert check.get_cost() == 3.33
	assert check.get_formatted_cost() == '$3.33'
	assert check.get_weight() == 4.44
	assert check.get_formatted_weight() == '4.44 lb'


def attribute_template_option_insert_test_high_precision_insertion():
	request = merchantapi.request.AttributeTemplateOptionInsert(helper.init_client())

	request.set_attribute_template_code('ATOI_Template_1')
	request.set_attribute_template_attribute_code('ATOI_Attribute_HP')
	request.set_code('ATOI_Option_HP')
	request.set_prompt('ATOI_Option_HP')
	request.set_price(2.12345678)
	request.set_cost(3.12345678)
	request.set_weight(4.12345678)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateOptionInsert)

	assert isinstance(response.get_attribute_template_option(), merchantapi.model.AttributeTemplateOption)
	assert response.get_attribute_template_option().get_price() == 2.12345678
	assert response.get_attribute_template_option().get_cost() == 3.12345678
	assert response.get_attribute_template_option().get_weight() == 4.12345678
	assert response.get_attribute_template_option().get_formatted_price() == '$2.12345678'
	assert response.get_attribute_template_option().get_formatted_cost() == '$3.12345678'
	assert response.get_attribute_template_option().get_formatted_weight() == '4.12345678 lb'

	check = helper.get_attribute_template_option('ATOI_Template_1', 'ATOI_Attribute_HP', 'ATOI_Option_HP')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_option().get_id()
	assert check.get_price() == 2.12345678
	assert check.get_formatted_price() == '$2.12345678'
	assert check.get_cost() == 3.12345678
	assert check.get_formatted_cost() == '$3.12345678'
	assert check.get_weight() == 4.12345678
	assert check.get_formatted_weight() == '4.12345678 lb'
