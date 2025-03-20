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


def test_attribute_template_attribute_insert():
	"""
	Tests the AttributeTemplateAttribute_Insert API Call
	"""

	helper.provision_store('AttributeTemplateAttribute_Insert.xml')

	attribute_template_attribute_insert_test_insertion()
	attribute_template_attribute_insert_test_high_precision_insertion()


def attribute_template_attribute_insert_test_insertion():
	request = merchantapi.request.AttributeTemplateAttributeInsert(helper.init_client())

	request.set_attribute_template_code('ATAI_Template_1')
	request.set_code('ATAI_Attribute_1')
	request.set_prompt('ATAI_Attribute_1')
	request.set_price(1.11)
	request.set_cost(2.22)
	request.set_weight(3.33)
	request.set_type('checkbox')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeInsert)

	assert isinstance(response.get_attribute_template_attribute(), merchantapi.model.AttributeTemplateAttribute)
	assert response.get_attribute_template_attribute().get_attribute_template_id() > 0
	assert response.get_attribute_template_attribute().get_code() == 'ATAI_Attribute_1'
	assert response.get_attribute_template_attribute().get_prompt() == 'ATAI_Attribute_1'
	assert response.get_attribute_template_attribute().get_type() == 'checkbox'
	assert response.get_attribute_template_attribute().get_price() == 1.11
	assert response.get_attribute_template_attribute().get_cost() == 2.22
	assert response.get_attribute_template_attribute().get_weight() == 3.33
	assert response.get_attribute_template_attribute().get_formatted_price() == '$1.11'
	assert response.get_attribute_template_attribute().get_formatted_cost() == '$2.22'
	assert response.get_attribute_template_attribute().get_formatted_weight() == '3.33 lb'

	check = helper.get_attribute_template_attribute('ATAI_Template_1', 'ATAI_Attribute_1')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_attribute().get_id()
	assert check.get_code() == 'ATAI_Attribute_1'
	assert check.get_prompt() == 'ATAI_Attribute_1'
	assert check.get_type() == 'checkbox'
	assert check.get_price() == 1.11
	assert check.get_cost() == 2.22
	assert check.get_weight() == 3.33
	assert check.get_formatted_weight() == '3.33 lb'


def attribute_template_attribute_insert_test_high_precision_insertion():
	request = merchantapi.request.AttributeTemplateAttributeInsert(helper.init_client())

	request.set_attribute_template_code('ATAI_Template_1')
	request.set_code('ATAI_Attribute_HP')
	request.set_prompt('ATAI_Attribute_HP')
	request.set_price(1.12345678)
	request.set_cost(2.12345678)
	request.set_weight(3.12345678)
	request.set_type('checkbox')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.AttributeTemplateAttributeInsert)

	assert isinstance(response.get_attribute_template_attribute(), merchantapi.model.AttributeTemplateAttribute)
	assert response.get_attribute_template_attribute().get_attribute_template_id() > 0
	assert response.get_attribute_template_attribute().get_code() == 'ATAI_Attribute_HP'
	assert response.get_attribute_template_attribute().get_prompt() == 'ATAI_Attribute_HP'
	assert response.get_attribute_template_attribute().get_type() == 'checkbox'
	assert response.get_attribute_template_attribute().get_price() == 1.12345678
	assert response.get_attribute_template_attribute().get_cost() == 2.12345678
	assert response.get_attribute_template_attribute().get_weight() == 3.12345678
	assert response.get_attribute_template_attribute().get_formatted_price() == '$1.12345678'
	assert response.get_attribute_template_attribute().get_formatted_cost() == '$2.12345678'
	assert response.get_attribute_template_attribute().get_formatted_weight() == '3.12345678 lb'

	check = helper.get_attribute_template_attribute('ATAI_Template_1', 'ATAI_Attribute_HP')

	assert check is not None
	assert check.get_id() == response.get_attribute_template_attribute().get_id()
	assert check.get_code() == 'ATAI_Attribute_HP'
	assert check.get_prompt() == 'ATAI_Attribute_HP'
	assert check.get_type() == 'checkbox'
	assert check.get_price() == 1.12345678
	assert check.get_cost() == 2.12345678
	assert check.get_weight() == 3.12345678
	assert check.get_formatted_weight() == '3.12345678 lb'
