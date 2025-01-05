----
### Directory structure
---
```
.
├── README.md
├── ci-pipeline.yaml
├── k8s-deploy-test.yaml
└── pytest.yaml
```

### Overview
---
This workflow automates a CI/CD process for a Dockerized application. It starts by running Pytest to ensure code functionality, then builds and pushes a Docker image to Docker Hub if the tests pass. Once the image is available, it deploys the application to a Kubernetes cluster using Minikube and Helm. The deployment includes setting up ingress, ensuring pod readiness, and validating the application by testing its API endpoints to confirm proper functionality.

The pipeline consists of three primary workflows:

1. **Pytest**: Runs on push to main, setting up Python, installing dependencies, and executing pytest tests to ensure the application's integrity.

2. **Docker CI Pipeline**: Triggers when the Pytest workflow completes successfully, building and pushing a Docker image to Docker Hub using version and repo info from DOCKER_VARS.

3. **K8s CD Pipeline**: Deploy the Docker image to a Minikube Kubernetes cluster using Helm after the Docker pipeline completes. It sets up Minikube, configures ingress, installs the app, ensures readiness, and tests API endpoints for functionality.

### Workflows Breakdown
---
#### Pytest Workflow (pytest.yaml)

**Location:** `.github/workflows/pytest.yaml`

**Trigger**: Runs on a `push` to the main branch.

**Purpose**: Ensures the application code passes all tests before proceeding to the next stages.

**Steps**:
- Checks out the code from the repository.
- Sets up Python 3.10.
- Installs application and test dependencies.
- Configures the PYTHONPATH for proper module resolution.
- Executes pytest, using environment variables for API key and base URL if needed.

#### CI Pipeline (ci-pipeline.yaml)
---

**Location:** `.github/workflows/ci-pipeline.yaml`

**Trigger**: Runs when the Pytest workflow successfully completes.

**Purpose**: Builds and pushes the Docker image to Docker Hub.

**Steps**:
- Checks out the code from the branch associated with the Pytest workflow.
- Loads Docker image version and repository details from the `DOCKER_VARS` file.
- Sets up Docker Buildx for efficient multi-platform image building.
- Logs into Docker Hub using secrets.
- Builds and pushes the Docker image with versioned and latest tags to Docker Hub.

#### CD Workflow (k8s-deploy-test.yaml)
---

**Location:** `.github/workflows/k8s-deploy-test.yaml`

**Trigger**: Runs when the Docker CI Pipeline completes successfully.

**Purpose**: Deploys the Docker image to a Minikube Kubernetes cluster and validates functionality.

**Steps**:
- Checks out the code.
- Sets up Minikube with Docker as the driver, allocating memory and CPUs.
- Enables `ingress` in Minikube.
- Installs `kubectl` and helm for Kubernetes operations.
- Deploys the application using Helm with ingress enabled.
- Waits for ingress controller readiness and ensures pods are running.
- Validates the deployment by:
	- Listing Kubernetes services.
	- Port-forwarding the application’s service to localhost.
	- Testing API endpoints (`/characters_data and /healthcheck`) to ensure the application works as expected.

### Screenshots
---

![Alt desc](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/application_output_workflow.png)
![Alt desc](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/k8s_services.png)
![Alt desc](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/healthchecks_workflow.png)
