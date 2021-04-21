from scm.file_manip import *
from scm.components import *
from os.path import expanduser
from os.path import join as join_path
import argparse


def main():
  parser = argparse.ArgumentParser(description='find default packages for spack')
  parser.add_argument('-f', '--file', type=str, help="input file")
  parser.add_argument('-b', '--buildable', action='store_true', help="denote as buildable")
  parser.add_argument('-H', '--header', action='store_true', help="decorate with `packages:` at the top")
  parser.add_argument('-v', '--verbose', action='store_true', help="verbose information")
  parser.add_argument('-i', '--indent', type=int, default=2, help="newline indent of yaml format")
  args = parser.parse_args()

  spec_file = args.file
  if not args.file:
    spec_file = join_path(expanduser('~'), '.spack/scm-spec.yaml')
  package_list = get_packages_from_file(spec_file)

  if args.verbose:
    print(f'# requested packages: {len(package_list)}')
    for i, item in enumerate(package_list):
      print(f'  {i}) {item}')
    print(TextBar())


  utils: List[Util] = []
  skipped_packages = []
  for package_name in package_list:
    version = get_version(package_name)
    if version:
      utils.append(Util(package_name, version))
    else:
      skipped_packages.append(package_name)

  if args.verbose:
    print(f'# skipped packages: {len(skipped_packages)}')
    for i, item in enumerate(skipped_packages):
      print(f'  {i}) {item}')
    print(TextBar())


  for util in utils:
    set_util_path(util)


  for util in utils:
    if util.name in ['python2', 'python3']:
      util.name = 'python'    

  dec = Decorator(with_header=args.header,
                  are_buildable=args.buildable,
                  indent_factor=args.indent)

  dec.produce(utils)
  for line in dec.writer.text:
    print(line)


if __name__ == '__main__':
  main()
