@echo off
pandoc --from=markdown --to=rst --output=description.rst description.rst.in
pandoc --from=rst --to=html --output=description.html description.rst
pandoc --from=markdown --to=rst --output=README.rst README.rst.in
