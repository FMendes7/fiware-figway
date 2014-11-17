# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
# 
# This file is part of FIGWAY software (a set of tools for FIWARE Orion ContextBroker and IDAS2.6).
#
# FIGWAY is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as 
# published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
# FIGWAY is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with FIGWARE. 
# If not, see http://www.gnu.org/licenses/
#
# For those usages not covered by the GNU Affero General Public License please contact with: Carlos Ralli Ucendo [ralli@tid.es] 
# Developed by Carlos Ralli Ucendo (@carlosralli), Nov 2014.


import requests, json
import ConfigParser
import io
import sys

CONFIG_FILE = "../config.ini"

NUM_ARG=len(sys.argv)
COMMAND=sys.argv[0] 

if NUM_ARG==2:
   MODEL=sys.argv[1]
else:
   print 'Usage: '+COMMAND+' [MODEL] '
   print '  Example of MODEL: SENSOR_TEMP'
   sys.exit(2)


# Load the configuration file
with open(CONFIG_FILE,'r+') as f:
    sample_config = f.read()
config = ConfigParser.RawConfigParser(allow_no_value=True)
config.readfp(io.BytesIO(sample_config))

IDAS_HOST=config.get('idas', 'host')
IDAS_ADMIN_PORT=config.get('idas', 'adminport')
IDAS_UL20_PORT=config.get('idas', 'ul20port')
IDAS_AAA=config.get('idas', 'OAuth')
if IDAS_AAA == "yes":
   TOKEN=config.get('user', 'token')
else:
   TOKEN="NULL"
f.close()

IDAS_URL = "http://"+IDAS_HOST+":"+IDAS_ADMIN_PORT

HEADERS = {'content-type': 'application/json' , 'X-Auth-Token' : TOKEN}

URL = IDAS_URL + '/m2m/v2/services/OpenIoT/models/'+MODEL

print "* Asking to "+URL
print "* Headers: "+str(HEADERS)
print "..."
r = requests.get(URL, headers=HEADERS)
print 
print "* Status Code: "+str(r.status_code)

print json.dumps(json.loads(r.text), indent=4)
print