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

Ensure mongod is running:

    `sudo mongod`

### To load DJIA stock data into the MongoDB Database

The following script will try to add data to the vestview/stocks collection. **It will raise errors if you have data that is inconsistent with the new schema**

If it does raise, then run:

    python yfmongo.py --clear

If you want to add DJIA data for a specific data range:

    python yfmongo.py --start MM/DD/YYYY --end MM/DD/YYYY

If you want to update the databases DJIA data from the most recent entry to todays date:

    python yfmongo.py --update

The data is stored in the following way:

    {
            "Date": python datetime
            "AAPL": {
                    "adjClose":float
                    "close":    float
                    "high":     float
                    "low":      float
                    "open":     float
                    "symbol":   float
                    "volume":   float
                    }
            ....
            ....
            "WMT:": {.....}
       }

### To load DJIA news data into the MongoDB Database

The following script will create collections for each of the 30 DJIA stocks in the `news` database. Each collection is named after the company's stock ticker symbol. For example, Apple's collection is the news.AAPL collection.

*There is no guarentee on what dates are inserted. The current implementation grabs 500 articles from the google finance stream for a particular company, and inserts articles associated with dates that aren't already in the database.*

Run the following to do a bulk insert of news data for all of the 30 DJIA companies:

    python gfnews.py --insert

Run the following to list **all** the titles associated with a certain company

    python gfnews.py --list <symbol>

Each company has a document corresponding to a date has articles associated with it, in the following format:

    {
      "date": python datetime
      "articles": [
                      {
                        "title":           string
                        "titleId":         string
                        "openingSentence": string
                        "url":             string
                        "source":          string
                        "date":            python datetime
                      }
                  ]
    }

For example, in the news.APPL collection, the document corresponding to 11/25/2016 has
4 articles associated with it.

### Ensure you have frontend libraries and scripts (e.g. Bootstrap, Jquery):
	*you need to have nodejs https://nodejs.org/en/download/package-manager/
    *you need to have bower https://www.npmjs.com/package/bower

	Navigate to app
	Run "bower install"


### Now you must start the flask app:
	Navigate to app
	Run "python app.py"
	Then, in your web browser, navigate to "localhost:5000"
