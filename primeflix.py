import os
import requests
from bs4 import BeautifulSoup
import webbrowser

# Function to display welcome message
def display_welcome():
    print("Welcome to Super Lazy Lads Movie Downloader!")
    print("Avoiding annoying pop-up ads. Enjoy the movies!\n")

# Function to search for movies and handle missing search results
def search_for_movies():
    while True:
        movie_name = input("Enter the movie name: ")
        if movie_name:
            return movie_name

# Function to display search results and handle user selection
def display_and_select_movies(movies_info):
    for index, movie_info in enumerate(movies_info):
        print(f"{index}: {movie_info.text}")

    while True:
        try:
            choice = int(input("Choose a movie: "))
            if 0 <= choice < len(movies_info):
                return choice
        except ValueError:
            pass

# Function to get movie links and display quality options
def get_and_display_movie_links(movie_links):
    for index, link in enumerate(movie_links):
        print(f"{index}: {link}")
    
    while True:
        try:
            quality = input("Choose quality: ")
            if quality.isdigit() and 0 <= int(quality) < len(movie_links):
                return int(quality)
        except ValueError:
            pass

# Function to download the selected movie
def download_movie(selected_link):
    webbrowser.open(selected_link)

# Main script logic
def main():
    display_welcome()

    # Handling missing search results
    while True:
        movie_name = search_for_movies()
        search_link = f"https://mycima.cloud/search/{'+'.join(movie_name.split())}"
        result = requests.get(search_link)
        soup = BeautifulSoup(result.content, "html.parser")
        movies_info = soup.find_all("div", {"class": "Thumb--GridItem"})

        if movies_info:
            break
        print("No such movie found. Please try again.")

    # Handling single or multiple search results
    if len(movies_info) > 1:
        chosen_index = display_and_select_movies(movies_info)
        chosen_movie = movies_info[chosen_index]
        link = chosen_movie.find("a").attrs['href']
    else:
        link = movies_info[0].find("a").attrs['href']

    # Opening movie link
    result = requests.get(link)
    soup = BeautifulSoup(result.content, "html.parser")
    movies = soup.find_all("a", {"class": "hoverable activable"})
    
    # Getting movie links for each movie
    movie_links = [movie['href'] for movie in movies if "upbaam" in movie['href']]

    # Listing movie links according to quality
    quality_choice = get_and_display_movie_links(movie_links)

    # Downloading the selected movie
    download_movie(movie_links[quality_choice])

if __name__ == "__main__":
    main()
