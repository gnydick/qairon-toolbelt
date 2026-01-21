#!/usr/bin/env python3
import argparse
import os

from toolbelt_topology_levels import ToolbeltTopologyLevel


class CapitalizeAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.upper())


parser = argparse.ArgumentParser(description='Toolbelt setup')
parser.add_argument('dir', type=str, help='directory to updated')
parser.add_argument('-l', dest='level', type=str, default='ROOT', action=CapitalizeAction,
                    choices=[x.name.lower() for x in ToolbeltTopologyLevel])
parser.add_argument('-o', dest='overwrite_levels', action='append', default=[])
parser.add_argument('-e', dest='exclude_levels', action='append', default=[])


# '-f', help='output fields', dest='output_fields', action='append')


def process_dir(dir, iter, **kwargs):
    level = ToolbeltTopologyLevel(iter)
    level.setup(dir, **kwargs)
    with os.scandir(dir) as scan_dir:
        for entry in scan_dir:
            if iter <= len(ToolbeltTopologyLevel) - 1 and entry.is_dir():
                process_dir(entry.path, iter + 1, **kwargs)


def _main_():
    args = parser.parse_args()
    base_dir = args.dir
    level = getattr(ToolbeltTopologyLevel, args.level)
    process_dir(base_dir, level.value, exclude_levels=args.exclude_levels, overwrite_levels=args.overwrite_levels)


if __name__ == '__main__':
    _main_()
