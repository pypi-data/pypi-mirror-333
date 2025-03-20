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


def test_page_delete():
	"""
	Tests the Page_Delete API Call
	"""

	helper.provision_store('Page_Delete.xml')

	page_delete_test_deletion()
	page_delete_test_branch_deletion()


def page_delete_test_deletion():
	request = merchantapi.request.PageDelete(helper.init_client())

	request.set_page_code('PageDeleteTest_1')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageDelete)

	check = helper.get_page('PageDeleteTest_1')

	assert check is None


def page_delete_test_branch_deletion():
	helper.delete_branch('PageDeleteTest_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('PageDeleteTest_1', default_branch.get_color(), default_branch)

	request = merchantapi.request.PageDelete(helper.init_client())

	request.set_page_code('PageDeleteTest_2')
	request.set_branch_id(branch.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageDelete)

	checkDefault = helper.get_page('PageDeleteTest_2')
	checkBranch = helper.get_page('PageDeleteTest_2', branch)

	assert checkBranch is None
	assert checkDefault is not None
