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


def test_store_load():
	"""
	Tests the Store_Load API Call
	"""

	helper.provision_store('Store_Load.xml')

	store_load_test_load()


def store_load_test_load():
	request = merchantapi.request.StoreLoad(helper.init_client())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.StoreLoad)

	store = response.get_store()

	assert isinstance(store, merchantapi.model.Store)
	assert store.get_manager_id() > 0
	assert store.get_tax_id() > 0
	assert store.get_user_interface_id() > 0
	assert store.get_branch_id() > 0
	assert store.get_currency_id() > 0
	assert store.get_box_packing_id() > 0
	assert store.get_address_validation_id() > 0
	assert store.get_name() == 'Dev Test Store'
	assert store.get_owner() == 'Jonathan Burchmore'
	assert store.get_icon() == 'graphics/en-US/admin/store_icon_1.png'
	assert store.get_email() == 'donotreply@miva.com'
	assert store.get_company() == 'Miva Merchant'
	assert store.get_address() == '5060 Shoreham Place, Suite 130'
	assert store.get_city() == 'San Diego'
	assert store.get_state() == 'CA'
	assert store.get_zip() == '92122'
	assert store.get_phone() == '858.490.2570'
	assert store.get_fax() == ''
	assert store.get_country() == 'US'
	assert store.get_weight_units() == 'lb'
	assert store.get_weight_unit_code() == 'LB'
	assert store.get_weight_digits() == 2
	assert store.get_display_mixed_weight_units() is False
	assert store.get_display_weight_less_than() is False
	assert store.get_dimension_units() == 'IN'
	assert store.get_defer_baskets() is True
	assert store.get_track_page_hits() is False
	assert len(store.get_maintenance_warning_message()) > 0
	assert len(store.get_maintenance_closed_message()) > 0
	assert store.get_maintenance_allowed_ips() == '0'
	assert store.get_scheduled_task_advance() == 0
	assert store.get_scheduled_task_timeout() == 0
	assert store.get_cache_type() == 'none'
	assert store.get_cache_compression() is False
	assert store.get_cache_expiration() == 240
	assert store.get_cache_set() >= 0
	assert store.get_cache_version() >= 0
	assert store.get_redis_host() == '127.0.0.1'
	assert store.get_redis_port() == 6379
	assert store.get_redis_expiration() == 300
	assert store.get_redis_timeout() == 1000
	assert store.get_price_group_overlap_resolution() == 'HIGHEST'
	assert store.get_character_set() == 'utf-8'
