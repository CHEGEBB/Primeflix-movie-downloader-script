import os
import webbrowser
import time
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import requests

init(autoreset=True)  # Initialize colorama

def print_color(text, color=Fore.WHITE, style=Style.NORMAL):
    print(f"{color}{style}{text}{Style.RESET_ALL}")

def show_banner():
    banner = """
__________        .__                        ___________.__  .__        
\______   \_______|__| _____   ____          \_   _____/|  | |__|__  ___
 |     ___/\_  __ \  |/     \_/ __ \   ______ |    __)  |  | |  \  \/  /
 |    |     |  | \/  |  Y Y  \  ___/  /_____/ |     \   |  |_|  |>    < 
 |____|     |__|  |__|__|_|  /\___  >         \___  /   |____/__/__/\_ \\
                           \/     \/              \/                  \/
"""
    print_color(banner, Fore.GREEN)

def search_content(content_type):
    while True:
        content_name = input(f"Enter the {content_type} name: ")
        if content_name.strip() != "":
            break
        print_color("Invalid input. Please enter a valid name.", Fore.RED)

    name_query = "+".join(content_name.split())
    result = requests.get(f"https://mycima.cloud/search/{name_query}")
    src = result.content
    soup = BeautifulSoup(src, "html.parser")

    content_info = soup.find_all("div", {"class": "Thumb--GridItem"})
    
    if len(content_info) == 0:
        print_color(f"No matching {content_type} found. Please try again.", Fore.RED)
        return None
    
    if len(content_info) > 1:
        for index, content in enumerate(content_info):
            print_color(f"{index}: {content.text}", Fore.CYAN)

        while True:
            try:
                choice = int(input(f"Choose a {content_type} by entering its index: "))
                if 0 <= choice < len(content_info):
                    return content_info[choice].find("a").attrs['href']
                else:
                    print_color("Invalid choice. Please enter a valid index.", Fore.RED)
            except ValueError:
                print_color("Invalid input. Please enter a number.", Fore.RED)
    else:
        return content_info[0].find("a").attrs['href']

def main():
    show_banner()
    print_color("Welcome to Primeflix - Created by CHEGEBB", Fore.GREEN)

    while True:
        print("\nChoose what to download:")
        print_color("1. Movie", Fore.YELLOW)
        print_color("2. TV Series", Fore.YELLOW)
        print_color("3. Links to other download sites (Coming Soon)", Fore.YELLOW)
        print_color("4. Exit", Fore.RED)

        choice = input("Enter your choice: ")

        if choice == "1":
            movie_link = search_content("movie")

            if movie_link is not None:
                print_color("Opening movie link...", Fore.GREEN)
                time.sleep(1)  # Simulate delay for animation
                webbrowser.open(movie_link)
            else:
                print_color("No valid download links found for the selected movie.", Fore.RED)
        elif choice == "2":
            series_link = search_content("TV series")

            if series_link is not None:
                print_color("Opening TV series link...", Fore.GREEN)
                time.sleep(1)  # Simulate delay for animation
                webbrowser.open(series_link)
            else:
                print_color("No valid download links found for the selected TV series.", Fore.RED)
        elif choice == "3":
            print_color("Links to other download sites functionality coming soon!", Fore.BLUE)
        elif choice == "4":
            print_color("Thank you for using Primeflix. Goodbye!", Fore.GREEN)
            break
        else:
            print_color("Invalid choice. Please enter a valid option.", Fore.RED)

if __name__ == "__main__":
    main()
