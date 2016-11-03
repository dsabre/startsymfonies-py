import os, sys, socket, getopt, pprint
from subprocess import call
from time import sleep
from datetime import date

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# check if config.ini exists
configFile = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
Config = ConfigParser()
if not os.path.isfile(configFile):
    config = open(configFile, 'w')
    Config.add_section('config')
    Config.set('config', 'dir', 'INSER_HERE_YOUR_PATH')
    Config.set('config', 'skipdirs', '')
    Config.set('config', 'htmlfilename', '/tmp/symfonies.html')
    Config.set('config', 'htmltitle', 'Active Symfonies')
    Config.write(config)
    config.close()
    print 'Config file not found, no problem, we have now created that for you! ;)\nOpen ' + configFile + ' and set your directory to scan.'
    sys.exit(1)

# permit opt --start-only to perform only the start of the symfonies
try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['start-only', 'no-public', 'no-open'])
    arrOpts = ()

    for opt in opts:
        arrOpts = arrOpts + opt

    startOnly = '--start-only' in arrOpts
    noPublic = '--no-public' in arrOpts
    noOpen = '--no-open' in arrOpts
except getopt.GetoptError:
    print 'Invalid argument'
    sys.exit(2)
except IndexError:
    startOnly = False
    noPublic = False
    noOpen = False

# read configuration
Config.read(configFile)

# get directory to scan
dir = Config.get('config', 'dir')

# check for valid directory
if not os.path.isdir(dir):
    print 'Invalid directory ' + dir
    sys.exit(3)

publicIp = socket.gethostbyname(socket.gethostname())
localIp = "127.0.0."
finalLocalIp = 1
publicPort = 8000
symfonies = []
htmlfilename = Config.get('config', 'htmlfilename')
htmltitle = Config.get('config', 'htmltitle')

# get dirs to skip
skipdirs = Config.get('config', 'skipdirs')
skipdirs = skipdirs.split(',') if skipdirs else None

# cycle over directory for find all symfonies
for dirname, dirnames, filenames in os.walk(dir):
    fname = dirname + '/app/console'
    if os.path.isfile(fname):
        skip = False

        if skipdirs:
            for i in skipdirs:
                if dirname.find(i) > -1:
                    skip = True

        symfonies.append({'dirname': dirname, 'skip': skip})

