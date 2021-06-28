import websocket
import ssl
import json
import pathlib


headers = {'X-Qlik-User':  'UserDirectory=internal; UserId=sa_engine'}

sslopt = {  # Exported pem!!!(not for Windows) certificates from Qlik
'check_hostname': True,
'keyfile': 'client_key.pem',
'certfile': 'client.pem',
'ca_certs': 'root.pem'}



wss = websocket.create_connection("wss://?????.?????.??:4747/app/", sslopt=sslopt, header=headers) # necessarily full domain name, with IP not work

print("connect")
print(wss.recv())

wss.send(json.dumps({
    "jsonrpc": "2.0",
    "id": 1,
    "method": "GetDocList",
    "handle": -1,
    "params": []
}))

print("receiving list")
print(wss.recv())

wss.send(json.dumps({
    "method": "OpenDoc",
    "handle": -1,
    "params": [
        "???????" #qDocId from previous print
    ],
    "outKey": -1,
    "id": 2
}))

print("open doc")
print(wss.recv())

wss.send(json.dumps({
    "handle": 1,
    "method": "DoReloadEx",
    "params": [{"qMode": 0}],
    "outKey": -1,
    "id": 3
}))
if """"qSuccess":true""" in wss.recv():
    print("do Reload OK")
else:
    print("ERROR")


wss.send(json.dumps({
    "handle": 1,
    "method": "GetScript",
    "params": {},
    "outKey": -1,
    "id": 3
}))

print("get script")
print(wss.recv())

wss.close()