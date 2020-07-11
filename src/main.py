from bs4 import BeautifulSoup
import csv
import requests

starting_year = "2020"

"""
To clean this up a bit:

Request the page for the year
Make a soup from the html of the page

Remove each sup tag from the soup
Get the first table with class wikitable collapsible
Get the first tbody inside of it

Dispose the first 3 tr we find (maybe repeat soup.select(tr).decompose() three times)
Create a csv file named rocket_data inside the folder of the year on data

On the csv file, add the rows
Set up a list for the values so we can push them here

For each tr
    If it has no style
        We write to file 
        We clean up the list
        For each td inside this tr
            If the td has a colspan of 2
                Get the span tag inside of it, then the a tag inside of it, then append it's class to the list
            Append the text to list
    Else if it has style background #e8eeee or #e9e4e4
        For each td inside this tr 
            Append text to list
"""
# Testing with 2020 page first

# We request the 2020 page and translate to html
# rockets2020html = requests.get(f"https://en.wikipedia.org/wiki/{starting_year}_in_spaceflight").text

rockets2020html = ''

with open(f'data/{starting_year}/table.html', 'r') as file:
    rockets2020html = file.read()

# We make a soup out of that
soup = BeautifulSoup(rockets2020html, features="html.parser")

# Removing all sup tags
for sup in soup.findAll('sup'):
    sup.decompose()

# Not needed because we have the local table file
# Getting the first table with class wikitable
# first_table = soup.findAll('table', {'class': 'wikitable'})[0]


# Getting the first tbody inside of it
first_tbody = soup.findAll('tbody')[0]

# Removing the first three tr
for _ in range(3):
    first_tbody.find('tr').decompose()

# Already saved
# Saving table locally so we don't re-query wikipedia every time
with open('data/2020/tbody.html', 'w') as file:
    file.write(str(first_tbody))
            
# Creating file for the data
with open(f'data/{starting_year}/rocket_launch_data.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Date and Time', 'Rocket Country','Rocket', 'Flight Number', 'Launched Country', 'Launch Site','LSP Country', 'LSP', 'Payload', 'Operator', 'Orbit', 'Function', 'Decay', 'Outcome', 'Remarks'])
    data_list = []
    extra_list = []
    write = False
    for tr in first_tbody.findAll('tr'):
        country_inserted = False
        write = False
        monthSpan = tr.find('td').find('span', {'class': 'mw-headline'})
        if monthSpan:
            monthSpanText = monthSpan.get_text() if monthSpan and monthSpan.get_text() != 'To be determined' else ""
            if monthSpanText:
                print(monthSpanText)
        elif not 'style' in tr.attrs:
            for td in tr.findAll('td'):
                if td.find('span') and 'colspan' in td.attrs:
                    if td.find('span').find('a'):
                        # I don't know how else to save this one
                        title = ' '.join(td.find('span').find('a')['title'].split())
                        if not country_inserted: 
                            data_list.append(title)
                            country_inserted = True
                if not td.find('li'):
                    data_list.append(' '.join(td.get_text().split()))
        elif tr['style'] == 'background: #e8eeee':
            temp_list = []
            for td in tr.findAll('td'):
                temp_list.append('\n'.join(td.get_text().strip().split('\n')))

            if 'style' in tr.findNext('tr').attrs and tr.findNext('tr')['style'] == 'background: #e8eeee':
                if extra_list.__len__() > 0 and temp_list.__len__() > 0:
                    extra_list = ['\n'.join([a,b]).strip() for a,b in zip(extra_list, temp_list)]
                else:
                    extra_list = temp_list

            else:
                if extra_list.__len__() > 0 and temp_list.__len__() > 0:
                    extra_list = ['\n'.join([a,b]).strip() for a,b in zip(extra_list, temp_list)]
                else:
                    extra_list = temp_list
                data_list.extend(extra_list)
                extra_list = []
                if 'style' in tr.findNext('tr').attrs:
                    if tr.findNext('tr')['style'] == 'background-color:#e9e4e4;' or 'background-color: #e9e4e4;':
                        write = False
                else: write = True
        
        elif tr['style'] == 'background-color:#e9e4e4;' or tr['style'] == 'background-color: #e9e4e4;':
            data_list.append(tr.get_text())
            write = True
        
        if write: 
            filewriter.writerow(data_list)
            data_list = []