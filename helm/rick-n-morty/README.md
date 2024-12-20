----

### Directory Structure
---
```console
helm
└── rick-n-morty
    ├── Chart.yaml
    ├── templates
    │   ├── _helpers.tpl
    │   ├── deployment.yaml
    │   ├── ingress.yaml
    │   └── service.yaml
    └── values.yaml
```

### Overview
---
This directory contains a Helm chart for deploying a Rick and Morty API application to a Kubernetes cluster. It includes templates for deployment, ingress, and service resources, along with customizable values in the values.yaml file.

### Requirements
---
- Clone the [r-m-k8s-pipeline](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline) project repository.
- Helm installed.
- Kubernetes cluster context configured.

### Description
---
We are deploying a Kubernetes-based application that interacts with the Rick and Morty API. The application provides routes for retrieving character data, health checks, and downloading CSVs. Using Helm, this setup ensures a scalable and configurable deployment, supporting both LoadBalancer services and Ingress routing.

### Installation
---

1. Navigate to the Helm directory:
	```sh
	cd r-m-api-k8s-pipline/helm/rick-n-morty/ 
	```

2. Install the Chart:
	```sh
	helm install rick-n-morty .
	```
	The `helm install` command will complete the following:
	- Install the Chart with the release name : `rick-n-morty`
	- Create a Deployment with 2 replicas.
	- Create the Ingress resource.
	- Create a LoadBalancer Service.

3. Check the resources:
	```sh
	kubectl get deployments
	kubectl get svc
	kubectl get ingress
	```

	**Expected result:**
```output
$ kubectl get deployments
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
rick-n-morty-rick-n-morty   2/2     2            2           158m
```

```output
$ kubectl get svc
NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes                  ClusterIP      10.96.0.1       <none>        443/TCP        15d
rick-n-morty-rick-n-morty   LoadBalancer   10.103.2.161    10.0.1.201    80:31954/TCP   160m
rick-n-morty-svc            LoadBalancer   10.109.73.120   10.0.1.200    80:30877/TCP   3d2h
```
>[!note]
>Take note of the external IPs
>In this case:
>- `10.0.1.201`
>- `10.0.1.200`


```output
$ kubectl get ingress
NAME                        CLASS    HOSTS                ADDRESS   PORTS   AGE
rick-n-morty-ingress        <none>   rick-n-morty.local             80      3d2h
rick-n-morty-rick-n-morty   <none>   rick-n-morty.local             80      160m           80      160m
```

4. Use the external IPs to test the connection to the application using the `curl` command:
	```sh
	curl http://<EXTERNAL_IP>/<URL>
	```

	**Routes:**
	- **``/characters_data``**: Returns a JSON list of characters.
	  
	- **``/healthcheck``**: Returns a JSON object with health check results.
	  
	- **``/download``:** Downloads a CSV file with character information.

	Examples:
		**``$ curl http://10.0.1.201/characters_data``:**
	```json
	[
	  {
	    "Image": "https://rickandmortyapi.com/api/character/avatar/3.jpeg",
	    "Location": "Earth (Replacement Dimension)",
	    "Name": "Summer Smith"
	  },
	  {
	    "Image": "https://rickandmortyapi.com/api/character/avatar/4.jpeg",
	    "Location": "Earth (Replacement Dimension)",
	    "Name": "Beth Smith"
	  },
	  {
	    "Image": "https://rickandmortyapi.com/api/character/avatar/5.jpeg",
	    "Location": "Earth (Replacement Dimension)",
	    "Name": "Jerry Smith"
	  },
	  ...
	```
	 
	 **``$ curl http://10.0.1.201/healthcheck:``**
	```json
	{
	  "Health Checks": [
	    {
	      "Message": "API healthchecks passed successfully.",
	      "Status": "PASSED",
	      "Status code": "200",
	      "Timestamp": "2024-12-10 19:21:53"
	    }
	  ]
	}
	```
	
	**`$ curl http://10.0.1.201/download`:**
```csv
Name,Location,Image
Summer Smith,Earth (Replacement Dimension),https://rickandmortyapi.com/api/character/avatar/3.jpeg
Beth Smith,Earth (Replacement Dimension),https://rickandmortyapi.com/api/character/avatar/4.jpeg
Jerry Smith,Earth (Replacement Dimension),https://rickandmortyapi.com/api/character/avatar/5.jpeg
Beth Sanchez,Earth (C-500A),https://rickandmortyapi.com/api/character/avatar/37.jpeg
Beth Smith,Earth (C-137),https://rickandmortyapi.com/api/character/avatar/38.jpeg
Beth Smith,Earth (Evil Rick's Target Dimension),https://rickandmortyapi.com/api/character/avatar/39.jpeg
Bill,Earth (C-137),https://rickandmortyapi.com/api/character/avatar/45.jpeg	
...
```

5. Ensure `rick-n-morty.local` resolves to the Ingress IP by adding this to /etc/hosts:
	```sh
	echo "<INGRESS_IP> rick-n-morty.local" | sudo tee -a /etc/hosts
	```

	 **Test `rick-n-morty.local` with the `curl` command:**

	```sh
	curl http://rick-n-morty.local/download
	curl http://rick-n-morty.local/characters_data
	curl http://rick-n-morty.local/healthcheck
	```
	**You should get the same results in the previous step.**

### Customizing Values
---
You can modify the values.yaml file to change:

- `replicaCount`: Number of application replicas.
- `image.repository`, `image.tag`: Docker image and tag.
- `service.type`, `service.port`, `service.targetPort`: Service type and ports.
- `ingress.enabled`, `ingress.host`, `ingress.className`: Ingress configuration.

For example, to override values without editing the file directly:
```shell
helm install my-release . --set replicaCount=3 --set ingress.enabled=false
```