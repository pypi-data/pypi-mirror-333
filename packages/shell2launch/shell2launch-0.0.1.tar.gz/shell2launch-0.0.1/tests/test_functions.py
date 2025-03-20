import pytest

import shell2launch


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param("positional \\\n", {"positional": []}, id="positional"),
        pytest.param("--store_true \\\n", {"--store_true": []}, id="boolean"),
        pytest.param("--no_val \\\n", {"--no_val": []}, id="no value"),
        pytest.param(
            "--single_val 1 \\\n", {"--single_val": ["1"]}, id="single value"
        ),
        pytest.param(
            "--list_val 1 2 3 4 \\\n",
            {"--list_val": ["1", "2", "3", "4"]},
            id="multiple values",
        ),
        pytest.param("-s short \\\n", {"-s": ["short"]}, id="short option"),
        pytest.param(
            '--path "some/path/with/qoutes.txt" \\\n',
            {"--path": ["some/path/with/qoutes.txt"]},
            id="path with quotes",
        ),
    ],
)
def test_parse_args(test_input, expected):
    output = shell2launch._parse_args(test_input)
    assert output == expected


def test_parse_args_with_positional_and_optional():
    test_input = "positional \\\n--single_val 1 \\\n-s short \\\n"
    output = shell2launch._parse_args(test_input)
    assert output == {
        "positional": [],
        "--single_val": ["1"],
        "-s": ["short"],
    }


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            "   whitespaces", "whitespaces", id="starting whitespaces"
        ),
        pytest.param("whitespaces    ", "whitespaces", id="ending whitespaces"),
        pytest.param("#comment\nuncomment", "uncomment", id="commented line"),
        pytest.param("line1\nline2", "line1\nline2", id="multiple lines"),
        pytest.param(
            "   line1  \n    line2   ",
            "line1\nline2",
            id="multiple lines with whitespaces",
        ),
    ],
)
def test_clean_shell_code(test_input, expected):
    output = shell2launch._clean_shell_code(test_input)
    assert output == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            {"positional": []},
            ['"args": [\n', '\t"positional",\n', "]"],
            id="single positional",
        ),
        pytest.param(
            {"--optional": []},
            ['"args": [\n', '\t"--optional",\n', "]"],
            id="optional no value",
        ),
        pytest.param(
            {"--optional": ["1"]},
            ['"args": [\n', '\t"--optional", "1",\n', "]"],
            id="optional single value",
        ),
        pytest.param(
            {"--optional": ["1", "2", "3"]},
            ['"args": [\n', '\t"--optional", "1", "2", "3",\n', "]"],
            id="optional multiple values",
        ),
    ],
)
def test_build_args_string(test_input, expected):
    output = shell2launch._build_args_strings(test_input)
    assert output == expected


def test_build_launch_string():
    args = [
        '"args": [\n',
        '\t"positional"\n',
        '\t"--optional", "1", "2", "3",\n',
        "]",
    ]
    python_filename = "testfile.py"
    expected = (
        "{\n"
        + '\t"name": "Python Debugger: testfile.py with Arguments",\n'
        + '\t"type": "debugpy",\n'
        + '\t"request": "launch",\n'
        + '\t"program": "testfile.py",\n'
        + '\t"console": "integratedTerminal",\n'
        + '\t"args": [\n'
        + '\t\t"positional"\n'
        + '\t\t"--optional", "1", "2", "3",\n'
        + "\t]"
        + "\n}"
    )
    output = shell2launch._build_launch_string(
        python_filename=python_filename, args=args
    )
    assert output == expected


shell2launch_expected_full = (
    "{\n"
    + '\t"name": "Python Debugger: testfile.py with Arguments",\n'
    + '\t"type": "debugpy",\n'
    + '\t"request": "launch",\n'
    + '\t"program": "testfile.py",\n'
    + '\t"console": "integratedTerminal",\n'
    + '\t"args": [\n'
    + '\t\t"argument",\n'
    + "\t]"
    + "\n}"
)
shell2launch_expected_args_only = '"args": [\n' + '\t"argument",\n' + "]"
shell2launch_testcode = "python testfile.py \\\n" + "argument \\\n"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        pytest.param(
            (shell2launch_testcode, False),
            shell2launch_expected_full,
            id="full return value",
        ),
        pytest.param(
            (shell2launch_testcode, True),
            shell2launch_expected_args_only,
            id="args_only return value",
        ),
    ],
)
def test_shell2launch(test_input, expected):
    output = shell2launch.shell2launch(test_input[0], test_input[1])
    assert output == expected


def test_shell2launch_error_without_python_call():
    shell_code = "--no python call"
    with pytest.raises(ValueError):
        shell2launch.shell2launch(shell_code=shell_code)
