#VestView README

### Compiling <br/>
   Do not need to compile because the program is in Python<br/>
   <br/>

### Install Python3, virtualenv, pip
MacOS Installation Reference: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos

Ubuntu Installation Reference: https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04

### To interact and load the database:
First, ensure MongoDB installed on your computer.
https://docs.mongodb.com/manual/installation/

Ensure mongod is running in a new terminal window:

  	sudo mongod

### Create a project directory (vestview) and unzip all folders into it
[Link to .zip file](INSERT LINK HERE)

## In the project directory, make a virtual environment called Venv_env:
`virtualenv Venv_env`
`source Venv_env/bin/activate`

Stay in this virtual environment for the rest of the following steps

### Install the Python dependencies

	pip install -r /path/to/requirements.txt

### To load DJIA stock data into the MongoDB Database

The following script will try to add data to the vestview/stocks collection. **It will raise errors if you have data that is inconsistent with the new schema**

If you want to update the databases DJIA data from the most recent entry to todays date:

    python yfmongo.py --update

If you want to add DJIA data for a specific data range:

    python yfmongo.py --start MM/DD/YYYY --end MM/DD/YYYY

If it does raise, then run:

    python yfmongo.py --clear

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

Run the following in the `lib` folder to do a bulk insert of news data for all of the 30 DJIA companies:

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

### Create Twitter DB and Company Collections:
Start mongo shell in a new terminal window:
`mongo`

Copy and paste this into the shell and run it:

```mongo
use twitter
db.createCollection( "3MInteractive", { capped: true, size: 300000000 } )
db.createCollection( "AmericanExpress", { capped: true, size: 300000000 } )
db.createCollection( "Apple", { capped: true, size: 300000000 } )
db.createCollection( "Boeing", { capped: true, size: 300000000 } )
db.createCollection( "CaterpillarInc", { capped: true, size: 300000000 } )
db.createCollection( "Chevron", { capped: true, size: 300000000 } )
db.createCollection( "Cisco", { capped: true, size: 300000000 } )
db.createCollection( "CocaCola", { capped: true, size: 300000000 } )
db.createCollection( "Disney", { capped: true, size: 300000000 } )
db.createCollection( "DuPont_News", { capped: true, size: 300000000 } )
db.createCollection( "ExxonMobil", { capped: true, size: 300000000 } )
db.createCollection( "GeneralElectric", { capped: true, size: 300000000 } )
db.createCollection( "GoldmanSachs", { capped: true, size: 300000000 } )
db.createCollection( "HomeDepot", { capped: true, size: 300000000 } )
db.createCollection( "IBM", { capped: true, size: 300000000 } )
db.createCollection( "Intel", { capped: true, size: 300000000 } )
db.createCollection( "JNJCares", { capped: true, size: 300000000 } )
db.createCollection( "JPMorgan", { capped: true, size: 300000000 } )
db.createCollection( "McDonalds", { capped: true, size: 300000000 } )
db.createCollection( "Merck", { capped: true, size: 300000000 } )
db.createCollection( "Microsoft", { capped: true, size: 300000000 } )
db.createCollection( "Nike", { capped: true, size: 300000000 } )
db.createCollection( "Pfizer", { capped: true, size: 300000000 } )
db.createCollection( "ProcterGamble", { capped: true, size: 300000000 } )
db.createCollection( "Travelers", { capped: true, size: 300000000 } )
db.createCollection( "UTC", { capped: true, size: 300000000 } )
db.createCollection( "MyUHC", { capped: true, size: 300000000 } )
db.createCollection( "Verizon", { capped: true, size: 300000000 } )
db.createCollection( "Visa", { capped: true, size: 300000000 } )
db.createCollection( "Walmart", { capped: true, size: 300000000 } )
```

### Insert some tweets into Apple Collections
Make sure you are in the `lib` directory and run the following:
```python
python3 insertTweets.py
```

### Ensure you have frontend libraries and scripts (e.g. Bootstrap, Jquery):
	*you need to have nodejs https://nodejs.org/en/download/package-manager/
    *you need to have bower https://www.npmjs.com/package/bower

	Navigate to app
	Run "bower install"


### Now you must start the flask app:
	Navigate to app
	Run "python app.py"
	Then, in your web browser, navigate to "localhost:5000"
