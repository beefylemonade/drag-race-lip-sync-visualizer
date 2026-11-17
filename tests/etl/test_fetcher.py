from core.constants import Franchise
from etl.fetcher import get_section_index


def test_get_section_index_no_response(mocker):
    # 1. Create a mock response and configure .json() to return an empty dict
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"parse": {"sections": []}}

    # 2. Patch requests.get where it is used (in the 'api' module)
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    assert get_section_index(Franchise.US, 3, "123") is None
    mock_get.assert_called_once()


def test_get_section_index_valid_response(mocker):

    intended_section_index = 1

    # 1. Create a mock response and configure .json() to return an empty dict
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "parse": {
            "sections": [
                {"line": "123", "index": intended_section_index},
                {"line": "456", "index": 2},
            ]
        }
    }

    # 2. Patch requests.get where it is used (in the 'api' module)
    mock_get = mocker.patch("requests.get", return_value=mock_response)

    assert get_section_index(Franchise.US, 3, "123") == intended_section_index
    mock_get.assert_called_once()
