from __future__ import unicode_literals
from textx import (metamodel_from_str)
import os.path
from pytest import raises
from textx.exceptions import TextXError


grammar = r"""
Model: 'MyModel' name=ID;
"""

text = r"""
MyModel test1
"""


def test_model_kwargs():
    mm = metamodel_from_str(grammar)
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter1", "an example param (1)"
    )
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter2", "an example param (2)"
    )

    m = mm.model_from_str(text, parameter1='P1', parameter2='P2')
    assert m.name == 'test1'
    assert hasattr(m, '_tx_model_kwargs')
    assert len(m._tx_model_kwargs) == 2
    assert len(m._tx_model_kwargs.used_keys) == 0

    assert not m._tx_model_kwargs.have_all_parameters_been_used()

    assert m._tx_model_kwargs['parameter1'] == 'P1'
    assert len(m._tx_model_kwargs.used_keys) == 1
    assert 'parameter1' in m._tx_model_kwargs.used_keys
    assert 'parameter2' not in m._tx_model_kwargs.used_keys

    assert not m._tx_model_kwargs.have_all_parameters_been_used()

    assert m._tx_model_kwargs['parameter2'] == 'P2'
    assert len(m._tx_model_kwargs.used_keys) == 2
    assert 'parameter1' in m._tx_model_kwargs.used_keys
    assert 'parameter2' in m._tx_model_kwargs.used_keys

    assert m._tx_model_kwargs.have_all_parameters_been_used()

    assert m._tx_model_kwargs.get_with_default(
        'missing_params', 'default value') == 'default value'
    assert m._tx_model_kwargs.get_with_default(
        'parameter1', 'default value') == 'P1'

    with raises(TextXError, match=".*unknown parameter myerror2.*"):
        mm.model_from_str(text, parameter1='P1', myerror2='P2')

    assert len(mm._tx_model_kwarg_definitions) == 2
    assert mm._tx_model_kwarg_definitions['parameter1'].description ==\
           "an example param (1)"


def test_model_kwargs_empty():
    mm = metamodel_from_str(grammar)
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter1", "an example param (1)"
    )
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter2", "an example param (2)"
    )

    m = mm.model_from_str(text)
    assert m.name == 'test1'
    assert hasattr(m, '_tx_model_kwargs')
    assert len(m._tx_model_kwargs) == 0

    assert m._tx_model_kwargs.have_all_parameters_been_used()


def test_model_kwargs_file_based():
    mm = metamodel_from_str(grammar)
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter1", "an example param (1)"
    )
    mm._tx_model_kwarg_definitions.add_definition(
        "parameter2", "an example param (2)"
    )

    current_dir = os.path.dirname(__file__)
    m = mm.model_from_file(
        os.path.join(current_dir, 'test_model_kwargs',
                     'model.txt'),
        parameter1='P1', parameter2='P2')
    assert m.name == 'file_based'
    assert hasattr(m, '_tx_model_kwargs')
    assert len(m._tx_model_kwargs) == 2
