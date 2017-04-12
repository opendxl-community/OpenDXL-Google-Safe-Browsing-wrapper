# The API key for invoking the Google Safe Browsing service
#_______________________________________________________________________________________
GOOGLE_SAFE_BROWSING_API_KEY = ''
#_______________________________________________________________________________________

GOOGLE_SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + GOOGLE_SAFE_BROWSING_API_KEY

SERVICE_INPUT = "/reputation"
TOPIC_INPUT = SERVICE_INPUT + "/googlesafebrowsing"

import time
import logging
import os
import requests
import json

from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
config = DxlClientConfig.create_dxl_config_from_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dxl.conf'))

from dxlclient.message import ErrorResponse, Response

from dxlclient.callbacks import RequestCallback
from dxlclient.service import ServiceRegistrationInfo


def is_safe(URL):
	headers = {'content-type': 'application/json'}
	payload = {'client': {'clientId': "dxlclient", 'clientVersion': "1.0"},
        'threatInfo': {'threatTypes':  ['THREAT_TYPE_UNSPECIFIED',
                                'MALWARE',
                                'SOCIAL_ENGINEERING',
                                'UNWANTED_SOFTWARE',
                                'POTENTIALLY_HARMFUL_APPLICATION'],
                       'platformTypes': ["ANY_PLATFORM"],
                        'threatEntryTypes': ['THREAT_ENTRY_TYPE_UNSPECIFIED',
                                     'URL',
                                     'EXECUTABLE',
                                     'IP_RANGE'],
                       'threatEntries': [{'url': URL }]}}


	r = requests.post(GOOGLE_SAFE_BROWSING_URL, data=json.dumps(payload), headers=headers)
	if not r.json():
		 return "{'safe'}"
	else:
		return r.json()

# Enable logging, this will also direct built-in DXL log messages.
log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

# Configure local logger
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

def jsonparse(message):
#suppose the message coming is like {"PAYLOAD": "x.y.z.t", "SRC_HOST": "server_name"}
    filtered = json.loads(message)
    return str(filtered['PAYLOAD'])


with DxlClient(config) as client:

    client.connect()   
    class DxlService(RequestCallback):
        def on_request(self, request):
            try:
                query = request.payload.decode()
                logger.info("Service received request payload: " + query)
                response = Response(request)
                response.payload = str(is_safe(jsonparse(query))).encode()
                client.send_response(response)
                print response

            except Exception as ex:
                print str(ex)
                client.send_response(ErrorResponse(request, error_message=str(ex).encode()))

    info = ServiceRegistrationInfo(client, SERVICE_INPUT)
    info.add_topic(TOPIC_INPUT, DxlService())
    # Register the service with the fabric (wait up to 10 seconds for registration to complete)
    client.register_service_sync(info, 10)
    logger.info("Service is running on topic: " + TOPIC_INPUT)

    # Wait forever
    while True:
    	time.sleep(60)



