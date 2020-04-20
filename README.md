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
### Project Structure

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

This triggers app.py which serves as the index file to navigate through the whole application. The homepage [index.html](https://github.com/yogen-p/flask_app/blob/master/templates/index.html) opens up as soon as the application launches.
It shows 3 sections in the Navigation bar.

    Home   Log In  Signup

### Normal User

These are accessible to any user who uses this app. A user can login or signup based on the situation.
Which brings the app again to home screen but with more functions.

    Home   Explore API   Explore ToDo   Logout
    
Based on the choice, user can choose the next action to perform:
* Home - `/` - Display the homepage
* Explore API - `/explore` - Leads to a new page with three different options from the API
  - *Force*: `/force` - Show info about a particular Police Force. Eg. **Kent**
  - *Crime*: `/crime` - Shows crime info around a specific area in a month. Eg. **51.52369, -0.0395857, 2018-11**
  - *Neighbourhood*: `/neigh` - Shows a list of neighbourhoods that come under jurisdiction of a force and their code. Eg. **Kent**
* Explore ToDo - `/todo` - Brings another three options to perform
  - *View*: Displays all the tasks of logged in user and also lets a user filter the displayed tasks based on its **title** and **status
  ```
  http://<hostname>:5000/tasks/title=<title>
  http://<hostname>:5000/tasks/status=<status>
  ```
  - *Add*: Lets a user add new tasks
  - *Delete*: Lets a user delete any of their tasks
* Logout - `/logout` - Literally

### Admin User

When an admin logs in with admin credentials, they see some more options as compared to a normal user.
Admin credentials can be set in the database and the code.

    Home   Explore API   Explore ToDo   Signup   All Users   Delete User   All Tasks   Logout
    
These have normal functions as a normal user and the others are:
* Signup - `/signup` - Admins can use this to add a user to the database
* All Users - `/all_users` - To see all the available users which can be filtered by name with the following uri

      http://<hostname>:5000/all_users/<name>
      
* Delete User - `/delete` - To delete any user, which also deletes all their corresponding tasks
* All Tasks - `/all_task` - Display all the tasks of all the users with the abilty to filter by title and status

      http://<hostname>:5000/all_task/status=<status>
      http://<hostname>:5000/all_task/title=<title>
 

The rest of them work same as a non-privileged user

### Security

* Passwords - Passwords are encrypted using sha256 encryption available in python library `passlib`
* Webpages - Webpages other than *Home, Login and Signup* cannot be accessed by users if they are not authenticated, i.e. logged in.
