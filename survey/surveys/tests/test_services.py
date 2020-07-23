import pytest

from survey.surveys.services import is_valid_uuid4


pytestmark = [pytest.mark.django_db]


@pytest.mark.parametrize('invalid_val',
                         [None, 0, '123', 'd180c934-dd75-42f3-adbc-79021488a39'])
def test_invalid_uuid4(invalid_val):
    assert is_valid_uuid4(invalid_val) is False


def test_valid_uuid():
    assert is_valid_uuid4('d180c934-dd75-42f3-adbc-79021488a395') is True
