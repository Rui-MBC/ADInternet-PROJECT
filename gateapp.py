import sys
import requests

print("Contacting server ...")
if sys.argv != 3:
    print("Inavlid number of arguments")
else:
    id = sys.argv[1]
    secret = sys.argv[2]
    body = {
        'id':str(id),
        'secret':str(secret)
    }
    resp = requests.get("http://localhost:8008/gates/id",json=body)
    resp = resp.json()
    resp = resp['SUCCESS']
    if int(resp) == 1 :
        print("The secret is valid for this gate")
        code = input("type the user code:")
        body = {
            'code':str(code)
        }
        resp = requests.get("http://localhost:8008/gates/code",json=body)
    else:
        print("The secret is not valid for this gate")
        print("Exiting....")



