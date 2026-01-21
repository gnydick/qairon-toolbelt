import os
import shutil
from enum import Enum


def smart_copy(src, dest, **kwargs):
    overwrite_levels = kwargs.get('overwrite_levels', [])
    if kwargs.get('level') in overwrite_levels or not os.path.exists(os.path.join(dest, '.envrc')):
        shutil.copy(src, dest)


_SEGMENTS = ('skel', 'root', 'environment', 'provider', 'id', 'region', 'partition', 'dep_target_type')


class ToolbeltTopologyLevel(Enum):
    ROOT = (1, os.path.join(*_SEGMENTS[0:2], '.envrc'))
    ENVIRONMENT = (2, os.path.join(*_SEGMENTS[0:3], '.envrc'))
    PROVIDER = (3, os.path.join(*_SEGMENTS[0:4], '.envrc'))
    ID = (4, os.path.join(*_SEGMENTS[0:5], '.envrc'))
    REGION = (5, os.path.join(*_SEGMENTS[0:6], '.envrc'))
    PARTITION = (6, os.path.join(*_SEGMENTS[0:7], '.envrc'))
    DEPLOYMENT_TARGET_TYPE = (7, os.path.join(*_SEGMENTS[0:8], '.envrc'))
    DEPLOYMENT_TARGET = (8, None)  # uses provider/{provider}/{target_type}/

    def __new__(cls, value, path):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.path = path
        return obj

    def setup(self, directory, **kwargs):
        level_name = self.name.lower()
        exclude_levels = kwargs.get('exclude_levels', [])
        if level_name in exclude_levels:
            return

        base_path = os.path.dirname(os.path.abspath(__file__))

        if self == ToolbeltTopologyLevel.DEPLOYMENT_TARGET:
            norm_dir = os.path.normpath(directory)

            # target_type is parent directory name (e.g., emr, eks)
            target_type = os.path.basename(os.path.dirname(norm_dir))

            # provider is 5 levels up from deployment_target
            provider_path = norm_dir
            for _ in range(5):
                provider_path = os.path.dirname(provider_path)
            provider = os.path.basename(provider_path)

            source = os.path.join(base_path, 'provider_svcs', provider, target_type, '.envrc')
        else:
            source = os.path.join(base_path, self.path)

        smart_copy(source, directory, level=level_name, **kwargs)