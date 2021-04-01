import math
import random
import base64

def create_base_64_header(clientId, clientSecret):
    message = "{}:{}".format(clientId, clientSecret)
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')
    print('base64: ' + base64Message)
    return base64Message