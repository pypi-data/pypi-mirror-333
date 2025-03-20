from typing_extensions import Final
import json
from semantic.common.utils import msg


'''
    set batch_size to ~samples/sec 

'''

batch_size = 100

schemaName: str = 'fera' 
schemaVersion: str = 'v001'
instanceName: str = 'jan2025'
dbUri: str = 'http://127.0.0.1:6363/'

brokerIp: Final = 'localhost'
port: Final = 1883
username: Final = 'semantic'
password: Final = 's3mant1c'
publishTopic: Final = 'fcs/serviceRequestTopic'
insertAcknowledgeTopic: Final = 'insertAcknowledgeTopic'

semanticConfigTopic: Final ='fcs/semanticConfig'
semanticConfigResponseTopic: Final ='fcs/semanticConfigResponse'
serviceRequestTopic: Final ='fcs/serviceRequestTopic'
serviceResponseTopic: Final ='fcs/serviceResponseTopic'
topics: Final = [semanticConfigResponseTopic, serviceResponseTopic]



