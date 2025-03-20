"""
This file is part of the MerchantAPI package.

(c) Miva Inc <https://www.miva.com/>

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.
"""

import pytest
from merchantapi.listquery import ListQueryRequest, FilterExpression
from . import helper

helper.configure_logging()


def test_custom_filters():
	"""
	Tests the custom filter functionality of the list query class

	:return:
	"""

	class TestListQuery(ListQueryRequest):
		available_custom_filters = {
			'int_test': 'int',
			'float_test': 'float',
			'string_test': 'str',
			'bool_test': 'bool',
			'choice_test': [
				'foo',
				'bar',
				9
			]
		}

	lq = TestListQuery()

	with pytest.raises(Exception):
		lq.set_custom_filter('invalid', 'foo')

	lq.set_custom_filter('int_test', 100)

	with pytest.raises(Exception):
		lq.set_custom_filter('int_test', 'foo')

	lq.set_custom_filter('float_test', 15.25)

	with pytest.raises(Exception):
		lq.set_custom_filter('float_test', 'foo')

	lq.set_custom_filter('string_test', 'foo')

	with pytest.raises(Exception):
		lq.set_custom_filter('string_test', 10)

	lq.set_custom_filter('bool_test', False)

	with pytest.raises(Exception):
		lq.set_custom_filter('bool_test', 10)

	lq.set_custom_filter('choice_test', 'foo')

	with pytest.raises(Exception):
		lq.set_custom_filter('choice_test', 'invalid')

	for filter in lq.get_custom_filters():
		assert filter['name'] in ['int_test','float_test','string_test','bool_test','choice_test']

		if filter['name'] == 'int_test':			assert filter['value'] == 100
		elif filter['name'] == 'float_test':		assert filter['value'] == 15.25
		elif filter['name'] == 'string_test':		assert filter['value'] == 'foo'
		elif filter['name'] == 'bool_test':			assert filter['value'] is False
		elif filter['name'] == 'choice_test':		assert filter['value'] == 'foo'
		else:
			pytest.fail('Unexpected value')

	lq.remove_custom_filter('int_test')

	for filter in lq.get_custom_filters():
		assert filter['name'] is not 'int_test'


def test_filter_expression():
	"""
	Tests the FilterExpression class

	:return:
	"""

	filter_expression_test_simple()
	filter_expression_test_complex()
	filter_expression_test_only_subexpressions()


def filter_expression_test_simple():
	"""
	Test a simple top level only filter with no subexpressions
	"""
	expr = FilterExpression()

	expr.equal('foo', 'bar').and_equal('bar', 'baz').or_equal('bar', 'foo')

	data = expr.to_list()

	assert len(data) == 1
	assert data[0]['name'] == 'search'
	assert len(data[0]['value']) == 3

	assert data[0]['value'][0]['field'] == 'foo'
	assert data[0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][0]['value'] == 'bar'

	assert data[0]['value'][1]['field'] == 'search_AND'
	assert data[0]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][1]['value']) == 1
	assert data[0]['value'][1]['value'][0]['field'] == 'bar'
	assert data[0]['value'][1]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][1]['value'][0]['value'] == 'baz'

	assert data[0]['value'][2]['field'] == 'search_OR'
	assert data[0]['value'][2]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][2]['value']) == 1
	assert data[0]['value'][2]['value'][0]['field'] == 'bar'
	assert data[0]['value'][2]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][2]['value'][0]['value'] == 'foo'


