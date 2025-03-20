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


def test_changesetitemversionlist_load_query():
	"""
	Tests the ChangesetItemVersionList_Load_Query API Call
	"""

	helper.provision_store('ChangesetItemVersionList_Load_Query.xml')

	changesetitemversionlist_load_query_test_list_load()


def changesetitemversionlist_load_query_test_list_load():
	helper.delete_branch('CIVLLQ_1')

	default_branch = helper.get_branch('Production')
	assert default_branch != None

	branch = helper.create_branch('CIVLLQ_1', default_branch.get_color(), default_branch)
	assert branch is not None
	
	changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	changeset_request.set_sort('id', 'DESC')
	changeset_request.set_count(1)

	changeset_response = changeset_request.send()
	helper.validate_response_success(changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert len(changeset_response.get_changesets()) == 1

	request = merchantapi.request.ChangesetItemVersionListLoadQuery(helper.init_client(), changeset_response.get_changesets()[0])
	request.get_filters().like('code', 'CIVLLQ%')

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetItemVersionListLoadQuery)

	assert len(response.get_changeset_item_versions()) == 4

	for civ in response.get_changeset_item_versions():
		assert isinstance(civ, merchantapi.model.ChangesetItemVersion)
		assert civ.get_id() > 0
		assert civ.get_item_id() > 0
		assert 'CIVLLQ' in civ.get_code()
		assert len(civ.get_module_code()) > 0
		assert isinstance(civ.get_module(), merchantapi.model.Module)
		assert civ.get_module().get_id() > 0