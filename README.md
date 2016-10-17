# StartSymfonies

Python program to launch all Symfony framework found in a specified directory.

## Usage

Can be used through the command line:
``` bash
python /your/path/startsymfonies/startsymfonies.py
```

### Options

- --start-only: bypass the preventive arrest of the
Symfonies, useful in the case of the computer just started
- --no-public: avoid to start the public interface
- --no-open: avoid browser auto-open

## Notes

The first run of the programm will be created a config.ini file with a few
options:
- **dir:** main directory to check symfonies (the program start here and
go for recursive)
- **skipdirs:** put here the directories (or a part of the names) to
skip
- **htmlfilename:** the path where the html generated file will be saved
- **htmltitle:** the title of the html page (h1)