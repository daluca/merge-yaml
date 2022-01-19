"""Merge yaml configs."""
import argparse
import os

import yaml
from mergedeep import merge, Strategy


def walk_directory(directory):
    """Get all files from directory."""
    files_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                files_list.append(os.path.join(root, file))

    return files_list


def get_yaml_files(locations):
    """Return list of yaml files."""
    directories = [directory for directory in locations if os.path.isdir(directory)]
    files = [file for file in locations if os.path.isfile(file)]

    for directory in directories:
        files.extend(walk_directory(directory))

    return files


def yaml_loader(yaml_file) -> dict:
    """Load yaml file."""
    with open(yaml_file) as file_descriptor:
        data = yaml.safe_load(file_descriptor)

    if not data:
        print(f"{yaml_file} is empty")
        data = {}

    return data


def write_yaml_config(name=str, data=dict):
    """Write yaml file."""
    with open(name, "w") as file_descriptor:
        yaml.dump(data, file_descriptor, indent=2, sort_keys=False, )


def main(args):
    """Execute function code."""
    yaml_files = get_yaml_files(args.files)
    configs = [yaml_loader(file) for file in yaml_files]
    merged_config = merge(*configs, strategy=Strategy.TYPESAFE_ADDITIVE)
    write_yaml_config(args.output, merged_config)
    print(f"Successfully combined {' '.join(args.files)} to {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="YAML Config Combiner",
        description="Combine multiple yaml files for configuration purposes",
    )

    parser.add_argument("files", metavar="N", type=str, nargs="+", help="List of yaml files")
    parser.add_argument("-o", "--output", default="config.yaml", type=str, help="Output file name and location")

    args = parser.parse_args()

    main(args)
