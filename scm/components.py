from .exceptions import ScmError
import subprocess
import re
from os.path import dirname
from typing import Union, List

class TextBar:
  _LENGTH = 80
  def __init__(self):
    pass

  def __str__(self):
    return '-' * TextBar._LENGTH


class SysCode:
  ok = 0


class Util:
  def __init__(self, name, version=None, path=None):
    self.name = name
    self.version = version
    self.path = path

  def __str__(self):
    return f'name: {self.name}, version: {self.version}, path: {self.path}'


class Version:
  _pattern = re.compile(r'(\d){1,3}\.(\d){1,3}(\.(\d){1,3})?')

  @classmethod
  def extract_version_from(cls, text):
    match = Version._pattern.search(text)
    return match.group(0) if match else None


def get_version(util_name: str) -> Union[str, None]:
  variants = ['--version', 'version', '-V', '-v']

  for version_query in variants:
    process = subprocess.run(f'{util_name} {version_query}',
                             shell=True,
                             capture_output=True,
                             text=True)

    text = process.stdout.replace('\n', ' ')
    version = Version.extract_version_from(text)
    if version:
      return version

  # return None if nothing has been found
  return None

def set_util_path(util: Util):
  process = subprocess.run(f'which {util.name}',
                           shell=True,
                           capture_output=True,
                           text=True)

  if process.returncode == SysCode.ok:
    util.path = process.stdout.rstrip()
  else:
    raise ScmError(f'cannot get path of {util.name}\n {process.stderr}')


class Block:
  def __init__(self, writer):
    self.writer = writer

  def __enter__(self):
    self.writer.mv_right()

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.writer.mv_left()

  def __call__(self, line):
    self.writer(line)


class Writer:
  def __init__(self, indent_factor=2):
    self.factor = indent_factor
    self.curr_indent = 0
    self.text = []

  def __enter__(self):
    self.text = []

  def __exit__(self, exc_type, exc_val, exc_tb):
    pass

  def __call__(self, line):
    ws = (' ' * self.factor) * self.curr_indent
    self.text.append(f'{ws}{line}')

  def mv_left(self):
    self.curr_indent -= 1

  def mv_right(self):
    self.curr_indent += 1

  def block(self):
    return Block(writer=self)



class Decorator:
  def __init__(self,
               with_header=False,
               are_buildable=False,
               indent_factor=2):
    self.with_header = with_header
    self.are_buildable = are_buildable
    self.writer = Writer(indent_factor)

  def produce(self, utils: List[Util]):

    if self.with_header:
      self.writer('packages:')
      self.writer.mv_right()

    for util in utils:
      self.writer(f'{util.name}:')

      with self.writer.block():
        self.writer(f'buildable: {Decorator.bool_as_str(self.are_buildable)}')
        self.writer(f'externals:')
        self.writer(f'- spec: {util.name}@{util.version}')

        with self.writer.block():
          self.writer(f'prefix: {dirname(dirname(util.path))}')

  @classmethod
  def bool_as_str(cls, is_true: bool):
    return 'true' if is_true else 'false'