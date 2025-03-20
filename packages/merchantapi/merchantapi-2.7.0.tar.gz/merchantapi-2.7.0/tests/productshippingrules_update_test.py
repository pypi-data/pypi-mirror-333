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


def test_productshippingrules_update():
	"""
	Tests the ProductShippingRules_Update API Call
	"""

	helper.provision_domain('ProductShippingRules_Update_Domain.xml')
	helper.provision_store('ProductShippingRules_Update.xml')

	productshippingrules_update_test_update()


def productshippingrules_update_test_update():
	helper.assign_api_token_group('PSRU')

	product = helper.get_product('PSRU_1')

	assert product != None
	assert product.get_product_shipping_rules().get_own_package() is False
	assert product.get_product_shipping_rules().get_limit_methods() is False
	assert len(product.get_product_shipping_rules().get_methods()) == 0

	request = merchantapi.request.ProductShippingRulesUpdate(helper.init_client(), product)

	request.set_ships_in_own_packaging(True)
	request.set_limit_shipping_methods(True)
	request.set_width(1.32)
	request.set_length(4.65)
	request.set_height(7.98)

	method1 = merchantapi.model.ShippingRuleMethod()
	method2 = merchantapi.model.ShippingRuleMethod()

	method1.set_module_code('flatrate')
	method1.set_method_code('PSRU_flatrate_1')

	method2.set_module_code('flatrate')
	method2.set_method_code('PSRU_flatrate_2')

	request.add_shipping_method(method1)
	request.add_shipping_method(method2)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ProductShippingRulesUpdate)

	check = helper.get_product('PSRU_1')

	assert check != None
	assert check.get_product_shipping_rules().get_own_package() is True
	assert check.get_product_shipping_rules().get_limit_methods() is True
	assert check.get_product_shipping_rules().get_width() == 1.32
	assert check.get_product_shipping_rules().get_length() == 4.65
	assert check.get_product_shipping_rules().get_height() == 7.98
	assert len(check.get_product_shipping_rules().get_methods()) == 2