import requests
print("Connecting Server ...")
resp = requests.get("http://localhost:8008/user/85229/code")
if resp.json() :
    print(">>>",int(resp.json()),"<<<")
    print("Type code in gate !!!")
else:
    print("!!! No Code !!!\n Internal Error \n Try Again")