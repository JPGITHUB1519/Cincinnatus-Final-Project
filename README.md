# This is our Cinccinnatus Final Project :


## What is it About?

Here, we created a Blog Engine. 

## Tecnology

### Front - End

	- HTML
	- CSS
	- Javascript
	
#### Front - End Frameworks

	- Bootstrap v3.3.7
	- jQuery v3.1.0

### Back - End

	- Python 2.7 with Google App Engine and webapp2 Framework

## Folder Structure Documentation

### Handlers

Top level directory which contains all the RequestHandler of the application. There is a basic handler for basic stuffs and the other handlers inherit from it. 

### Models

Top level directory which contains all the datastore models of the data.

### Templates

Top level directory containing all of the HTML templates.

Here we have a file called base.html who contains all basic commons stuffs of the files. Most of the other templates inherit from base.html.

### Static

Top level directory which contains all The Static Files.

##### This have subdtividitions :

* css : This directory contains all the css files for the project including externals frameworks. It has a sub-directory called Vendor.

* js : This directory contains all the javascript files for the project including externals frameworks. It has a sub-directory called Vendor.

* imgs : This directory contains all the images files for the project.

* css and js directories have a sub-folder called vendor, this contains all the externar frameworks firles for the project.

### Other important files in the Parent Directory

* main.py - It binds all the files toguether and here we put all  the URL mapping.

* general.py - This has all the global variables for the project. This is like configuration file.

* utility.py - This file contains utility functions that can be used by the other files.


> Written by Jean Ureña - Software Developer. Cincinnatus Student