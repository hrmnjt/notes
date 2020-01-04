# Documentation

TODO: update the Documentation to point to generated docs and add better details

## Important links

- [reStructured Text User Documentation](https://docutils.sourceforge.io/rst.html)
- [Python documentation guidelines](https://devguide.python.org/documenting/#style-guide)
- [Sphinx reStructured Text Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)


## Command reference

Make commands to be run from project root directory

```bash
# If you updated the python code - generate module documentation
sphinx-apidoc -f -o source/ ../.

# Regenerate all docs
make html

# Clean regenerate in single step - suggested only in case of major changes
make cleanhtml
```
