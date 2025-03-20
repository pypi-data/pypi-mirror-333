import yaml
import sys
import argparse
from pathlib import Path
from onlyaml.readonly_config import ReadonlyDict
from onlyaml.err import perr_exit


def parse_file(filepath: Path, exit_code=1):
    if (not filepath.is_file()):
        perr_exit(str(filepath) + " is not a file", exit_code=exit_code)

    with open(filepath) as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            if hasattr(exc, 'problem_mark'):
                mark = exc.problem_mark
                perr_exit(
                    ("\"{}\" is not a valid YAML file.\n" +
                     "Error at line {}, column {}")
                    .format(
                        str(filepath), mark.line+1, mark.column+1
                    ),
                    exit_code=exit_code
                )
            else:
                perr_exit(
                    "Error in {}: {}".format(str(filepath), exc),
                    exit_code=exit_code
                )

    return ReadonlyDict(config)


def parse(description="Your marvellous application !", exit_code=1):
    """
    Impose your program only accepting yaml file as command line argument.

    Your program will accept 2 arguments:
        -h / --help and
        --config CONFIG_FILE


    Return:
        a dict containing all the key-value in the yaml file.
    """
    parser = argparse.ArgumentParser(
        description=description)

    # --config argument that expects a file path
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the application configuration file."
    )

    args = parser.parse_args()
    file_path: str = args.config
    return parse_file(Path(file_path), exit_code=exit_code)
