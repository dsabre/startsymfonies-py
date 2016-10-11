# StartSymfonies

Python program to launch all Symfony framework found in a specified directory.

## Usage

Can be used through the command line:
``` bash
python /your/path/startsymfonies/startsymfonies.py
```

You can use the option `--start-only` to bypass the preventive arrest of the
Symfonies, useful in the case of the computer just started.

## Notes

The first run of the programm will be created a config.ini file with a few
options:
- **dir:** main directory to check symfonies (the program start here and
go for recursive)
- **skipdirs:** put here the directories (or a part of the names) to
skip
- **htmlfilename:** the path where the html generated file will be saved
 -**htmltitle:** the title of the html page (h1)