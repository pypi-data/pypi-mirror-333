from unittest.mock import MagicMock, patch

import pytest

from bayesnestor.utils.Utils import check_file_type


@pytest.mark.parametrize(
    "file_path, valid_extensions, file_exists, file_suffix, expected",
    [
        ("test_file.xml", [".xml", ".txt", ".csv"], True, ".xml", True),
        ("test_file.doc", [".xml", ".txt", ".csv"], True, ".doc", False),
        ("nonexistent_file.xml", [".xml", ".txt", ".csv"], False, None, False),
        ("test_file.csv", [".xml", ".txt", ".csv"], True, ".csv", True),
        ("test_file.txt", [".xml", ".txt"], True, ".txt", True),
        ("test_file.jpg", [".xml", ".txt", ".csv"], True, ".jpg", False),
    ],
)
def test_check_file_type(
    file_path, valid_extensions, file_exists, file_suffix, expected
):
    with patch("pathlib.Path.exists") as mock_exists, patch(
        "pathlib.Path.suffix", new_callable=MagicMock
    ) as mock_suffix:

        mock_exists.return_value = file_exists
        if file_suffix is not None:
            mock_suffix.__get__ = MagicMock(return_value=file_suffix)

        assert check_file_type(file_path, valid_extensions) == expected
