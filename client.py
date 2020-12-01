import requests
def client_req(url):
    post1 = requests.post('http://{}/tasks/pTask'.format(url),data = {'title':'FINALIZAÇÃO','pub_date':'2020-12-01T16:22:54Z','description':'final'})
    post2 = requests.post('http://{}/tasks/pTask'.format(url),data = {'title':'PROJETO','pub_date':'2020-12-12T16:22:54Z','description':'proj'})
    get = requests.get('http://{}/tasks/gTask'.format(url))
    print("POST 1 response code: {}".format(post1.status_code))
    print("POST 2 response code: {}".format(post2.status_code))
    print("GET response:")
    print(get.text)

client_req(input("Enter url you want to GET and POST:"))