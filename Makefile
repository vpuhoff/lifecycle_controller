check:
	helm install --dry-run lifecycle-controller  -f values.yaml .

install:
	helm install  -f values.yaml lifecycle-controller .

update:
	helm upgrade -f values.yaml lifecycle-controller .

change_param:
	helm upgrade dashboard-demo stable/kubernetes-dashboard --set fullnameOverride="kubernetes-dashboard" --reuse-values

create_secret:
	kubectl create secret generic docker-hub-token \
    --from-file=.dockerconfigjson=docker-config.json \
    --type=kubernetes.io/dockerconfigjson