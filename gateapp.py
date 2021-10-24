import sys
import requests

print("Contacting server ...")
if len(sys.argv) < 1:
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
    success=0
    if int(resp) == 1 :
        print("The secret is valid for this gate")
        while success != 1 :
            code = input("type the user code:")
            id = input("type the iser id:")
            print("Connecting Server ...")
            body = {
                'id':str(id),
                'code':str(code)
            }
            resp = requests.get("http://localhost:8008/gates/code",json=body)
            resp = resp.json()
            resp = resp['SUCCESS']
            if int(resp) == 1 :
                success = 1
                print("!!! Code Valid !!!")
                print("!!! The gate will cose in 5 s !!!")
            else:
                print("!!! Code Not Valid !!!")

    else:
        print("The secret is not valid for this gate")
        print("Exiting....")



