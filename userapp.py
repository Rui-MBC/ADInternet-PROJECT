import requests

print("Connecting Server ...")
#1111 is a simulated user id that would be enterd by the user when asking for a code
try:
    resp = requests.get("http://localhost:8008/users/1111/code")
except:
    print("Couldn´t access server!!!")
    exit()

if resp != None :
    response = resp.json()
    error = response['errorCode']
    if error == 0:
        print(">>>",response['code'],"<<<")
        print("Type code in gate !!!")
    else:
        print(response['errorDescription'])
else:
    print("!!! No Code !!!\n Internal Error \n Try Again")