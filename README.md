# vbml_core.py

This is the core implementation of the vbml text format as a python package.

## Install

I don't feel like making an official package right now, so the installation is
as follows:

**Step 1**: Make sure you have a custom `PYTHONPATH` and that it exists. For
example:
```shell
export PYTHONPATH=$PYTHONPATH:~/.local/lib/python_modules
```

**Step 2**: Use the makefile to symlink the library into that directory. This
only needs to be done once.
```shell
make autodetect # This should set the install directory.
make install
```

## Use

The package will be visible as `vbml_core`. A proper documentation is coming
soon.
