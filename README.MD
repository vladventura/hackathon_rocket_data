#2020 Intern Hackathon Rocket Data Scraper
---
A tool specifically made to scrape data from the rocket launch data wiki pages, so we can create models out of them.
It is written in Python, and it uses requests and BeautifulSoup to do the fetching of the webpage.
In the instance that more than

#Setup
---
- Because this project is built using Python(3), you need Python installed to run it.

- I recommend using a virtual environment to run this as well or if you want to work on it:
    - First clone the repo: `git clone https://github.com/vladventura/hackathon_rocket_data.git`
    - Then move into the repo's directory: `cd hackathon_rocket_data`
    - Install virtualenv if you haven't already: `pip install virtualenv`
    - Create a new virtualenv in the repo's root: `virtualenv .` or inside its own directory: `virtualenv <your environment directory's name>`
    - To run the environment: `source <your environment's directory>/bin/activate` (So `source ./bin/activate` for an environment in the repo's root)
    - Install the required packages to run the project: `pip install -r requirements.txt` at project root level

#Starting the app:
---
To start the app, run `python ./src/main.py` followed by the year to scrape data from (broken as of right now. See below):

    `python ./src/main.py 2020`

You can pass how many years after the base one you want data to scrape from with the -y or --years flag:

    `python ./src/main.py -y 10 2000`


#Known Issues
---
- When entering only the year without a flag, the app doesn't start. A workaround can be `python ./src/main.py -0 2020` and it scrapes 2020 only's data
- Data is not being scraped correctly. This tool needs more work but as of right now, I believe it's in a shareable state as it is.