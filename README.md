#VestView README

### Compiling <br/>
   Do not need to compile because the program is in Python<br/>
   <br/>
   
### Running the Code <br/>
   Install the dependencies packages<br/>
   Activate virtual environment<br/>
   Run run.py to start the application<br/>
   <br/>
### How to run unit tests<br/>
   python -m unittest testyfinance.py<br/>
   Test passed: The output will tell you that two tests have ran and print “OK”<br/>
   Test failed: The output will tell you how many tests you failed and which test you failed<br/>

### To install the python dependencies:

	pip install -r /path/to/requirements.txt

### To interact and load the database:

First, ensure MongoDB installed on your computer.
https://docs.mongodb.com/manual/installation/

	Ensure mongod is running
	Then navigate to lib, open a python interpreter, and run these commands:
		from YMongo import *
		ym = YMongo("vestview", "stocks")
		ym.add_djia_stocks()

### Ensure you have frontend libraries and scripts (e.g. Bootstrap, Jquery):
	*you need to have nodejs https://nodejs.org/en/download/package-manager/
    *you need to have bower https://www.npmjs.com/package/bower

	Navigate to app
	Run "bower install"


### Now you must start the flask app:
	Navigate to app
	Run "python app.py"
	Then, in your web browser, navigate to "localhost:5000"
