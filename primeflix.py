import os
import asyncio
import httpx
from bs4 import BeautifulSoup
from pyppeteer import launch

async def get_video_src(page, url):
    await page.goto(url)
    await page.waitForSelector('video', {'timeout': 60000})
    video_src = await page.evaluate('''() => {
        const video = document.querySelector('video');
        return video ? video.src : null;
    }''')
    return video_src

async def download_media(media_title, media_type='mega'):
    # First, try Goojara
    goojar_url = f'https://www.goojara.to/search/{media_title.replace(" ", "%20")}'
    await download_from_site(goojar_url, media_title, media_type)

async def download_from_site(site_url, media_title, media_type='mega'):
    browser = await launch()  # No need to specify executablePath for default browser
    page = await browser.newPage()

    try:
        video_src = await get_video_src(page, site_url)

        if video_src:
            download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', media_type)
            os.makedirs(download_dir, exist_ok=True)

            filename = os.path.join(download_dir, f"{media_title}.mp4")

            async with httpx.AsyncClient() as client:
                response = await client.get(video_src)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"[INFO] {media_type.capitalize()} '{media_title}' downloaded successfully to {filename}.")
                else:
                    print(f"[ERROR] Failed to download {media_type} '{media_title}'. Error: {response.status_code}")
        else:
            print(f"[INFO] Goojara did not have '{media_title}'. Trying MobileTVShows.net.")

            # Now try MobileTVShows.net
            mobiletvshows_url = f'https://www.mobiletvshows.net/search/{media_title.replace(" ", "+")}.html'
            await download_from_site(mobiletvshows_url, media_title, media_type)

    finally:
        await browser.close()

async def main():
    print("Welcome to PrimeFlix - Your number one place to download movies and TV series easily.")

    while True:
        print("\nMenu:")
        print("1. Enter Movie Title")
        print("2. Enter Series Title")
        print("3. Enter Movie URL")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            media_title = input("Enter the movie title: ")
            await download_media(media_title)
        elif choice == '2':
            media_title = input("Enter the series title: ")
            await download_media(media_title)
        elif choice == '3':
            media_url = input("Enter the movie URL: ")
            await download_media(media_url)
        elif choice == '4':
            print("Exiting PrimeFlix. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    asyncio.run(main())
