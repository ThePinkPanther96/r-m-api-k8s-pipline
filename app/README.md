----

#### Directory structure 
---
```console
├── README.md
├── __init__.py
├── __pycache__
│   ├── __init__.cpython-312.pyc
│   └── rick_and_morty.cpython-312.pyc
├── requirements.txt
├── rick_and_morty.py
├── static
│   └── background.jpg
└── templates
    ├── 404.html
    ├── 500.html
    ├── characters.html
    └── index.html
```

#### Overview
---
The **Rick & Morty Character Explorer** is a Flask-based web application that allows users to explore human characters who are alive and originate from Earth-like locations in the Rick and Morty universe. The app provides a visual interface, downloadable CSV files, and JSON REST API endpoints for programmatic data access.

#### Requirements 
---
- Python 3.x installed locally
- Docker installed (if running as a container)
- Required Python dependencies (from `requirements.txt`)

#### Building and Running the Docker Image
---
1. Build the Docker Image:
	```sh
	docker build -t rick-and-morty-app .
	```

2. Run the Docker Container:
	```sh
	docker run -d -p 5002:5002 --name rick-n-morty rick-and-morty-app
	```

	This maps the container’s port to your host’s port: `5002`.

#### Application Endpoints
---
1. Home page:
	- **Route:** `/`
	- **Action:** `GET`
	- **Description:** Displays the home page, providing navigation links to the available features and functionalities.
		![Alt text](templates/Homepage.png)
---
2. Characters page:
	- **Route:** `/characters`
	- **Action:** `GET`
	- **Description:** Presents a visually styled HTML page displaying a comprehensive list of characters.
		![Alt text](templates/Characters.png)
3. Health Checks
	- **Route:** `/healthcheck`
	- **Action:** `GET`
	- **Description:** Returns a JSON object containing status logs for various components of the app.
		![Alt text](templates/Healthchecks_paased.png)
---
4. Download CSV
	- **Route:** `/download`
	- **Action:** `GET`
	- **Description:** Downloads a CSV file with character data.
		![Alt text](templates/CSV.png)
	   ![Alt text](templates/csv_results.png)
		**See [Characters](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/characters.csv) CSV file.**
5. Error Codes
	- **Route:** `/404`
	- **Action:** `Error handle`
	- **Description:**  Invoked when a user tries to access a non-existent route.
		![Alt text](templates/404.png)
	- **Route:** `/500`
	- **Action:** `Error handle`
	- **Description:** Invoked when the application encounters an unexpected error or exception.
		![Alt text](/templates/500.png)