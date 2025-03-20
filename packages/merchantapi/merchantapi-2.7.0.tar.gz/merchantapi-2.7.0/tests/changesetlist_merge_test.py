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


def test_changeset_list_merge():
	"""
	Tests the ChangesetList_Merge API Call
	"""

	helper.provision_store('ChangesetList_Merge.xml')

	changeset_list_merge_test_merge()


def changeset_list_merge_test_merge():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create 3 seperate Changes

	create_changeset_request1 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)
	create_changeset_request2 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)
	create_changeset_request3 = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	change1 = merchantapi.model.TemplateChange()
	change2 = merchantapi.model.TemplateChange()
	change3 = merchantapi.model.TemplateChange()

	change1.set_template_filename('clm_1.mvc').set_source('CLM_1 Updated')
	change2.set_template_filename('clm_2.mvc').set_source('CLM_2 Updated')
	change3.set_template_filename('clm_3.mvc').set_source('CLM_3 Updated')

	create_changeset_request1.add_template_change(change1)
	create_changeset_request2.add_template_change(change2)
	create_changeset_request3.add_template_change(change3)

	create_changeset_response1 = create_changeset_request1.send()
	create_changeset_response2 = create_changeset_request2.send()
	create_changeset_response3 = create_changeset_request3.send()

	helper.validate_response_success(create_changeset_response1, merchantapi.response.ChangesetCreate)
	helper.validate_response_success(create_changeset_response2, merchantapi.response.ChangesetCreate)
	helper.validate_response_success(create_changeset_response3, merchantapi.response.ChangesetCreate)

	assert isinstance(create_changeset_response1.get_changeset(), merchantapi.model.Changeset)
	assert isinstance(create_changeset_response2.get_changeset(), merchantapi.model.Changeset)
	assert isinstance(create_changeset_response3.get_changeset(), merchantapi.model.Changeset)

	# Now merge the changes into one change

	request = merchantapi.request.ChangesetListMerge(helper.init_client(), branch)

	request.add_changeset(create_changeset_response1.get_changeset())
	request.add_changeset(create_changeset_response2.get_changeset())
	request.add_changeset(create_changeset_response3.get_changeset())

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetListMerge)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)
	assert response.get_completed() is True
	assert response.get_changesetlist_merge_session_id() is None
