### Spack-Complete-Me (scm)
This script is intend to help you to accelerate an installation process of HPC packages with Spack. 

Spack is a great tool but installing packages can take too long especially when you are working on a system which has not been pre-configured: your personal computer, laptop or you are building Docker or Singularity images. A typical HPC package is build on top of some libraries, these libraries depends on others and so on. Moreover, a library or a package can depend on a building tool or tools. All of these can result in a huge building tree which Spack is going to install/compile from sources. However, a decent Linux distribution may have versions of low-level packages (building dependencies) which could be ok for your purposes i.e., `autoconf`, `automake`, `pkg-config`, `m4`, `tar`, etc. 

You can list all building dependencies that your typical installation needs in a simple yaml file and provide it as an input to the script. The script will try to find these packages, their version and installation paths. The results will be printed on stdout which can be redirected to `~/.spack/packages.yaml`.

It is good to remember that once you add a package to `~/.spack/packages.yaml` as `buildable: False` you impose some constrains on your destination library or packages. Sometimes it can result in unsuccessful builds. Therefore, please, be careful while using this option.

#### Installation
```console
git clone 
cd  spack-complete-me
pip install -e .
```


#### Usage
To just print discovered packages to `stdout`
```console
python scm -f <path>/scm-spec.yaml 
```

To build Docker/Singularity images with Spack
 or when Spack is firstly installed on a system
```
python scm -f <path>/scm-spec.yaml -H > /.spack/packages.yaml
```

To populate an existing `packages.yaml` file with some packages
```
python scm -f <path>/scm-spec.yaml >> /.spack/packages.yaml
```

if an input file is not provided `scm` will try to read one
in `$HOME/.spack/scm-spec.yaml`


| Options             | Descriptions                          |
|---------------------|---------------------------------------|
| '-f', '--file'      | path to an input yaml file            |
| '-b', '--buildable' | denotes found packages as `buildable` |
| '-H', '--header'    | prepends output with `packages:` line |
| '-v', '--verbose'   | prints some debug information         |
| '-i', '--indent'    | indent width (default is 2            |

#### Input file structure:
```
spec:
  - tar
  - automake
  - autoconf
  - python3
  - m4
  - xz
  - go
```

#### 
