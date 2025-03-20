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


def test_page_insert():
	"""
	Tests the Page_Insert API Call
	"""

	helper.provision_store('Page_Insert.xml')

	page_insert_test_insertion()
	page_insert_test_branch_insertion()
	page_insert_test_fragment_insertion()


def page_insert_test_insertion():
	request = merchantapi.request.PageInsert(helper.init_client())

	request.set_page_code('PageInsertTest_1')
	request.set_page_name('PageInsertTest_1')
	request.set_page_title('PageInsertTest_1')
	request.set_page_layout(False)
	request.set_page_template('Hello World')
	request.set_page_cache(merchantapi.model.Page.PAGE_CACHE_TYPE_ALWAYS)
	request.set_page_secure(True)
	request.set_page_uri('/my-custom-page-uri')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageInsert)

	assert response.get_page().get_id() > 0
	assert response.get_page().get_code() == 'PageInsertTest_1'
	assert response.get_page().get_name() == 'PageInsertTest_1'
	assert response.get_page().get_title() == 'PageInsertTest_1'
	assert response.get_page().get_layout() == False
	assert response.get_page().get_admin() == False
	assert response.get_page().get_secure() == True

	check = helper.get_page('PageInsertTest_1')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'PageInsertTest_1'
	assert check.get_name() == 'PageInsertTest_1'
	assert check.get_title() == 'PageInsertTest_1'
	assert check.get_layout() == False
	assert check.get_admin() == False
	assert check.get_secure() == True


def page_insert_test_branch_insertion():
	helper.delete_branch('PageInsertTest_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('PageInsertTest_1', default_branch.get_color(), default_branch)

	request = merchantapi.request.PageInsert(helper.init_client())

	request.set_page_code('PageInsertTest_2')
	request.set_page_name('PageInsertTest_2')
	request.set_page_title('PageInsertTest_2')
	request.set_page_layout(False)
	request.set_page_template('Hello World')
	request.set_page_cache(merchantapi.model.Page.PAGE_CACHE_TYPE_ALWAYS)
	request.set_page_secure(True)
	request.set_branch_id(branch.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageInsert)

	assert response.get_page().get_id() > 0
	assert response.get_page().get_code() == 'PageInsertTest_2'
	assert response.get_page().get_name() == 'PageInsertTest_2'
	assert response.get_page().get_title() == 'PageInsertTest_2'
	assert response.get_page().get_layout() == False
	assert response.get_page().get_admin() == False
	assert response.get_page().get_secure() == True

	check = helper.get_page('PageInsertTest_2', branch)

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'PageInsertTest_2'
	assert check.get_name() == 'PageInsertTest_2'
	assert check.get_title() == 'PageInsertTest_2'
	assert check.get_layout() == False
	assert check.get_admin() == False
	assert check.get_secure() == True

def page_insert_test_fragment_insertion():
	request = merchantapi.request.PageInsert(helper.init_client())

	request.set_page_code('PageInsertTest_3')
	request.set_page_name('PageInsertTest_3')
	request.set_page_title('PageInsertTest_3')
	request.set_page_layout(False)
	request.set_page_template('Hello World')
	request.set_page_cache(merchantapi.model.Page.PAGE_CACHE_TYPE_ALWAYS)
	request.set_page_secure(True)
	request.set_page_public(True)
	request.set_page_fragment(True)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageInsert)

	assert response.get_page().get_id() > 0
	assert response.get_page().get_code() == 'PageInsertTest_3'
	assert response.get_page().get_name() == 'PageInsertTest_3'
	assert response.get_page().get_title() == 'PageInsertTest_3'
	assert response.get_page().get_layout() == False
	assert response.get_page().get_admin() == False
	assert response.get_page().get_secure() == True
	assert response.get_page().get_public() == True
	assert response.get_page().get_fragment() == True

	check = helper.get_page('PageInsertTest_3')

	assert check is not None
	assert check.get_id() > 0
	assert check.get_code() == 'PageInsertTest_3'
	assert check.get_name() == 'PageInsertTest_3'
	assert check.get_title() == 'PageInsertTest_3'
	assert check.get_layout() == False
	assert check.get_admin() == False
	assert check.get_secure() == True
	assert check.get_public() == True
	assert check.get_fragment() == True