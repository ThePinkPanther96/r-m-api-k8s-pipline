----
### Directory Structure
---
```console
k8s/
├── deployment.yaml
├── ingress.yaml
├── metallb-ipaddresspool.yaml
├── metallb-l2advertisement.yaml
└── service.yaml
```
### Overview
---
This repository includes Kubernetes manifests such as `Deployment.yaml`, `Service.yaml`, and `Ingress.yaml` for deploying a RESTful API application. The application retrieves and filters character data from an external API, exposing two main endpoints.
### Prerequisites
---
- A running Kubernetes cluster (e.g., Kubeadm, Minikube, etc).
- An ingress controller installed and configured (e.g., NGINX Ingress Controller).
- A load balancer solution (e.g., MetalLB) configured for external IP assignment in a bare-metal environment (e.g., EC2 instances).
- Ensure a required Docker image is accessible to the Kubernetes cluster, either by pushing it to a container registry or loading it directly into the cluster.
### Description
---
In this case, we are working with a Kubernetes cluster that uses Kubeadm on a bare-metal environment hosted on EC2 instances. For ingress management, we are utilizing an NGINX Ingress Controller. To assign external IPs to services within this cluster, we implement a load balancer solution using MetalLB.
### Installation
---
#### Install MetalLB on the Kubeadm cluster:
1. Install the manifests:
	```shell
	kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.8/config/manifests/metallb-native.yaml
	```
2. Create the `memberlist` Secret:
   MetalLB uses the `memberlist` protocol for internal communication between speaker pods.
	```shell
	kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
	```
	
>[!Important]
>If the secrets already exist, delete and recreate them:
>```shell
>kubectl delete secret memberlist -n metallb-system
>
>kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"
>```

3. Verify the Secrets:
	```shell
	kubectl describe secret memberlist -n metallb-system
	```
	**Expected output:**
	```console
	Name:         memberlist
	Namespace:    metallb-system
	
	Type:  Opaque
	
	Data
	====
	secretkey:  174 bytes
	```

4. Create an `IPAddressPool`, by defining the range of IP addresses that `MetalLB` can assign to `LoadBalancer` services.

   **Create a `metallb-ipaddresspool.yaml`:**

	```yaml
	apiVersion: metallb.io/v1beta1
	kind: IPAddressPool
	metadata:
		name: default-addresspool
		namespace: metallb-system
	spec:
		addresses:
		- 10.0.1.200-10.0.1.210
	```
5. Apply the configuration:
	```shell
	kubectl apply -f metallb-ipaddresspool.yaml
	```
6. Configure **metallb-l2advertisement.yaml** to enable MetalLB to announce IPs using Layer 2 mode:
	```yaml
	apiVersion: metallb.io/v1beta1
	kind: L2Advertisement
	metadata:
		name: default-l2advertisement
		namespace: metallb-system
	spec:
		ipAddressPools:
		- default-addresspool	
	```
7. Apply the configuration:
	```shell
	kubectl apply -f metallb-l2advertisement.yaml
	```
8. Verify the `MetalLB` installation by checking the pods:
	```shell
	kubectl gets pods -n metal-system
	```
	**Expected output (All pods should be running):**
	```console
	NAME                          READY   STATUS    RESTARTS     AGE
	controller-77676c78d9-92jh2   1/1     Running   1 (2d ago)   6d22h
	speaker-g5q7x                 1/1     Running   2 (2d ago)   6d22h
	speaker-rmmt6                 1/1     Running   2 (2d ago)   6d22h
	speaker-tvw8x                 1/1     Running   2 (2d ago)   6d22h	
	```
9. Verify the `svc`:
	```shell
	kubectl get svc -n metallb-system
	```
	**Expected result:**
	```console
	NAME                     TYPE       CLUSTER-IP  EXTERNAL-IP  PORT(S)   AGE
	metallb-webhook-service  ClusterIP  10.106.205.117  <none>  443/TCP  6d22h
	```
#### Deploying Manifests:
The `k8s` directory includes the following files:
- **`Deployment.yaml`**: Defines a Deployment for the application with multiple replicas.
- **`Service.yaml`**: Configures a Service of type LoadBalancer to expose the application internally and externally via MetalLB or a cloud provider’s load balancer.
- **`Ingress.yaml`**: Configures an Ingress resource to route HTTP traffic to the Service using a specified hostname.
1. Apply the Manifests:
	```shell
	kubectl apply -f yamls/Deployment.yaml
	kubectl apply -f yamls/Service.yaml
	kubectl apply -f yamls/Ingress.yaml
	```

2. Check that the resources have been created successfully with these commands:
	```shell
	kubectl get deployments
	kubectl get svc
	kubectl get ingress
	```

	**Expected results:**
	```console
	$ kubectl get deployment
	NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
	rick-n-morty-rick-n-morty   2/2     2            2           8s
	```

	```console
	$ kubectl get svc
	NAME                        TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
	kubernetes                  ClusterIP      10.96.0.1        <none>        443/TCP        19d
	rick-n-morty-rick-n-morty   LoadBalancer   10.101.109.240   10.0.1.201    80:31178/TCP   3m34s
	rick-n-morty-svc            LoadBalancer   10.109.73.120    10.0.1.200    80:30877/TCP   6d22h
	```

>[!note]
>Take note of the external IPs.

	```console 
	$ kubectl get ingress
	NAME                        CLASS    HOSTS                ADDRESS   PORTS   AGE
	rick-n-morty-ingress        <none>   rick-n-morty.local             80      6d22h
	rick-n-morty-rick-n-morty   <none>   rick-n-morty.local             80      8m33s
	```

3. Resolve the hostname:
	-  The provided `Ingress.yaml` uses `rick-n-morty.local` as the host.
	- If you’re using `Minikube`, get the ingress controller’s IP (e.g., Minikube IP or MetalLB’s LoadBalancer IP) and add it to your `/etc/hosts` file as rick-n-morty.local:
		```shell
		echo "<EXTERNAL_IP> rick-n-morty.local" | sudo tee -a /etc/hosts
		```

	- Replace `<EXTERNAL_IP>` with the actual IP address of the LoadBalancer or the node where the ingress is exposed. 

### Testing
---
Use the external IPs to test the connection to the application using the `curl` command:

```sh

curl http://<EXTERNAL_IP>/<URL>

```

#### Routes:
- **``/characters_data``**: Returns a JSON list of characters.
- **``/healthcheck``**: Returns a JSON object with health check results.
- **``/download``:** Downloads a CSV file with character information.

#### Examples:
	**``$ curl http://10.0.1.201/characters_data``**

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
  }
  ...
]
```

**``$ curl http://10.0.1.201/healthcheck:``**

```json
{
  "Health Checks": [
    {
      "Message": "API healthchecks passed successfully.",
      "Status": "PASSED",
      "Status code": "200",
      "Timestamp": "2024-12-14 16:03:56"
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

Ensure `rick-n-morty.local` resolves to the Ingress IP by adding this to /etc/hosts:

```sh
echo "<INGRESS_IP> rick-n-morty.local" | sudo tee -a /etc/hosts
```

**Test `rick-n-morty.local` with the `curl` command:**

```sh
curl http://rick-n-morty.local/download
curl http://rick-n-morty.local/characters_data
curl http://rick-n-morty.local/healthcheck
```

**You should get the same results as previously when using the IPs.**