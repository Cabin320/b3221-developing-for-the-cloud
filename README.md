# Introduction 
This is the Waqq.ly web application designed for the module `BS3221 Developing for the Cloud`.

Hosted in this repository, you will find all the necessary code needed to run the application, alongside the dependencies found in the `requirements.txt`.

The application has been developed using FastAPI, which is a Python web framework used to manage and build APIs. The application can be used to:
- Register dog walkers or owners
- View information on dog walkers or owners


The link to the live application hosted by Azure can be found using two different links:
- https://www.waqqly.co.uk/
- https://waqqly-web-app.azurewebsites.net/

# Install Dependencies

This project uses dependencies listed in a file called requirements.txt.  You can install them using the following command:

`pip install -r requirements.txt`

This command will download and install all the necessary libraries your program needs to run.

# Run the Application

You can start the application using the following command:

`python app.py`

## Additional Notes

You will not be able to run the application locally without the environment variables, please see the `Word document` attached in the `.zip` to find the environment variables, of which will be listed in the Appendices.

**DISCLAIMER**: Due to the use of private endpoints, you will not be able to connect to the MongoDB API, due to a network firewall to ensure security. To run the application you will either need to set up your own MongoDB instance with the collection names "owners" and "walkers" or more simply make a dictionary that can temporarily host the data in the session.
