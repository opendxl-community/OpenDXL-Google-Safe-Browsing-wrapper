# OpenDXL Google Safe Browsing wrapper


## Intro
[Google Safe Browsing](https://developers.google.com/safe-browsing/) checks URLs against Google's constantly updated lists of unsafe web resources. For example it can find social engineering sites (phishing and deceptive sites) and sites that host malware or unwanted software. Any URL found on a Safe Browsing list is considered unsafe.
The API lets your client applications send URLs within a HTTP POST to the Google Safe Browsing server to check their status. 

This project focuses on an OpenDXL wrapper for the Google Safe Browsing API.

![Alt text](https://cloud.githubusercontent.com/assets/24607076/24956848/7687e3ee-1f81-11e7-9b9a-2c3105532155.png "Structure")


## Setup

#### McAfee OpenDXL

https://www.mcafee.com/us/developers/open-dxl/index.aspx

1. Python SDK Installation [link](https://opendxl.github.io/opendxl-client-python/pydoc/installation.html)
2. Certificate Files Creation [link](https://opendxl.github.io/opendxl-client-python/pydoc/certcreation.html)
3. ePO Certificate Authority (CA) Import [link](https://opendxl.github.io/opendxl-client-python/pydoc/epocaimport.html)
4. ePO Broker Certificates Export  [link](https://opendxl.github.io/opendxl-client-python/pydoc/epobrokercertsexport.html)

#### edit the dxl.conf
```clj
[Certs]
BrokerCertChain=certs/brokercert.crt
CertFile=certs/client.crt
PrivateKey=certs/client.key

[Brokers]
{}={};8883;
```
#### Safe Browsing API service

To use the Lookup API you need a [Google Account](https://accounts.google.com/SignUp), a [Google Developer Console project](https://support.google.com/cloud/answer/6251787?hl=en), and an [API key](https://support.google.com/cloud/answer/6158862?hl=en&ref_topic=6262490). You also need to [activate](https://support.google.com/cloud/answer/6158841?hl=en) the Safe Browsing APIs for use with this project.


Define the **GOOGLE_SAFE_BROWSING_API_KEY** variable inside the **service.py** script.

```
GOOGLE_SAFE_BROWSING_API_KEY = ''
```
#### DXL TOPIC
Set the variables SERVICE_INPUT and TOPIC_INPUT
```clj
SERVICE_INPUT = "/reputation"
TOPIC_INPUT = SERVICE_INPUT + "/googlesafebrowsing"
```
  
## Instructions
 
1.  run the service
 
>python service.py


2.  run the client specifying the TOPIC and the destination PAYLOAD

>python client.py -t /reputation/googlesafebrowsing -p www.google.com

#### Results are shown as follows:

>python client.py -t /reputation/googlesafebrowsing -p www.google.com
result is coming:

{'safe'}


>python client.py -t /reputation/googlesafebrowsing -p www.----.info/errorreport/ty5ug6h4ndma4/
result is coming:

{u'matches': [{u'threatType': u'SOCIAL_ENGINEERING', u'threatEntryType': u'URL', u'platformType': u'ANY_PLATFORM', u'threat': {u'url': u'www.----.info/errorreport/ty5ug6h4ndma4/'}, u'cacheDuration': u'300s'}]}

