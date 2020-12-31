import yaml
from .exceptions import ScmError
from typing import List


def get_packages_from_file(file_path: str) -> List[str]:
  with open(file_path) as file:
    packages = yaml.load(file, Loader=yaml.FullLoader)

  if 'spec' not in packages:
    raise ScmError('spec in not provided in the file')
  else:
    return packages['spec']
