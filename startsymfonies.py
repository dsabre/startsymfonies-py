import os, sys, socket, pprint
from subprocess import call

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

# check if config.ini exists
configFile = os.path.dirname(os.path.abspath(__file__)) + '/config.ini'
Config = ConfigParser()
if not os.path.isfile(configFile):
	config = open(configFile, 'w')
	Config.add_section('config')
	Config.set('config', 'dir', 'INSER_HERE_YOUR_PATH')
	Config.set('config', 'htmlFilename', '/tmp/symfonies.html')
	Config.set('config', 'htmlTitle', 'Active Symfonies')
	Config.write(config)
	config.close()
	print 'Config file not found, no problem, we have now created that for you! ;)\nOpen ' + configFile + ' and set your directory to scan.'
	sys.exit()

# read configuration
Config.read(configFile)

# get directory to scan
dir = Config.get('config', 'dir')

# check for valid directory
if not os.path.isdir(dir):
	print 'Invalid directory ' + dir
	sys.exit()

publicIp = socket.gethostbyname(socket.gethostname())
localIp = "127.0.0."
finalLocalIp = 1
publicPort = 8000
symfonies = []
htmlFilename = Config.get('config', 'htmlfilename')
htmlTitle = Config.get('config', 'htmltitle')

# cycle over directory for find all symfonies
for dirname, dirnames, filenames in os.walk(dir):
	fname = dirname + '/app/console'
	if os.path.isfile(fname):
		# start symfony in private address
		address = localIp + str(finalLocalIp)
		call(["php", fname, "server:start", address])
		
		# start symfony in public path
		call(["php", fname, "server:start", publicIp, "-p", str(publicPort)])
		
		symfonies.append({
			'dirname': dirname,
			'address': address,
			'publicPort': publicPort
		})
		
		finalLocalIp += 1
		publicPort += 1

# creation of menu html file
if symfonies:
	target = open(htmlFilename, 'w')
	
	target.writelines([
		'<!DOCTYPE html>\n',
		'<html lang="en">\n',
		'<head>\n',
		'\t<meta charset="utf-8">\n',
		'\t<meta http-equiv="X-UA-Compatible" content="IE=edge">\n',
		'\t<meta name="viewport" content="width=device-width, initial-scale=1">\n',
		'\t<title>' + htmlTitle + '</title>\n',
		'\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">\n',
		'</head>\n',
		'<body>\n',
		'\t<div class="container-fluid">\n',
		'\t<h1>' + htmlTitle + '</h1>\n',
		'\t<div class="table-responsive">\n',
		'\t\t<table class="table table-bordered table-hover">\n',
		'\t\t\t<tr>\n',
		'\t\t\t\t<th>Path</th>\n',
		'\t\t\t\t<th>Private link</th>\n',
		'\t\t\t\t<th>Public link</th>\n',
		'\t\t\t</tr>\n'
	]);
	
	for symfony in symfonies:
		privateAddress = 'http://' + symfony['address'] + ':8000'
		publicAddress = 'http://' + publicIp + ':' + str(symfony['publicPort'])
		
		target.write('\t\t\t<tr>\n')
		target.write('\t\t\t\t<td>' + symfony['dirname'] + '</td>\n')
		target.write('\t\t\t\t<td><a href="' + privateAddress + '">' + privateAddress + '</a></td>\n')
		target.write('\t\t\t\t<td><a href="' + publicAddress + '">' + publicAddress + '</a></td>\n')
		target.write('\t\t\t</tr>\n')
	
	target.writelines([
		'\t\t</table>\n',
		'\t\t</div>\n',
		'\t</div>\n',
		'\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n',
		'\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>\n',
		'</body>\n',
		'</html>'
	]);
	
	target.close()
	
	# launch default browser with html menu file
	call(['gnome-open', "file://" + htmlFilename])
