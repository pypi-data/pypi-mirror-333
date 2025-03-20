import pytest

import shell2launch


@pytest.fixture
def output():
    with open("testing/example.txt", "r") as f:
        return f.read() + "\n"


def test_main(capsys, output):
    assert shell2launch.main(["testing/example.sh"]) == 0

    out, err = capsys.readouterr()
    assert out == output


def test_main_with_output_path(tmp_path, output):
    shell2launch.main(
        ["testing/example.sh", f"--output_filepath={tmp_path}/example.txt"]
    )
    with open(tmp_path / "example.txt", "r") as f:
        assert f.read() + "\n" == output


def test_main_error_without_args():
    with pytest.raises(SystemExit):
        shell2launch.main([])


def test_main_error_with_empty_string():
    with pytest.raises(IsADirectoryError):
        shell2launch.main([""])


def test_main_error_with_non_existing_file():
    with pytest.raises(FileNotFoundError):
        shell2launch.main(["random_subdir/almost_certainly_does_not_exist.sh"])
