# ECS781P Cloud Computing - Mini Project
This is a flask application which can be deployed using any cloud hosting service such as AWS, Google Cloud, etc. It focuses on REST APIs and their functionalities along with other capabilities. 

This app makes use of UK Police Public API available at https://data.police.uk/docs/ and focuses on calling information on 3 of the sections provided in the API.
 - **Forces related**: Gives information about various forces and departments of UK Police
 - **Crime related**: Showing various crimes in specific areas and their details
 - **Neighbourhood related**: Areas, boundaries and other information specific to a particular force


## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
The codes used in the GitHub repo use the following libraries with their corresponding versions:
```
flask>=1.1
requests>=2.23
```
which can be installed from requirements.txt
## Project Structure
Image
## Working
To start the application run

    python app.py
This triggers app.py which serves as the index file to navigate through the whole application.

flask provides a module called as `render_template` which helps to bind HTML pages with flask, it takes its input/pages from a directory called as *templates*.

On startup, app.py calls index.html which initialises and gives access to other files and URLs.
