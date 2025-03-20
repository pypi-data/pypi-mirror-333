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


def test_changeset_change_list_load_query():
	"""
	Tests the ChangesetChangeList_Load_Query API Call
	"""

	helper.provision_store('ChangesetChangeList_Load_Query.xml')

	changeset_change_list_load_query_test_list_load()
	changeset_change_list_load_query_test_list_load_MMAPI220()


def changeset_change_list_load_query_test_list_load():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create 3 Changes in one changeset

	create_changeset_request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	change1 = merchantapi.model.TemplateChange()
	change2 = merchantapi.model.TemplateChange()
	change3 = merchantapi.model.TemplateChange()

	change1.set_template_filename('ccllq_1.mvc').set_source('CCLLQ_1 Updated')
	change2.set_template_filename('ccllq_2.mvc').set_source('CCLLQ_2 Updated')
	change3.set_template_filename('ccllq_3.mvc').set_source('CCLLQ_3 Updated')

	create_changeset_request.add_template_change(change1)
	create_changeset_request.add_template_change(change2)
	create_changeset_request.add_template_change(change3)

	create_changeset_response = create_changeset_request.send()

	helper.validate_response_success(create_changeset_response, merchantapi.response.ChangesetCreate)

	changeset = create_changeset_response.get_changeset()

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetChangeListLoadQuery(helper.init_client(), changeset)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetChangeListLoadQuery)

	assert len(response.get_changeset_changes()) == 3

	for change in response.get_changeset_changes():
		assert isinstance(change, merchantapi.model.ChangesetChange)


def changeset_change_list_load_query_test_list_load_MMAPI220():
	helper.delete_branch('Production Copy')

	production_branch = helper.get_branch('Production')

	assert production_branch is not None

	branch = helper.create_branch('Production Copy', '#000000', production_branch)

	assert branch is not None

	# Create a Change

	create_changeset_request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	change = merchantapi.model.TemplateChange()

	change.set_template_filename('ccllq_4.mvc').set_source('CCLLQ_4 Updated')

	create_changeset_request.add_template_change(change)

	create_changeset_response = create_changeset_request.send()

	helper.validate_response_success(create_changeset_response, merchantapi.response.ChangesetCreate)

	changeset = create_changeset_response.get_changeset()

	assert isinstance(changeset, merchantapi.model.Changeset)

	request = merchantapi.request.ChangesetChangeListLoadQuery(helper.init_client(), changeset)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetChangeListLoadQuery)

	assert len(response.get_changeset_changes()) == 1

	for change in response.get_changeset_changes():
		assert isinstance(change, merchantapi.model.ChangesetChange)
		assert change.get_item_type() != None
		assert change.get_item_id() != None
		assert change.get_item_user_id() != None
		assert change.get_item_user_name() != None
		assert change.get_item_user_icon() != None
		assert change.get_item_version_id() != None
		assert change.get_item_identifier() != None
		assert change.get_item_change_type() != None
