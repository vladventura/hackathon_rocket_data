import os
import requests
import csv
from bs4 import BeautifulSoup

class RocketTableScraper:
    """Class that manages the scraping of the wiki pages of the
        Rocket Launching tables.
    """
    def __init__(self, year, save_page=False):
        self.soup = BeautifulSoup()
        self.page_html = ''
        self.data_list = []
        self.extra_list = []
        self.year = year
        self.save_page = save_page
        self.file_opened = False
        self.first_tbody = ''
        self.first_table = ''
        super().__init__()


    def load(self):
        """In charge of the initial setup
            - Creates the directory if it's not created
            - Fetches the page
            - If the user wants to save the page locally, we write the
                the file inside the year's directory as original_page.html
            - Create a soup out of the page
        """
        #Trying to open file
        self.__open_file()
        #Trying to fetch and assign soup
        self.__fetch_soup()
        # Check if we should save
        self.__save_page()
    

    def clean(self):
        """Removes the necessary elements for the parsing to work
            - Takes away all of the sub tags, which are the small numbers
                between square brackets that have a tags sometimes
            - Finds the first table with the wikitable class
            - Inside of it, removes the first three table rows from the
                table body, because these are the table headers
        """
        for sup_tag in self.soup.findAll('sup'):
            sup_tag.decompose()

        self.first_table = self.soup.findAll('table', {'class': 'wikitable'})[0]
        self.first_tbody = self.first_table.findAll('tbody')[0]

        for _ in range(3):
            self.first_tbody.find('tr').decompose()
        
    
    def scrape(self):
        """In charge of scraping the page
            - Opens/Creates a file named rocket_launch_data.csv inside the
                previously created folder
            - Does more scraping stuff that I'll place here before
                I end this"""



    def __open_file(self):
        try:
            print('Looking for file already saved')
            # Try to open the page here
            with open(f"data/{self.year}/original_page.html", "r") as file:
                self.page_html = file.read()
                self.file_opened = True
        except:
            print('File not found. Fetching from Wikipedia')


    def __fetch_soup(self):
        try:
            # Try to fetch the page from wikipedia
            if not self.file_opened: self.page_html = requests.get(f"https://en.wikipedia.org/wiki/{self.year}_in_spaceflight").text
            self.soup = BeautifulSoup(self.page_html, features="html.parser")
        except Exception as e:
            print('Something went wrong, more detail on the exception print', e)



    def __save_page(self):
        """This checks if the page should be saved locally
            and if it does, it saves it."""
        if self.save_page and self.soup:
            print('Saving file')
            try:
                with open(f"data/{self.year}/original_page.html", 'w') as file:
                    file.write(self.soup)
            except Exception as e:
                print('Something went wrong while saving the page', e)