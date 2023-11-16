import os
import asyncio
import httpx
from bs4 import BeautifulSoup
from pyppeteer import launch

# Set the event loop policy to fix the deprecation warning
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def get_video_src(page, url):
    await page.goto(url)
    await page.waitForSelector('video', {'timeout': 60000})
    video_src = await page.evaluate('''() => {
        const video = document.querySelector('video');
        return video ? video.src : null;
    }''')
    return video_src

async def download_media(media_url, media_type='mega'):
    # Provide the path to the Chromium executable
    browser = await launch(executablePath=r'C:\Users\brian\Downloads\Compressed\chrome-win64\chrome-win64\chrome.exe')
    page = await browser.newPage()

    try:
        video_src = await get_video_src(page, media_url)

        if video_src:
            media_title = media_url.split('/')[-1]
            download_dir = os.path.join(os.path.expanduser('~'), 'Downloads', media_type)
            os.makedirs(download_dir, exist_ok=True)

            filename = os.path.join(download_dir, f"{media_title}.mp4")

            async with httpx.AsyncClient() as client:
                response = await client.get(video_src)
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"{media_type.capitalize()} '{media_title}' downloaded successfully to {filename}.")
                else:
                    print(f"Failed to download {media_type} '{media_title}'. Error: {response.status_code}")

    finally:
        await browser.close()

async def main():
    media_url = input("Enter the URL of the movie or series to download: ")
    await download_media(media_url)

if __name__ == "__main__":
    asyncio.run(main())
