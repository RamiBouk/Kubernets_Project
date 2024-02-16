kubectl apply -f ./database/database-deployment.yaml
kubectl apply -f ./classifier/classifier-deployment.yaml
kubectl apply -f ./interface/interface-deployment.yaml
kubectl apply -f ./interface/interface-service.yaml
#kubectl apply -f ./load_balancer.yaml
