the order of applying kubernetes manifests:  
1. Set proper settings
```
minikube addons enable ingress
```
2. Apply all secrets
```
kubectl apply -f .\kubernetes-app\secrets\
```
2. Apply deploy and service of databases
```
kubectl apply -f .\kubernetes-app\mongo-db\
kubectl apply -f .\kubernetes-app\postgres\
```
3. Take a cup of coffee and wait while databases are filling
4. Wait a little bit longer  
You can check the completeion by logs  
For PostgreSQL it will be smth like this:  
```
PostgreSQL init process complete; ready for start up.
database system is ready to accept connections
```  
For MongoDB it should be smth like this:
```
{"t":{"$date":"2023-12-16T16:06:48.074+00:00"},"s":"I",  "c":"NETWORK",  "id":23016,   "ctx":"listener","msg":"Waiting for connections","attr":{"port":27017,"ssl":"off"}}
```
5. Apply deploy and service of another microservices
```
kubectl apply -f .\kubernetes-app\flask\   
kubectl apply -f .\kubernetes-app\connector\
```
6. In the end apply ingress
```
kubectl apply -f .\kubernetes-app\ingresses\
```
7. make a tunnel to kubernetes
```
minikube tunnel
```
Further optimizations and improvements
- If you want to add basic authorizarion you need to apply new conf in ingress
- make an .htpassw file with your login/password
- create a secret file
- uncomment strings in ingress file
- apply new configuration  
A secret for "admin" "verysecret" is created and you applied it when applied secrets, so you just need to execute last two steps
