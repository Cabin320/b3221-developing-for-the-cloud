# Introduction 
Welcome to the Waqq.ly web application repository! This application is designed for the module: BS3221 Developing for the Cloud.

## Overview
Waqq.ly is a web application built with FastAPI, a Python web framework used for managing and building APIs. It serves as a platform for registering dog walkers or owners and accessing information about them.

## Live Application

You can access the live application hosted on Azure through the following links:
- https://www.waqqly.co.uk/
- https://waqqly-web-app.azurewebsites.net/

# Installation
To install the necessary dependencies for running the application, execute the following command in your terminal:

`pip install -r requirements.txt`

This command will download and install all required libraries.

# Run the Application

You can start the application using the following command:

`python app.py`

## Additional Notes
- **Environment Variables**: Refer to the attached Word document in the .zip file to find the necessary environment variables. These are essential for running the application locally.
- **MongoDB API Access**: The application utilises a MongoDB API for data storage. If you encounter issues connecting to the MongoDB API due to network firewall restrictions, consider setting up your own MongoDB instance with collections named "owners" and "walkers". Alternatively, you can create a temporary dictionary to store data during the session.
