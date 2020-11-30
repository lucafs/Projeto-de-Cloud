import requests
# res=requests.post("http://18.216.171.179:8080/admin/auth/group/add/" , {'Name':"teste","permission"})

# res = requests.post('http://18.216.171.179:8080/admin')
# res = requests.post("http://18.216.171.179:8080/admin", auth=('cloud', 'cloud'))
# res = requests.post('http://18.216.171.179:8080/admin/login/?next=/admin/', {'USER': 'cloud', 'PASSWORD': 'cloud'})
res =requests.get("http://loadbalancerprojeto-653508327.us-east-2.elb.amazonaws.com/admin/login/?next=/admin/")
print(res)