if symfonies:
    # order symfonies by dirname
    symfonies = sorted(symfonies, key=lambda symfony: symfony['dirname'])

    # creation of menu html file
    target = open(htmlfilename, 'w')

    target.writelines([
        '<!DOCTYPE html>\n',
        '<html lang="en">\n',
        '<head>\n',
        '\t<meta charset="utf-8">\n',
        '\t<meta http-equiv="X-UA-Compatible" content="IE=edge">\n',
        '\t<meta name="viewport" content="width=device-width, initial-scale=1">\n',
        '\t<title>' + htmltitle + '</title>\n',
        '\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">\n',
        '\t<link rel="stylesheet" href="https://bootswatch.com/superhero/bootstrap.min.css">\n',
        '\t<style>\n',
        '\t\ttable > thead > tr > th, .table > thead > tr > th, table > tbody > tr > th, .table > tbody > tr > th, table > tfoot > tr > th, .table > tfoot > tr > th, table > thead > tr > td, .table > thead > tr > td, table > tbody > tr > td, .table > tbody > tr > td, table > tfoot > tr > td, .table > tfoot > tr > td{\n',
        '\t\t\tborder-color: #4e5d6c !important;\n',
        '\t\t}\n',
        '\t</style>\n',
        '</head>\n',
        '<body>\n',
        '\t<nav class="navbar navbar-inverse">\n',
        '\t\t<div class="container">\n',
        '\t\t\t<div class="navbar-header">\n',
        '\t\t\t\t<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-2">\n',
        '\t\t\t\t\t<span class="sr-only">Toggle navigation</span>\n',
        '\t\t\t\t\t<span class="icon-bar"></span>\n',
        '\t\t\t\t\t<span class="icon-bar"></span>\n',
        '\t\t\t\t\t<span class="icon-bar"></span>\n',
        '\t\t\t\t</button>\n',
        '\t\t\t\t<a class="navbar-brand" href="#">' + htmltitle + '</a>\n',
        '\t\t\t</div>\n',
        '\t\t\t<div class="collapse navbar-collapse" id="bs-example-navbar-collapse-2">\n',
        '\t\t\t\t<ul class="nav navbar-nav">\n',
        '\t\t\t\t\t<li class="dropdown">\n',
        '\t\t\t\t\t\t<a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Utilities <span class="caret"></span></a>\n',
        '\t\t\t\t\t\t<ul class="dropdown-menu" role="menu">\n',
        '\t\t\t\t\t\t\t<li><a href="https://symfony.com/doc/current/index.html" target="_blank">Symfony documentation</a></li>\n',
        '\t\t\t\t\t\t</ul>\n',
        '\t\t\t\t\t</li>\n',
        '\t\t\t\t</ul>\n',
        '\t\t\t\t<form class="navbar-form navbar-right" role="search">\n',
        '\t\t\t\t\t<div class="form-group">\n',
        '\t\t\t\t\t\t<input class="form-control" placeholder="Search" type="text" id="search">\n',
        '\t\t\t\t\t</div>\n',
        '\t\t\t\t\t<div class="checkbox">\n',
        '\t\t\t\t\t\t<label>\n',
        '\t\t\t\t\t\t\t<input id="flgHideSkipped" type="checkbox" checked> Hide skipped\n',
        '\t\t\t\t\t\t</label>\n',
        '\t\t\t\t\t</div>\n',
        '\t\t\t\t</form>\n',
        '\t\t\t</div>\n',
        '\t\t</div>\n',
        '\t</nav>\n',
        '\t<div class="container">\n',
        '\t\t<div class="table-responsive">\n',
        '\t\t\t<table class="table table-bordered table-hover table-responsive">\n',
        '\t\t\t\t<thead>\n',
        '\t\t\t\t\t<tr>\n',
        '\t\t\t\t\t\t<th class="text-center">Favicon</th>\n',
        '\t\t\t\t\t\t<th>Path</th>\n',
        '\t\t\t\t\t\t<th>Private link</th>\n',
        '\t\t\t\t\t\t<th>Public link</th>\n',
        '\t\t\t\t\t\t<th class="text-center">Status</th>\n',
        '\t\t\t\t\t</tr>\n'
        '\t\t\t\t</thead>\n'
        '\t\t\t\t<tbody>\n'
    ])

    # cycle over directory for find all symfonies
    i = 1
    count = str(len(symfonies))
    for infoSymfony in symfonies:
        symfony = infoSymfony['dirname']

        stopped = False
        started = False
        skipped = infoSymfony['skip']
        privateAddress = ''
        publicAddress = ''

        print bcolors.HEADER + str(i) + '/' + count + bcolors.ENDC + ' ::: ' + symfony
        i += 1

        if not skipped:
            # define local address
            address = localIp + str(finalLocalIp)

            fname = symfony + '/app/console'

            if not startOnly:
                sys.stdout.write('STOP : ')

                # try to stop private and public symfony
                s1 = call(["php", fname, "-q", "server:stop", address])
                s2 = call(["php", fname, "-q", "server:stop", publicIp, "-p", str(publicPort)])

                # print operation status
                if s1 == 0 and s2 == 0:
                    print bcolors.OKGREEN + 'OK' + bcolors.ENDC
                    stopped = True
                else:
                    print bcolors.FAIL + 'KO' + bcolors.ENDC

                sys.stdout.write('START: ')

                sleep(1)
            else:
                sys.stdout.write('START: ')

            # try to start private and public symfony
            s1 = call(["php", fname, "-q", "server:start", address])

            if not noPublic:
                s2 = call(["php", fname, "-q", "server:start", publicIp, "-p", str(publicPort)])
            else:
                s2 = 0

            # print operation status
            if s1 == 0 and s2 == 0:
                print bcolors.OKGREEN + 'OK' + bcolors.ENDC
                started = True
            else:
                print bcolors.FAIL + 'KO' + bcolors.ENDC

            privateAddress = 'http://' + address + ':8000'
            publicAddress = 'http://' + publicIp + ':' + str(publicPort)

            finalLocalIp += 1
            publicPort += 1
        else:
            print 'SKIPPED'

        # get the status of the symfony
        if started:
            status = 'Active'
            bgClass = 'success'
        elif stopped:
            status = 'Stopped'
            bgClass = 'warning'
        elif skipped:
            status = 'Skipped'
            bgClass = 'info'
        else:
            status = 'Error'
            bgClass = 'danger'

        favicon = symfony + '/web/favicon.ico'

        target.write('\t\t\t\t\t<tr>\n')

        if os.path.isfile(favicon):
            target.write('\t\t\t\t\t\t<td class="text-center"><img src="' + favicon + '" alt="No favicon" width="16" /></td>\n')
        else:
            target.write('\t\t\t\t\t\t<td class="text-center">--</td>\n')

        target.write('\t\t\t\t\t\t<td>' + symfony + '</td>\n')
        target.write('\t\t\t\t\t\t<td><a href="' + privateAddress + '">' + privateAddress + '</a></td>\n')

        if not noPublic:
            target.write('\t\t\t\t\t\t<td><a href="' + publicAddress + '">' + publicAddress + '</a></td>\n')
        else:
            target.write('\t\t\t\t\t\t<td class="text-center">--</td>\n')

        target.write('\t\t\t\t\t\t<td class="col-status text-center bg-' + bgClass + '">' + status + '</td>\n')
        target.write('\t\t\t\t\t</tr>\n')

        print ''

    target.writelines([
        '\t\t\t\t</tbody>\n',
        '\t\t\t</table>\n',
        '\t\t</div>\n',
        '\t\t<p class="text-center text-muted"><small>Page generated automatically by StartSymfonies.<br>&copy; ' + str(date.today().year) + ' <a href="https://github.com/raniel86" target="_blank">raniel86</a></small></p>\n',
        '\t</div>\n',
        '\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n',
        '\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>\n',
        '\t<script type="text/javascript">\n',
        '\t\t$(function() {\n',
        '\t\t\tvar $rows = $("table tbody tr");\n',
        '\t\t\tmanageRows();\n',
        '\t\t\t$("#search").keyup(function() {\n',
        '\t\t\t\tmanageRows();\n',
        '\t\t\t});\n',
        '\t\t\t$("#flgHideSkipped").click(function() {\n',
        '\t\t\t\tmanageRows();\n',
        '\t\t\t});\n',
        '\t\t\tfunction manageRows(){\n',
        '\t\t\t\tvar string = $.trim($("#search").val()).replace(/ +/g, " ").toLowerCase();\n',
        '\t\t\t\tvar hideSkipped = $("#flgHideSkipped").is(":checked");\n',
        '\t\t\t\t$rows.show().filter(function() {\n',
        '\t\t\t\t\tvar text = $(this).text().replace(/\s+/g, " ").toLowerCase();\n',
        '\t\t\t\t\tvar status = $(this).children("td.col-status").text().replace(/\s+/g, " ").toLowerCase();\n',
        '\t\t\t\t\tvar checkString = string !== "" ? !~text.indexOf(string) : false;\n',
        '\t\t\t\t\tvar checkSkipped = hideSkipped ? ~status.indexOf("skipped") : false;\n',
        '\t\t\t\t\treturn checkString || checkSkipped;\n',
        '\t\t\t\t}).hide();\n',
        '\t\t\t}\n',
        '\t\t});\n',
        '\t</script>\n',
        '</body>\n',
        '</html>'
    ])

    target.close()

    # launch default browser with html menu file
    if not noOpen:
        call(['gnome-open', "file://" + htmlfilename])

sys.exit(0)
