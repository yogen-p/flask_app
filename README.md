# ECS781P Cloud Computing - Mini Project
This is a flask application which can be deployed using any cloud hosting service such as AWS, Google Cloud, etc. It focuses on REST APIs and their functionalities along with other capabilities. 

### UK Police Public API
This app makes use of UK Police Public API available at https://data.police.uk/docs/ and focuses on calling information on 3 of the sections provided in the API.
 - **Forces related**: Gives information about various forces and departments of UK Police
 - **Crime related**: Showing various crimes in specific areas and their details
 - **Neighbourhood related**: Areas, boundaries and other information specific to a particular force

### TODO
Mini Project also integrates a simple ToDo application to maintain task list separately for each authenticated user which can perform standard CRUD operations.

### Admin Privileges
Along with user accounts and access management, role based policies are also provided for authorised users. It gives rights to view, create and delete all users and their tasks.

## Getting started
This section will help you to get this project up and running in your system

### Prerequisites
The codes used in the GitHub repo use the following libraries with their corresponding versions:
```
flask>=1.1
requests>=2.23
flask_sqlalchemy>=2.4.1
flask_login>=0.5.0
...
```
which can be installed from requirements.txt using Linux command

```
pip install -r requirements.txt
```
## Project Structure

    .
    ├── templates               # Contains html files
    │   ├── index.html          # Display the homepage
    │   ├── base.html           # Basic design for all html files
    │   ├── todo.html           # Interface for ToDo 
    │   └── explore.html        # Interface for UK Police public API
    ├── app.py                  # Main file to launch app
    ├── exploring.py            # Backend for UK Police public API
    ├── tasks.py                # Backend for ToDo
    ├── responses.py            # Some standard HTTP responses
    └── ...

## Working
To start the application run

    python app.py
This triggers app.py which serves as the index file to navigate through the whole application.

flask provides a module called as `render_template` which helps to bind HTML pages with flask, it takes its input/pages from a directory called as *templates*.

On startup, app.py calls index.html which initialises and gives access to other files and URLs.
