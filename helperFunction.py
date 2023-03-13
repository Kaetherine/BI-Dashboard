from base64 import b64encode
import requests

def getJobID(refnr):
    code_bytes = bytes(refnr, 'utf-8')
    encoded_code = b64encode(code_bytes)
    return encoded_code.decode()


async def getJobInfo(url, headers):
    return requests.get(url, headers=headers).json()