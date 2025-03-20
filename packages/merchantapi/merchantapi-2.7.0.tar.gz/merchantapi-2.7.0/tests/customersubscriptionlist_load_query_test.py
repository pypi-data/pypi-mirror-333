"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import merchantapi.request
import merchantapi.response
import merchantapi.model
import time
import datetime
from . import helper


def test_customer_subscription_list_load_query():
	"""
	Tests the CustomerSubscriptionList_Load_Query API Call
	"""

	helper.provision_store('MivaPay.xml')
	helper.provision_store('CustomerSubscriptionList_Load_Query.xml')

	customer_subscription_list_load_query_test_list_load()
	customer_subscription_list_load_query_test_list_load_with_filters()


def customer_subscription_list_load_query_test_list_load():
	customer = helper.get_customer('CSLLQ_1')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_1')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ')

	assert methods is not None and len(methods) == 1

	attributes = [ merchantapi.model.SubscriptionAttribute() ]

	attributes[0].set_code('FOO')
	attributes[0].set_value('BAR')
	attributes[0].set_template_code('BAZ')

	subscription1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1, attributes)
	subscription2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1, attributes)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 2

	for subscription in response.get_customer_subscriptions():
		create_subscription = subscription1 if subscription.get_id() == subscription1.get_id() else subscription2
		product = products[0] if subscription.get_product_id() == products[0].get_id() else products[1]

		assert subscription.get_quantity() == 1
		assert subscription.get_tax() == 0.00
		assert subscription.get_shipping() == 2.50
		assert subscription.get_subtotal() == 10.00
		assert subscription.get_total() == 12.50
		assert subscription.get_formatted_tax() == "$0.00"
		assert subscription.get_formatted_shipping() == "$2.50"
		assert subscription.get_formatted_subtotal() == "$10.00"
		assert subscription.get_formatted_total() == "$12.50"
		assert subscription.get_frequency() == "daily"
		assert subscription.get_term() == 2
		assert subscription.get_description() == "Daily"
		assert subscription.get_n() == 0
		assert subscription.get_fixed_day_of_week() == 0
		assert subscription.get_fixed_day_of_month() == 0
		assert subscription.get_subscription_count() == 1
		assert subscription.get_method() == "CSLLQ"
		assert subscription.get_ship_data() == "CSLLQ"
		assert subscription.get_ship_id() > 0
		assert subscription.get_subscription_term_id() > 0
		assert subscription.get_address_id() == addresses[0].get_id()
		assert subscription.get_term_remaining() == 2
		assert subscription.get_term_processed() == 0

		# Product Fields
		assert subscription.get_product_code() == product.get_code()
		assert subscription.get_product_name() == product.get_name()
		assert subscription.get_product_sku() == product.get_sku()
		assert subscription.get_product_price() == product.get_price()
		assert subscription.get_product_formatted_price() == product.get_formatted_price()
		assert subscription.get_product_cost() == product.get_cost()
		assert subscription.get_product_formatted_cost() == product.get_formatted_cost()
		assert subscription.get_product_weight() == product.get_weight()
		assert subscription.get_product_formatted_weight() == product.get_formatted_weight()
		assert subscription.get_product_taxable() == product.get_taxable()
		assert subscription.get_product_thumbnail() == product.get_thumbnail()
		assert subscription.get_product_image() == product.get_image()
		assert subscription.get_product_active() == product.get_active()
		assert subscription.get_product_date_time_created() == product.get_date_time_created()
		assert subscription.get_product_date_time_updated() == product.get_date_time_update()
		assert subscription.get_product_page_title() == product.get_page_title()
		assert subscription.get_product_page_id() == product.get_page_id()
		assert subscription.get_product_page_code() == product.get_page_code()
		assert subscription.get_product_canonical_category_code() == product.get_canonical_category_code()
		assert subscription.get_product_canonical_category_id() >= 0

		# Payment Fields
		assert subscription.get_payment_card_last_four() == "1111"
		assert subscription.get_payment_card_type() == "Visa"
		assert subscription.get_customer_payment_card_id() == card.get_id()

		# Address Fields
		assert subscription.get_address_description() == addresses[0].get_description()
		assert subscription.get_address_first_name() == addresses[0].get_first_name()
		assert subscription.get_address_last_name() == addresses[0].get_last_name()
		assert subscription.get_address_email() == addresses[0].get_email()
		assert subscription.get_address_company() == addresses[0].get_company()
		assert subscription.get_address_phone() == addresses[0].get_phone()
		assert subscription.get_address_fax() == addresses[0].get_fax()
		assert subscription.get_address_address() == addresses[0].get_address1() + " " + addresses[0].get_address2()
		assert subscription.get_address_address1() == addresses[0].get_address1()
		assert subscription.get_address_address2() == addresses[0].get_address2()
		assert subscription.get_address_city() == addresses[0].get_city()
		assert subscription.get_address_state() == addresses[0].get_state()
		assert subscription.get_address_zip() == addresses[0].get_zip()
		assert subscription.get_address_country() == addresses[0].get_country()
		assert subscription.get_address_residential() == addresses[0].get_residential()

		# Customer Fields
		assert subscription.get_customer_id() == customer.get_id()
		assert subscription.get_customer_login() == customer.get_login()
		assert subscription.get_customer_password_email() == customer.get_password_email()
		assert subscription.get_customer_business_title() == customer.get_business_title()

		# Options
		assert len(subscription.get_options()) == 1;
		assert subscription.get_options()[0].get_subscription_id() == subscription.get_id()
		assert subscription.get_options()[0].get_template_code() == "BAZ"
		assert subscription.get_options()[0].get_attribute_code() == "FOO"
		assert subscription.get_options()[0].get_value() == "BAR"


def customer_subscription_list_load_query_test_list_load_with_filters():
	customer = helper.get_customer('CSLLQ_2')
	products = helper.get_products(['CSLLQ_1', 'CSLLQ_2'])
	addresses = helper.get_customer_addresses('CSLLQ_2')

	assert customer is not None
	assert products is not None and len(products) == 2
	assert addresses is not None and len(addresses) > 0

	card = helper.register_payment_card_with_address(customer, addresses[0])

	assert card is not None

	methods = helper.get_subscription_shipping_methods(customer, products[0], 'Daily', addresses[0], card, 1, 'CO', 'CSLLQ');

	assert methods is not None and len(methods) == 1

	sub1 = helper.create_subscription(customer, products[0], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)
	sub2 = helper.create_subscription(customer, products[1], 'Daily', int(time.mktime(datetime.date.today().timetuple())), addresses[0], card, methods[0].get_module().get_id(), 'CSLLQ', 1)

	request = merchantapi.request.CustomerSubscriptionListLoadQuery(helper.init_client())

	request.set_customer_id(customer.get_id())
	request.filters.equal('product_code', products[1].get_code())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.CustomerSubscriptionListLoadQuery)

	assert len(response.get_customer_subscriptions()) == 1
	assert response.get_customer_subscriptions()[0].get_id() == sub2.get_id()
