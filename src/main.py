from rocket_table_scraper import RocketTableScraper as rts
from time import sleep
import getopt
import sys

help = (
    """Rocket Launch Data Wiki Scraper for RiskyRockets
----------------------------------------------------
Usage:
    -h || --help:  Displays this menu
    -y || --years: How many more years after the base year you want to scrape.
                   Leave this empty to only scrape the base year

Examples:
    python3 main.py -y 2 2010
        This will scrape 2010 to 2012

    python3 main.py 2010
        This will only scrape 2010
""")

def check_year_is_valid(year):
    return 1944 <= year <= 2024

def scrape_year(y):
    scraper = rts(year=y)
    scraper.load()
    scraper.clean()
    scraper.scrape()
    sleep(1)


def is_integer(t):
    try:
        int(t)
        return True
    except ValueError:
        return False


def main(argv):
    years = 0
    base = 0

    try:
        opts, args = getopt.getopt(argv, "hy:", ['years='])
    except getopt.GetoptError:
        sys.exit(help)

    for opt, arg in opts:
        if opt in ('-h','--help'):
            print(help)
            sys.exit(0)
        elif opt in ('-y', '--years'):
            if is_integer(arg) and is_integer(args[0]):
                base = abs(int(args[0]))
                if int(arg) != 0: years = abs(int(arg)) + 1
                if check_year_is_valid(years + base):
                    print('Scrapping process began')

                    if years:
                        for i in range(years):
                            scrape_year(base + i)
                    else:
                        scrape_year(base)

                    print('Process finished')
                    sys.exit(0)
                else:
                    sys.exit('Given your numbers, the last year would either exceed 2024 or be too small to operate on')
            else:
                sys.exit('Only integers allowed')
    
    if args.__len__():
        if is_integer(args[0]): 
            if check_year_is_valid(int(args[0])):
                scrape_year(args[0])
                print('Process finished')
                sys.exit(0)
            else:
                sys.exit('Given your numbers, the last year would either exceed 2024 or be too small to operate on')
        else:
            sys.exit('Only integers allowed')


    sys.exit(help)


if __name__ == '__main__':
    main(sys.argv[1:])
