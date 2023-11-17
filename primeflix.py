import requests
from bs4 import BeautifulSoup
import webbrowser
import sys

def print_header():
    print("=====================================")
    print("     Welcome to Primeflix!           ")
    print(" Your number one place to download   ")
    print("      and stream hassle-free         ")
    print("=====================================")

def get_user_option():
    while True:
        try:
            option = int(input("\nWhat do you want to watch? (Enter 1, 2, or 3)\n"
                               "1- Series\n"
                               "2- Movie\n"
                               "3- Download a whole season\n"))
            if 3 >= option >= 1:
                return option
            else:
                print("Please enter 1, 2, or 3")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_series_name():
    return input("Enter the movie or series name: ").strip()

def print_series_options(recommended_series):
    print("Which series do you want to watch?")
    for idx, series in enumerate(recommended_series, start=1):
        title = series.find("a").get("title", f"Series {idx}")
        print(f"{idx}. {title}")

def get_user_selected_series(recommended_series):
    while True:
        try:
            series_number = int(input("Enter the number corresponding to your wanted series: "))
            if 1 <= series_number <= len(recommended_series):
                return series_number
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_selected_season(seasons_links):
    while True:
        try:
            season_number = int(input(f"There are {len(seasons_links)} Seasons. Enter your desired season number: "))
            if 1 <= season_number <= len(seasons_links):
                return season_number
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_selected_episodes(episodes_links):
    while True:
        try:
            print(f"There are {len(episodes_links)} episodes")
            ep1 = int(input("Enter episode number (from): "))
            ep2 = int(input("Enter episode number (to): "))
            if 1 <= ep1 <= len(episodes_links) and 1 <= ep2 <= len(episodes_links) and ep1 <= ep2:
                return ep1, ep2
            else:
                print("Invalid selection. Please enter valid episode numbers.")
        except ValueError:
            print("Invalid input. Please enter numbers.")

def main():
    print_header()
    option = get_user_option()

    if option == 1:  # Watch a series
        series_name = get_user_series_name()
        html_page = requests.get(f"https://mycima.tube/search/{series_name}/list/series")
        soup = BeautifulSoup(html_page.content, "lxml")
        recommended_series = soup.find_all("div", {"class": "Thumb--GridItem"})

        print_series_options(recommended_series)
        series_number = get_user_selected_series(recommended_series)

        html_page = requests.get(recommended_series[series_number - 1].find("a").get("href"))
        soup = BeautifulSoup(html_page.content, "lxml")
        temp_list = soup.find("div", {"class": "List--Seasons--Episodes"})

        if temp_list is None:
            temp_list = soup.find("div", {"class": "Seasons--Episodes"})
        seasons_links = temp_list.findAll("a")
        season_number = get_user_selected_season(seasons_links)

        html_page = requests.get(seasons_links[season_number - 1].get("href"))
        soup = BeautifulSoup(html_page.content, "lxml")
        temp_list = soup.find("div", {"class": "Episodes--Seasons--Episodes"})
        episodes_links = temp_list.findAll("a")
        episodes_links.reverse()

        ep1, ep2 = get_user_selected_episodes(episodes_links)

        for episode_number in range(ep2, ep1 - 1, -1):
            html_page = requests.get(episodes_links[episode_number - 1].get("href"))
            soup = BeautifulSoup(html_page.content, "lxml")
            link = soup.find("iframe", {"name": "watch"})
            watching_link = link.get("data-lazy-src")
            result = requests.get(watching_link)
            webbrowser.open(watching_link)

    elif option == 2:  # Watch a movie
        movie_name = get_user_series_name()
        html_page = requests.get(f"https://mycima.tube/search/{movie_name}")
        soup = BeautifulSoup(html_page.content, "lxml")
        recommended_movies = soup.find_all("div", {"class": "Thumb--GridItem"})

        print_series_options(recommended_movies)
        movie_number = get_user_selected_series(recommended_movies)
        movie_link = recommended_movies[movie_number - 1].find("a").get("href")

        html_page = requests.get(movie_link)
        soup = BeautifulSoup(html_page.content, "lxml")
        link = soup.find("iframe", {"name": "watch"})
        watching_link = link.get("data-lazy-src")
        webbrowser.open(watching_link)

    else:  # Download a whole season
        series_name = get_user_series_name()
        series_name = series_name.replace(" ", "-")
        season_number = int(input("Enter Season number: "))

        urls = [
            f"https://mycima.tube/series/{series_name}-%d9%85%d9%88%d8%b3%d9%85-{season_number}-",
            f"https://mycima.tube/series/%D9%85%D9%88%D8%B3%D9%85-{season_number}-%D9%85%D8%B3%D9%84%D8%B3%D9%84-{series_name}",
            f"https://mycima.tube/series/%d9%85%d9%88%d8%b3%d9%85-{season_number}-{series_name}",
            f"https://mycima.tube/series/{series_name}-%d9%85%d9%88%d8%b3%d9%85-{season_number}",
        ]

        for url in urls:
            html_page = requests.get(url)
            if html_page.status_code != 404:
                break

        soup = BeautifulSoup(html_page.content, "lxml")
        x = soup.find('ul', {'class': "Season--Download--Mycima--Single"})

        if x is None:
            input(f"This feature is not available for {series_name} season {season_number}! \nPress any key to exit")
            sys.exit()

        temp = x.findAll("a")
        qualities = soup.find_all("resolution")
        links = [i.get("href") for i in temp]

        for idx, quality in enumerate(qualities, start=1):
            print(f"{idx}- {quality.text}")

        while True:
            try:
                quality_number = int(input("Enter your desired quality: "))
                if 1 <= quality_number <= len(qualities):
                    webbrowser.open(links[quality_number - 1])
                    break
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        input("Enter any key to exit: ")

if __name__ == "__main__":
    main()
