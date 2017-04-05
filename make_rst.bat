@echo off
pandoc --from=markdown --to=rst --output=README.rst README.rst.in
pandoc --from=markdown --to=rst --output=Plugins.rst Plugins.rst.in
