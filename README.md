# Rick and Morty API Application Project
----

### Directory
---
```
├── DOCKER_VARS
├── Dockerfile
├── README.md
├── Templates
│   ├── 404.png
│   ├── 500.png
│   ├── CSV.png
│   ├── Characters.png
│   ├── Healthchecks_failed.png
│   ├── Healthchecks_paased.png
│   ├── Homepage.png
│   ├── characters.csv
│   └── csv_results.png
├── app
│   ├── README.md
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   └── rick_and_morty.cpython-312.pyc
│   ├── requirements.txt
│   ├── rick_and_morty.py
│   ├── static
│   │   └── background.jpg
│   └── templates
│       ├── 404.html
│       ├── 500.html
│       ├── characters.html
│       └── index.html
├── helm
│   └── rick-n-morty
│       ├── Chart.yaml
│       ├── README.md
│       ├── templates
│       │   ├── _helpers.tpl
│       │   ├── deployment.yaml
│       │   ├── ingress.yaml
│       │   └── service.yaml
│       └── values.yaml
├── k8s
│   ├── README.md
│   ├── deployment.yaml
│   ├── ingress.yaml
│   ├── metallb-ipaddresspool.yaml
│   ├── metallb-l2advertisement.yaml
│   └── service.yaml
└── tests
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-312.pyc
    │   └── test_rick_n_morty.cpython-312-pytest-8.3.3.pyc
    ├── requirements.txt
    └── test_rick_n_morty.py
```

### Introduction
---
This app is a Flask-based RESTful web application that interacts with the Rick and Morty API to retrieve and manage character data. It filters the data to include only human characters who are alive and have a location that mentions “Earth.” The app offers both a user-friendly web interface and RESTful API endpoints for seamless interaction. Users can view the filtered character data on a webpage, retrieve it as JSON via an API endpoint, or download it as a CSV file. The app includes health check functionality to monitor the status of the API and application, logging all events for transparency.

### Project Scope
---
To navigate through the components of this repository, use the contents table below:
- [RESTful API Application](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/app/README.md)

- [K8s Cluster](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/k8s/README.md)

- [Helm Chart Deployment](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/helm/rick-n-morty/README.md)

- [Workflow Actions](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/.github/workflows/README.md)

---
![Alt desc](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/rick-n-morty.jpg)