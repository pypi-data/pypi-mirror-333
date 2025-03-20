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


def test_page_copy_branch():
	"""
	Tests the Page_Copy_Branch API Call
	"""

	helper.provision_store('Page_Copy_Branch.xml')

	page_copy_branch_test_copy()
	page_copy_branch_test_copy_with_rules()


def page_copy_branch_test_copy():
	helper.delete_branch('PCB_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('PCB_1', default_branch.get_color(), default_branch)
	assert branch != None

	helper.delete_page('PCB_1', branch)

	check = helper.get_page('PCB_1', branch)
	assert check == None

	request = merchantapi.request.PageCopyBranch(helper.init_client())
	request.set_source_page_code('PCB_1')
	request.set_destination_branch_id(branch.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageCopyBranch)

	check = helper.get_page('PCB_1', branch)

	assert check != None


def page_copy_branch_test_copy_with_rules():
	helper.delete_branch('PCB_2')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('PCB_2', default_branch.get_color(), default_branch)
	assert branch != None

	helper.delete_page('PCB_2', branch)

	check = helper.get_page('PCB_2', branch)
	assert check == None

	request = merchantapi.request.PageCopyBranch(helper.init_client())
	request.set_source_page_code('PCB_2')
	request.set_destination_branch_id(branch.get_id())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.PageCopyBranch)

	check = helper.get_page('PCB_2', branch)

	assert check != None