def filter_expression_test_complex():
	"""
	Test a more complex expression with both top level entries and subexpressions
	"""

	expression = FilterExpression()
	sub_expression1 = expression.expr()
	sub_expression2 = expression.expr()
	
	expression.equal('foo', 'bar').and_equal('bar', 'baz')
	sub_expression1.equal('bin', 'bar').and_greater_than('baz', 5)
	sub_expression2.equal('bin', 'foo').or_equal('baz', 2)

	expression.and_x(sub_expression1)
	expression.or_x(sub_expression2)

	data = expression.to_list()
	
	assert len(data) == 1
	assert data[0]['name'] == 'search'
	assert len(data[0]['value']) == 4

	assert data[0]['value'][0]['field'] == 'foo'
	assert data[0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][0]['value'] == 'bar'
	
	assert data[0]['value'][1]['field'] == 'search_AND'
	assert data[0]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][1]['value']) == 1
	assert data[0]['value'][1]['value'][0]['field'] == 'bar'
	assert data[0]['value'][1]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][1]['value'][0]['value'] == 'baz'

	assert data[0]['value'][2]['field'] == 'search_AND'
	assert data[0]['value'][2]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][2]['value']) == 2
	assert data[0]['value'][2]['value'][0]['field'] == 'search'
	assert data[0]['value'][2]['value'][0]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][2]['value'][0]['value']) == 1
	assert data[0]['value'][2]['value'][0]['value'][0]['field'] == 'bin'
	assert data[0]['value'][2]['value'][0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][2]['value'][0]['value'][0]['value'] == 'bar'	
	assert data[0]['value'][2]['value'][1]['field'] == 'search_AND'
	assert data[0]['value'][2]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][2]['value'][1]['value']) == 1
	assert data[0]['value'][2]['value'][1]['value'][0]['field'] == 'baz'
	assert data[0]['value'][2]['value'][1]['value'][0]['operator'] == 'GT'
	assert data[0]['value'][2]['value'][1]['value'][0]['value'] == '5'

	assert data[0]['value'][3]['field'] == 'search_OR'
	assert data[0]['value'][3]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][3]['value']) == 2
	assert data[0]['value'][3]['value'][0]['field'] == 'search'
	assert data[0]['value'][3]['value'][0]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][3]['value'][0]['value']) == 1
	assert data[0]['value'][3]['value'][0]['value'][0]['field'] == 'bin'
	assert data[0]['value'][3]['value'][0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][3]['value'][0]['value'][0]['value'] == 'foo'	
	assert data[0]['value'][3]['value'][1]['field'] == 'search_OR'
	assert data[0]['value'][3]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][3]['value'][1]['value']) == 1
	assert data[0]['value'][3]['value'][1]['value'][0]['field'] == 'baz'
	assert data[0]['value'][3]['value'][1]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][3]['value'][1]['value'][0]['value'] == '2'


def	filter_expression_test_only_subexpressions():
	"""
	Test an expression which only contains subexpressions
	"""

	type_code_list = [
		{ 'type': 'readytheme_contentsection', 'code': 'address_validation' },
		{ 'type': 'flex', 'code': 'mmx-text-area' }
	]

	expression = FilterExpression()

	for type_code in type_code_list:
		expression.or_x( expression.expr().equal( 'type', type_code['type'] ).and_equal( 'code', type_code['code'] ) )

	data = expression.to_list()
	
	assert len(data) == 1
	assert data[0]['name'] == 'search'
	assert len(data[0]['value']) == 2

	assert data[0]['value'][0]['field'] == 'search_OR'
	assert data[0]['value'][0]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][0]['value']) == 2
	assert data[0]['value'][0]['value'][0]['field'] == 'search'
	assert data[0]['value'][0]['value'][0]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][0]['value'][0]['value']) == 1
	assert data[0]['value'][0]['value'][0]['value'][0]['field'] == 'type'
	assert data[0]['value'][0]['value'][0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][0]['value'][0]['value'][0]['value'] == 'readytheme_contentsection'
	assert data[0]['value'][0]['value'][1]['field'] == 'search_AND'
	assert data[0]['value'][0]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][0]['value'][1]['value']) == 1
	assert data[0]['value'][0]['value'][1]['value'][0]['field'] == 'code'
	assert data[0]['value'][0]['value'][1]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][0]['value'][1]['value'][0]['value'] == 'address_validation'

	assert data[0]['value'][1]['field'] == 'search_OR'
	assert data[0]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][1]['value']) == 2
	assert data[0]['value'][1]['value'][0]['field'] == 'search'
	assert data[0]['value'][1]['value'][0]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][1]['value'][0]['value']) == 1
	assert data[0]['value'][1]['value'][0]['value'][0]['field'] == 'type'
	assert data[0]['value'][1]['value'][0]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][1]['value'][0]['value'][0]['value'] == 'flex'
	assert data[0]['value'][1]['value'][1]['field'] == 'search_AND'
	assert data[0]['value'][1]['value'][1]['operator'] == 'SUBWHERE'
	assert len(data[0]['value'][1]['value'][1]['value']) == 1
	assert data[0]['value'][1]['value'][1]['value'][0]['field'] == 'code'
	assert data[0]['value'][1]['value'][1]['value'][0]['operator'] == 'EQ'
	assert data[0]['value'][1]['value'][1]['value'][0]['value'] == 'mmx-text-area'

