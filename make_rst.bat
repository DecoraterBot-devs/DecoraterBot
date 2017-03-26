@echo off
pandoc --from=markdown --to=rst --output=README.rst README.rst.in
pandoc --from=markdown --to=rst --output=Commands.rst Commands.rst.in
pandoc --from=markdown --to=rst --output=VoiceCommands.rst VoiceCommands.rst.in
pandoc --from=markdown --to=rst --output=UsedEvents.rst UsedEvents.rst.in
pandoc --from=markdown --to=rst --output=Plugins.rst Plugins.rst.in
