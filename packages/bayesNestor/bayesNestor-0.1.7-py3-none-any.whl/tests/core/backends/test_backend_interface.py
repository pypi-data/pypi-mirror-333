from unittest.mock import patch

import pytest

from bayesnestor.core.backends.IBackend import IBackend


@patch.multiple(IBackend, __abstractmethods__=set())
def test_validate_interface_instantiation_raises_exception():
    instance = IBackend()

    with pytest.raises(NotImplementedError) as e:
        assert instance.query(variables=None, evidence=None)

    with pytest.raises(NotImplementedError) as e:
        assert instance.interventional_query(variables=None, do=None, evidence=None)

