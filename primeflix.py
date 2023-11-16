import os
import requests
import urllib3
from bs4 import BeautifulSoup
import webbrowser

# Create an HTTP pool manager
http = urllib3.PoolManager()

# Function to display customized welcome message
def display_welcome():
    print("****************************************************")
    print("*          Welcome to Primeflix!       *")
    print("*  Your ultimate destination for movie exploration! *")
    print("*  Avoiding annoying pop-up ads. Enjoy the movies!  *")
    print("****************************************************\n")
    print("Exciting Intro:")
    print("Primeflix is your go-to tool for an")
    print("adventure in the world of cinema! Find your favorite")
    print("movies effortlessly and experience a cinematic journey")
    print("like never before. Choose from the options below to")
    print("embark on your movie-watching extravaganza!\n")
    print("1. Search for a Movie")
    print("2. Quit Primeflix(Enter 'q' to quit)")

# Function to select the movie source
def select_movie_source():
    print("Select a movie source:")
    print("1. mycima.cloud")
    print("2. goojara.to")
    print("3. mobiletvshow.net")

    while True:
        choice = input("Enter your choice: ")
        if choice.isdigit() and 1 <= int(choice) <= 3:
            return int(choice)

# Function to search for movies and handle missing search results
def search_for_movies(source):
    movie_name = input("Enter the movie name: ")
    movies_info = []

    if source == 1:  # mycima.cloud
        search_link = f"https://mycima.cloud/search/{'+'.join(movie_name.split())}"
        result = requests.get(search_link)
        soup = BeautifulSoup(result.content, "html.parser")
        movies_info = soup.find_all("div", {"class": "Thumb--GridItem"})
    elif source == 2:  # goojara.to
        # Implement goojara.to search logic here
        pass
    elif source == 3:  # mobiletvshow.net
        search_link = f"https://mobiletvshows.net/search.php?search={'+'.join(movie_name.split())}"
        response = http.request('GET', search_link)
        soup = BeautifulSoup(response.data, 'html.parser')
        movies_info = soup.find_all("div", {"class": "movie_thumb"})

    return movie_name, movies_info

# Function to handle user input for movie selection
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

# Function to handle movie quality selection
def get_and_display_movie_links(movie_links):
    for index, link in enumerate(movie_links):
        print(f"{index + 1}: {link}")

    while True:
        try:
            choice = input("Choose a download link (enter 'q' to quit): ")
            if choice.isdigit() and 1 <= int(choice) <= len(movie_links):
                return int(choice) - 1
            elif choice.lower() == 'q':
                exit()
            else:
                print("Invalid choice. Please choose a valid download link.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to download the selected movie
def download_movie(selected_link):
    webbrowser.open(selected_link)

# Main script logic
def main():
    display_welcome()

    # Select movie source
    source = select_movie_source()

    # Handling missing search results
    while True:
        movie_name, movies_info = search_for_movies(source)

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

    # Displaying available qualities
    print("\nAvailable Qualities:")
    print("1. 720p")
    print("2. 1080p")

    # Choosing quality
    quality_choice = int(input("Choose quality (enter 'q' to quit): "))
    if quality_choice == 1 or quality_choice == 2:
        quality = "720p" if quality_choice == 1 else "1080p"
    else:
        print("Invalid choice. Exiting.")
        exit()

    # Downloading the selected movie
    print(f"Downloading {quality} version...")
    download_movie(movie_links[quality_choice])

if __name__ == "__main__":
    main()
