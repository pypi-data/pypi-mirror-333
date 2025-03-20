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


def test_branchpageversionlist_load_query():
	"""
	Tests the BranchPageVersionList_Load_Query API Call
	"""

	helper.provision_store('BranchPageVersionList_Load_Query.xml')

	branchpageversionlist_load_query_test_list_load()


def branchpageversionlist_load_query_test_list_load():
	helper.delete_branch('BPVLLQ_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('BPVLLQ_1', default_branch.get_color(), default_branch)
	assert branch is not None

	request = merchantapi.request.BranchPageVersionListLoadQuery(helper.init_client(), branch)
	request.get_filters().like('code', 'BPVLLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.BranchPageVersionListLoadQuery)

	assert len(response.get_branch_page_versions()) == 2

	for i, bpv in enumerate(response.get_branch_page_versions()):
		assert isinstance(bpv, merchantapi.model.BranchPageVersion)
		assert bpv.get_id() > 0
		assert bpv.get_page_id() > 0
		assert f'BPVLLQ_{i+1}' == bpv.get_code()