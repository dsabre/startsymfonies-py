import os, datetime, sys, socket
from subprocess import call

year = str(datetime.datetime.now().year)
workDir = '/home/dsabre/Lavoro'
dir = workDir + '/git/' + year
publicIp = socket.gethostbyname(socket.gethostname())
ip = "127.0.0."
finalIp = 1
publicPort = 8000
symfonies = []
htmlFilename = '/tmp/symfonies.html'
htmlTitle = 'Active Symfonies'

# check for valid directory
if not os.path.isdir(dir):
	print 'Invalid directory ' + dir
	sys.exit()

# cycle over directory for find all symfonies
for dirname, dirnames, filenames in os.walk(dir):
	fname = dirname + '/app/console'
	if os.path.isfile(fname):
		# start symfony
		address = ip + str(finalIp)
		
		call(["php", fname, "server:start", address])
		call(["php", fname, "server:start", publicIp, "-p", str(publicPort)])
		
		finalIp += 1
		publicPort += 1
		
		symfonies.append({
			'dirname': dirname,
			'address': address,
			'publicPort': publicPort
		})

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
		'\t<table class="table table-bordered table-hover">\n',
		'\t\t<tr>\n',
		'\t\t\t<th>Path</th>\n',
		'\t\t\t<th>Private link</th>\n',
		'\t\t\t<th>Public link</th>\n',
		'\t\t</tr>\n'
	]);
	
	for symfony in symfonies:
		privateAddress = 'http://' + symfony['address'] + ':8000'
		publicAddress = 'http://' + publicIp + ':' + str(symfony['publicPort'])
		
		target.write('\t\t<tr>\n')
		target.write('\t\t\t<td>' + symfony['dirname'] + '</td>\n')
		target.write('\t\t\t<td><a href="' + privateAddress + '">' + privateAddress + '</a></td>\n')
		target.write('\t\t\t<td><a href="' + publicAddress + '">' + publicAddress + '</a></td>\n')
		target.write('\t\t</tr>\n')
	
	target.writelines([
		'\t</table>\n',
		'\t</div>\n',
		'\t<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>\n',
		'\t<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>\n',
		'</body>\n',
		'</html>'
	]);
	
	target.close()
	
	# launch default browser with html menu file
	call(['gnome-open', "file://" + htmlFilename])
