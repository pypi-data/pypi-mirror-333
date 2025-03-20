# Onlyaml

Impose your python program only accepting `.yaml` as command line argument.

## Usage

```py
from onlyaml import parse

def main():
    config = parse()
    print(config)


if __name__ == "__main__":
    main()

```

```shell
python3 main.py --config config.yaml
```

the output will be a `dict` presenting your config.yaml

## Detail
Underlying, it uses `argparse` and `pyyaml` to define CL arguments and parse
`.yaml` file.

If the path is not a valid file, it terminate the program with `exit(1)`. You can customize the error code by optional



