----
### Introduction
---
This app is a Flask-based RESTful web application that interacts with the Rick and Morty API to retrieve and manage character data. It filters the data to include only human characters who are alive and have a location that mentions “Earth.” The app offers both a user-friendly web interface and RESTful API endpoints for seamless interaction. Users can view the filtered character data on a webpage, retrieve it as JSON via an API endpoint, or download it as a CSV file. The app includes health check functionality to monitor the status of the API and application, logging all events for transparency.
### Project Scope
---
To navigate through the components of this repository, use the contents table below:
- [Basic usage with Docker Image (This page)](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/README.md)
- [RESTful application](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/app/README.md)
- [K8s Cluster](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/k8s/README.md)
- [Helm Chart Deployment](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/helm/rick-n-morty/README.md)
- [Workflow Actions](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/.github/workflows/README.md)

### Usage with Docker Image
---
#### How to Build and Run the Docker Image:

1. Build the Docker Image:
	```shell
	docker build -t rick-and-morty-app .
	```
2. Run the Docker Container:
	```shell
	docker run -d -p 5002:5002 --name rick-n-morty rick-and-morty-app
	```
	This maps the container’s port 5010 to your host’s port `5002`.

#### Testing the Application:
1. Open a web browser and search for `curl http://localhost:5002/`
2. You will be greeted by the home page:
   ![Alt text](Templates/Homepage.png)
3. Navigate to the `/characters` route. 
   You will see a webpage displaying a table of filtered Rick and Morty characters, including their names, locations, and images (linked to the full-size image):
   ![Alt text](Templates/Characters.png)
   Return to the homepage by clicking the **“Back to Home”** link at the bottom of the page or by using your browser’s back button. 
   
4. Navigate to the `/healthcheck` route:
	- **The following example showcases a healthy output:**
	  ![Alt text](Templates/Healthchecks_paased.png)
	
	-  **If an error occurs due to an issue with the code while using one of the routes, you will be redirected to a 500 error page:**
	  ![Alt text](Templates/500.png)
	
	- **Afterward, navigate to the /healthcheck route to review the logs and error details:**
	  ![Alt text](Templates/Healthchecks_failed.png)
	
	- **If an error occurs because of an incorrect route in the URL, you will be redirected to a custom 404 error page:**
	   ![Alt text](Templates/404.png)
6. Click on the `/download` route to download a CSV file containing the character data:
   ![Alt text](Templates/CSV.png)
   ![Alt text](Templates/csv_results.png)
   **See [Characters](https://github.com/ThePinkPanther96/r-m-api-k8s-pipline/blob/main/Templates/characters.csv) CSV file.**
