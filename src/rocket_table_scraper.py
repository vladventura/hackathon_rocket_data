import os
import requests
import csv
from bs4 import BeautifulSoup


class RocketTableScraper:
    """Class that manages the scraping of the wiki pages of the
        Rocket Launching in a year tables.
    """

    def __init__(self, year, save_page=False):
        self.soup = BeautifulSoup(features="html.parser")
        self.data_list = []
        self.extra_list = []
        self.page_html = ""
        self.year = year
        self.save_page = save_page
        self.file_opened = False
        self.loaded = False
        self.country_inserted = False
        self.write = False
        self.first_tbody = BeautifulSoup(features="html.parser")
        self.current_tr = BeautifulSoup(features="html.parser")
        self.TABLE_ROWS = [
            "Date and Time",
            "Rocket",
            "Flight Number",
            "Launch Country",
            "Launch Site",
            "LSP",
            "Payload",
            "Operator",
            "Orbit",
            "Function",
            "Decay",
            "Outcome",
            "Remarks",
        ]
        super().__init__()

    def load(self):
        """In charge of the initial setup
            - Creates the directory if it's not created
            - Fetches the page
            - If the user wants to save the page locally, we write the
                the file inside the year's directory as original_page.html
            - Create a soup out of the page
        """
        # Try to create directory
        self.__create_directory()
        # Trying to open file
        self.__open_file()
        # Trying to fetch and assign soup
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
        for sup_tag in self.soup.findAll("sup"):
            sup_tag.decompose()

        first_table = self.soup.findAll("table", {"class": "wikitable"})[0]
        self.first_tbody = first_table.findAll("tbody")[0]

        for _ in range(3):
            self.first_tbody.find("tr").decompose()

    def scrape(self):
        """In charge of scraping the page
            - Opens/Creates a file named rocket_launch_data.csv inside the
                previously created folder
            - Iterates over each table row inside the table body we scraped earlier
        """
        try:
            if self.loaded:
                with open(f"data/{self.year}/rocket_launch_file.csv", "w") as file:
                    filewriter = csv.writer(
                        file, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                    filewriter.writerow(self.TABLE_ROWS)
                    for tr in self.first_tbody.findAll("tr"):
                        self.country_inserted = False
                        self.write = False
                        month_span = tr.find("td").find(
                            "span", {"class": "mw-headline"})
                        if month_span:
                            text = (
                                month_span.get_text()
                                if month_span.get_text() != "To be determined"
                                else ""
                            )
                            if text:
                                print(
                                    f'Operating on data from {text} {self.year}')
                        elif not "style" in tr.attrs:
                            for td in tr.findAll("td"):
                                if td.find("span") and "colspan" in td.attrs:
                                    if td.find("span").find("a"):
                                        title = " ".join(
                                            td.find("span").find("a")[
                                                "title"].split()
                                        )
                                        if not self.country_inserted:
                                            self.data_list.append(title)
                                            self.country_inserted = True
                                if not td.find("li"):
                                    if not "Upcoming launches" in td.get_text():
                                        self.data_list.append(
                                            " ".join(td.get_text().split()))
                                    else:
                                        continue

                        elif "e8eeee" or "" in tr["style"]:
                            temp_list = []
                            for td in tr.findAll("td"):
                                temp_list.append(
                                    "\n".join(td.get_text().strip().split("\n")))

                            if self.extra_list.__len__() > 0 and temp_list.__len__() > 0:
                                self.extra_list = [
                                    "\n".join([a, b]).strip()
                                    for a, b in zip(self.extra_list, temp_list)
                                ]
                            else:
                                self.extra_list = temp_list

                            # This answers if there's anything else to write to this current data column/line
                            if (
                                "style" not in tr.findNext("tr").attrs
                                or ("e9e4e4" in tr.findNext("tr")["style"])
                            ):
                                self.data_list.extend(self.extra_list)
                                self.extra_list = []
                                # If there's a comment about the mission
                                if "style" in tr.findNext("tr").attrs:
                                    if (
                                        "e9e4e4" in tr.findNext("tr")["style"]
                                    ):
                                        self.write = False
                                    else:
                                        self.write = True
                                else:
                                    self.write = True

                        elif (
                            tr["style"] == "background-color:#e9e4e4;"
                            or tr["style"] == "background-color: #e9e4e4;"
                        ):
                            self.data_list.append(tr.get_text())
                            self.write = True

                        if self.write:
                            filewriter.writerow(self.data_list)
                            self.data_list = []
            else:
                print('Something went wrong while loading. Process canceled')
        except:
            print("Something went wrong. I blame it on the inconsistent Wikipedia pages")

    def __create_directory(self):
        try:
            print("Is data already created?")
            os.mkdir('data/')
        except:
            print('Yes, it is')
        try:
            print("Trying to create directory")
            os.mkdir(f"data/{self.year}/")
        except OSError as error:
            print("Directory found")

    def __open_file(self):
        try:
            print("Looking for file already saved")
            # Try to open the page here
            with open(f"data/{self.year}/original_page.html", "r") as file:
                self.page_html = file.read()
                self.file_opened = True
        except:
            print("File not found. Fetching from Wikipedia")

    def __fetch_soup(self):
        try:
            # Try to fetch the page from wikipedia
            if not self.file_opened:
                self.page_html = requests.get(
                    f"https://en.wikipedia.org/wiki/{self.year}_in_spaceflight"
                ).text
            self.soup = BeautifulSoup(self.page_html, features="html.parser")
            self.loaded = True
        except Exception as e:
            print("Something went wrong, more detail on the exception print", e)

    def __save_page(self):
        """This checks if the page should be saved locally
            and if it does, it saves it.
        """
        if self.save_page and self.soup:
            print("Saving file")
            try:
                with open(f"data/{self.year}/original_page.html", "w") as file:
                    file.write(str(self.soup))
            except Exception as e:
                print("Something went wrong while saving the page", e)
