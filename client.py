import requests
import time
url = input("Enter url you want to REQUEST:\n")
type_of_request = "0"
while (type_of_request != "3"):

    type_of_request = input("Enter 1 for GET \n2 for POST \n3 to exit\n")

    if type_of_request == "1":
        try:
            print("entrou")
            get = requests.get('{}tasks/gTask'.format(url))
            print("GET response:")
            print(get.text) 
            time.sleep(2)    
        except:
            print("url is not valid, remeber to insert http://")
            type_of_request ="3"
            
    elif type_of_request == "2":
        try:
            post1 = requests.post('{}tasks/pTask'.format(url),data = {'title':'FINALIZAÇÃO','pub_date':'2020-12-01T16:22:54Z','description':'final'})
            print("POST 1 response code: {} \n".format(post1.status_code))
            time.sleep(2)    
        except:
            print("url is not valid, remeber to insert http://")
            type_of_request ="3"

    if type_of_request == "3":
        print("Client shuting down...")



