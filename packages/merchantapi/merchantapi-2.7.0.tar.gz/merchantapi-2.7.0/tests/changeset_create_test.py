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


def test_changeset_create():
	"""
	Tests the Changeset_Create API Call
	"""

	helper.provision_store('Changeset_Create.xml')

	changeset_create_test_creation()
	changeset_create_test_creation_module()


def changeset_create_test_creation():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	assert request.get_branch_id() == branch.get_id()

	# Load a Changeset
	load_changeset_request = merchantapi.request.ChangesetListLoadQuery(helper.init_client(), branch)
	load_changeset_response = load_changeset_request.send()

	helper.validate_response_success(load_changeset_response, merchantapi.response.ChangesetListLoadQuery)

	assert isinstance(load_changeset_response.get_changesets(), list)
	assert len(load_changeset_response.get_changesets()) > 0

	changeset = load_changeset_response.get_changesets()[0]

	assert isinstance(changeset, merchantapi.model.Changeset)

	# Add a Change
	change1 = merchantapi.model.TemplateChange()
	change1.set_template_filename('changesetcreate_1.mvc').set_source('ChangesetCreate_1 Change')

	request.add_template_change(change1)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCreate)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)


def changeset_create_test_creation_module():
	branch = helper.get_branch('Production')

	assert branch is not None

	request = merchantapi.request.ChangesetCreate(helper.init_client(), branch)

	change_struct = merchantapi.model.ModuleChange()
	change_array = merchantapi.model.ModuleChange()
	change_scalar = merchantapi.model.ModuleChange()

	change_struct.set_module_code('api_changeset_create_test')
	change_struct.set_module_operation('success')
	change_struct.set_module_data({ 'foo': 'bar'})

	change_array.set_module_code('api_changeset_create_test')
	change_array.set_module_operation('success')
	change_array.set_module_data([ { 'foo': 'bar'}, { 'bar': 'foo'} ])

	change_scalar.set_module_code('api_changeset_create_test')
	change_scalar.set_module_operation('success')
	change_scalar.set_module_data('foo')

	request.add_module_change(change_struct)
	request.add_module_change(change_array)
	request.add_module_change(change_scalar)

	response = request.send()

	helper.validate_response_success(response, merchantapi.response.ChangesetCreate)

	assert isinstance(response.get_changeset(), merchantapi.model.Changeset)
