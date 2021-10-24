import sys
import requests

print("Contacting server ...")
if len(sys.argv) < 1:
    print("Inavlid number of arguments")
else:
    try:
        gate_id = sys.argv[1]
    except:
        print("Error getting ID !!!")
        exit()
    
    try:
        secret = sys.argv[2]
    except:
        print("Error getting secret !!!")
        exit()

    body = {
        'id':gate_id,
        'secret':str(secret)
    }
    try:
        resp = requests.get("http://localhost:8008/gates/id",json=body)
    except:
        print('Couldn´t access server')
        exit()

    resp = resp.json()
    resp_code = resp['errorCode']

    success=0
    if resp_code == 0 :
        print("The secret is valid for this gate")
        while success != 1 :
            code = input("type the user code:")
            id = 1111 #input("type the user id:(1111)")
            print("Connecting Server ...")
            body = {
                'id':str(id),
                'code':str(code),
                'gate_id':gate_id
            }
            try:
                resp = requests.get("http://localhost:8008/gates/code",json=body)
            except:
                print('Couldn´t access server')
                exit()
            resp = resp.json()
            errorCode = resp['errorCode']
            if errorCode == 0:
                success = 1
                print("!!! Code Valid !!!")
                print("!!! The gate will cose in 5 s !!!")
            else:
                print(resp['errorDescription'])

    else:
        print(resp['errorDescription'])
        print("Exiting....")



