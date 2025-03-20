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


def test_page_update():
	"""
	Tests the Page_Update API Call
	"""

	helper.provision_store('Page_Update.xml')

	page_update_test_update()
	page_update_test_update_branch()


def page_update_test_update():
	request = merchantapi.request.PageUpdate(helper.init_client())

	request.set_page_code('PageUpdateTest_1')
	request.set_page_name('PageUpdateTest_1 Updated')
	request.set_page_title('PageUpdateTest_1 Updated')
	request.set_page_cache(merchantapi.model.Page.PAGE_CACHE_TYPE_ALLEMPTY)
	request.set_page_secure(True)
	request.set_page_public(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageUpdate)

	check = helper.get_page('PageUpdateTest_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'PageUpdateTest_1'
	assert check.get_name() == 'PageUpdateTest_1 Updated'
	assert check.get_title() == 'PageUpdateTest_1 Updated'
	assert check.get_layout() == False
	assert check.get_admin() == False
	assert check.get_secure() == True
	assert check.get_public() == True
	assert check.get_cache() == merchantapi.model.Page.PAGE_CACHE_TYPE_ALLEMPTY


def page_update_test_update_branch():
	helper.delete_branch('PageUpdateTest_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('PageUpdateTest_1', default_branch.get_color(), default_branch)

	request = merchantapi.request.PageUpdate(helper.init_client())

	request.set_page_code('PageUpdateTest_2')
	request.set_page_name('PageUpdateTest_2 Updated')
	request.set_page_title('PageUpdateTest_2 Updated')
	request.set_page_cache(merchantapi.model.Page.PAGE_CACHE_TYPE_ALLEMPTY)
	request.set_page_secure(True)
	request.set_branch_id(branch.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageUpdate)

	check = helper.get_page('PageUpdateTest_2', branch)

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'PageUpdateTest_2'
	assert check.get_name() == 'PageUpdateTest_2 Updated'
	assert check.get_title() == 'PageUpdateTest_2 Updated'
	assert check.get_layout() == False
	assert check.get_admin() == False
	assert check.get_secure() == True
	assert check.get_cache() == merchantapi.model.Page.PAGE_CACHE_TYPE_ALLEMPTY
