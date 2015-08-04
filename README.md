Cary_pandoccommand
-------------------

A simple cary command to run the unix `pandoc` command.  Obviously
you need pandoc installed on your system.  At the moment this simply
converts the attached markdown file into html, docx, epub, and pdf
formats and mails them back (in the future I will try to handle
attachments, command-line options, etc).

Configuration
-------------

In your configuration (usually a `local_conf.py` file), have the following:

```
PANDOC_CONFIG = dict(PANDOC_PATH='/path/to/pandoc/command',
                     TEXLIVE_PATH='/path/to/texlive/executables')
from cary_pandoccommand import PandocCommand
COMMANDS = {..."pandoc": (PandocCommand, PANDOC_CONFIG)...}
```
