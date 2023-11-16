from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

def initialize_browser(driver_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1366x768")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--dns-prefetch-disable")
    return webdriver.Chrome(executable_path=driver_path, options=chrome_options)

def search_for_movie(browser, movie_title):
    search_box = browser.find_element("xpath", '//*[@id="search"]')
    search_box.send_keys(movie_title)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Allow time for the search results to load

def download_movie(browser, download_link, count):
    # Implement your download logic here
    pass

if __name__ == "__main__":
    driver_path = r'C:\Users\brian\Downloads\Compressed\chromedriver-win64\chromedriver.exe'
    browser = initialize_browser(driver_path)

    # Prompt the user to enter the movie title they want to search
    movie_title = input("Enter the name of the movie: ")
    
    # Use Selenium to perform the search
    browser.get("https://www.goojara.to/")
    search_for_movie(browser, movie_title)

    # Extract and print the search results (for demonstration purposes)
    search_results = browser.find_elements("xpath", '//div[@class="movie-box"]//a[@class="title"]')
    if not search_results:
        print("No results found.")
    else:
        print("Search Results:")
        for i, result in enumerate(search_results, start=1):
            print(f"{i}. {result.text}")

        # Allow the user to choose a movie to download
        choice = input("Enter the number of the movie you want to download: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(search_results):
                # Click on the selected movie to go to its page
                selected_movie = search_results[choice - 1]
                selected_movie.click()
                
                # Implement your download logic for the selected movie
                download_link = browser.find_element("xpath", '//*[@id="download"]')
                download_movie(browser, download_link, count=1)
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        finally:
            browser.quit()
