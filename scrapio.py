import os
import re
import requests
import time
from bs4 import BeautifulSoup
from tabulate import tabulate

# Clean terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Default User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

print(r'''
    __                      _       
   / _\ ___ _ __ __ _ _ __ (_) ___  
   \ \ / __| '__/ _` | '_ \| |/ _ \ 
   _\ \ (__| | | (_| | |_) | | (_)  v1.0
   \__/\___|_|  \__,_| .__/|_|\___/ Beta
                     |_|            
''')
time.sleep(3)

while True:
    url = input(" Enter the site URL: ")
    if not re.match(r'^https?://', url):
        print("Invalid URL format. Please include 'http://' or 'https://'")
        continue

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError:
        print("Failed to access the site. Please check the URL and try again.")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string
    print("Site title:", title)

    print("\nMenu:")
    print("1. Get all emails on the page/pages")
    print("2. Get all phone numbers on the page/pages")
    print("3. Get table data")
    print("4. Find words")
    print("5. Information/Requirements")
    print("6. Exit script")

    choice = input("\nEnter your choice (1-6): ")

    if choice == "1":
        # Get all emails
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.text)
        if emails:
            filename = input("Enter the filename to save the emails: ")
            with open(filename, 'w') as file:
                file.write("\n".join(emails))
            print("Emails saved successfully!")
        else:
            print("No matching emails found.")

    elif choice == "2":
        # Get all phone numbers
        phone_numbers = re.findall(r'\b(00963|0|\+963)?([1-9][0-9]{8})\b', soup.text)
        if phone_numbers:
            filename = input("Enter the filename to save the phone numbers: ")
            with open(filename, 'w') as file:
                file.write("\n".join(["".join(pn) for pn in phone_numbers]))
            print("Phone numbers saved successfully!")
        else:
            print("No matching phone numbers found.")

    elif choice == "3":
        # Get table data
        tables = soup.find_all('table')
        if tables:
            print("Available tables:")
            for i, table in enumerate(tables):
                print(f"Table {i+1}")
                headers = [th.text for th in table.find_all('th')]
                data = [[td.text for td in row.find_all('td')] for row in table.find_all('tr')]
                print(tabulate(data, headers=headers, tablefmt="grid"))
                print()
            table_choice = input("Enter the table number (1, 2, ...): ")
            try:
                table_choice = int(table_choice)
                if 1 <= table_choice <= len(tables):
                    table = tables[table_choice - 1]
                    headers = [th.text for th in table.find_all('th')]
                    data = [[td.text for td in row.find_all('td')] for row in table.find_all('tr')]
                    filename = input("Enter the filename to save the table data: ")
                    save_as_tabulate = input("Save as tabulate format? (y/n): ").lower() == "y"
                    with open(filename, 'w') as file:
                        if save_as_tabulate:
                            file.write(tabulate(data, headers=headers, tablefmt="grid"))
                        else:
                            file.write(tabulate(data, headers=headers, tablefmt="plain"))
                    print("Table data saved successfully!")
                else:
                    print("Invalid table number.")
            except ValueError:
                print("Invalid input.")

        else:
            print("No tables found on the page.")

    elif choice == "4":
        # Find words
        search_words = input("Enter the words to search for (comma-separated): ").split(",")
        found_words = []
        for word in search_words:
            word = word.strip()
            matches = re.findall(fr'\b\w*{word}\w*\b', soup.text)
            found_words.extend(matches)
        if found_words:
            filename = input("Enter the filename to save the found words: ")
            with open(filename, 'w') as file:
                file.write("\n".join(found_words))
            print("Found words saved successfully!")
        else:
            print("No matching words found.")

    elif choice == "5":
        # Information/Requirements
        print("Script version: 1.0")
        print("Built by: Amjad A. Bahnasi (https://github.com/amjadbahnasi/scrapio)")
        print("Requirements:")
        print("- beautifulsoup4 library (pip install beautifulsoup4)")
        print("- tabulate library (pip install tabulate)")
        print("- Python 3.6 or above")

    elif choice == "6":
        print("Exiting the script...")
        break

    else:
        print("Invalid choice. Please select a number from 1 to 6.")
