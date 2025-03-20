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


def test_branchitemversionlist_load_query():
	"""
	Tests the BranchItemVersionList_Load_Query API Call
	"""

	helper.provision_store('BranchItemVersionList_Load_Query.xml')

	branchitemversionlist_load_query_test_list_load()


def branchitemversionlist_load_query_test_list_load():
	helper.delete_branch('BIVLLQ_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('BIVLLQ_1', default_branch.get_color(), default_branch)
	assert branch is not None

	request = merchantapi.request.BranchItemVersionListLoadQuery(helper.init_client(), branch)
	request.get_filters().like('code', 'BIVLLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchItemVersionListLoadQuery)

	assert len(response.get_branch_item_versions()) == 4

	for biv in response.get_branch_item_versions():
		assert biv.get_id() > 0
		assert biv.get_item_id() > 0
		assert 'BIVLLQ' in biv.get_code()
		assert len(biv.get_module_code()) > 0
		assert isinstance(biv.get_module(), merchantapi.model.Module)
		assert biv.get_module().get_id() > 0
