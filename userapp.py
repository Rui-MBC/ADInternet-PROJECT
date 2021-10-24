import requests

print("Connecting Server ...")
#85229 is a simulated user id that would be enterd by the user when asking for a code
resp = requests.get("http://localhost:8008/users/85229/code")
if resp != None :
    print(">>>",int(resp.json()),"<<<")
    print("Type code in gate !!!")
else:
    print("!!! No Code !!!\n Internal Error \n Try Again")