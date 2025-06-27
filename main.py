from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import requests
import http.client
from urllib.parse import urlparse
import json
import os
import random
import re
from bs4 import BeautifulSoup as bs

TOKEN = '' # your telegram token here

# Your RapidAPI credentials
RAPIDAPI_KEY = "" # your rapid api key.

def extract_video_id(url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
    if match:
        return match.group(1)
    return None

def get_video_download_link(video_id: str) -> str:
    """
    Gets the download link for the YouTube video using the RapidAPI.
    """
    conn = http.client.HTTPSConnection("yt-api.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "yt-api.p.rapidapi.com"
    }

    try:
        conn.request("GET", f"/dl?id={video_id}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode("utf-8"))

        # Debug: Print the API response for inspection
        print("API Response:", result)

        if result.get('formats'):
            # Find the highest quality video
            best_video = max(result['formats'], key=lambda x: int(x.get('qualityLabel', '0').replace('p', '')), default=None)
            if best_video:
                return best_video.get('url', None)
        return None
    except Exception as e:
        print(f"Error while fetching video download link: {e}")
        return None
    
# Helper function to generate a random User-Agent
def random_ua():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/602.3.12',
        # Add more User-Agents if needed
    ]
    return random.choice(user_agents)

# Function to download TikTok video using one of the three methods
def get_content(url, output_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(output_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return output_name
    return None

class Downloader:
    def __init__(self, output_name: str):
        self.output_name = output_name

    def snaptikpro(self, url: str):
        try:
            ses = requests.Session()
            ses.headers.update({"User-Agent": random_ua()})

            res = ses.get("https://snaptik.pro/")
            token = re.search('<input type="hidden" name="token" value="(.*?)">', res.text).group(1)
            data = {"url": url, "token": token, "submit": "1"}
            res = ses.post("https://snaptik.pro/action", data=data)

            if res.json()["error"]:
                return None

            video_url = re.search(
                '<div class="btn-container mb-1"><a href="(.*?)" target="_blank" rel="noreferrer">',
                res.json()["html"],
            ).group(1)
            return video_url if len(video_url) > 0 else None

        except Exception as e:
            print(f"snaptikpro error: {e}")
            return None

    def tiktapiocom(self, url: str):
        try:
            ses = requests.Session()
            ses.headers.update({"User-Agent": random_ua()})
            res = ses.get("https://tiktokio.com/id/")
            prefix = re.search(r'<input type="hidden" name="prefix" value="(.*?)"/>', res.text).group(1)
            data = {"prefix": prefix, "vid": url}
            ses.headers.update(
                {
                    "Content-Length": str(len(str(data))),
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Hx-Current-Url": "https://tiktokio.com/",
                    "Hx-Request": "true",
                    "Hx-Target": "tiktok-parse-result",
                    "Hx-Trigger": "search-btn",
                }
            )
            res = ses.post("https://tiktokio.com/api/v1/tk-htmx", data=data)
            parser = bs(res.text, "html.parser")
            video_url = (
                parser.find_all("div", attrs={"class": "tk-down-link"})[0]
                .find("a")
                .get("href")
            )
            return video_url if video_url else None

        except Exception as e:
            print(f"tiktapiocom error: {e}")
            return None

    def tikmatecc(self, url: str):
        try:
            headers = {
                "Host": "europe-west3-instadown-314417.cloudfunctions.net",
                "User-Agent": "socialdownloader.p.rapidapi.com",
                "Accept": "*/*",
                "Accept-Language": "ar",
                "Accept-Encoding": "gzip, deflate",
            }
            api = "https://europe-west3-instadown-314417.cloudfunctions.net/yt-dlp-1?url=" + url
            res = requests.get(api, headers=headers)
            if res.text[0] != "{":
                return None

            error = res.json()["null"] or res.json()["error"] or res.json()["Error"]
            if error:
                return None

            video_url = res.json()["LINKS"]
            return video_url if video_url else None

        except Exception as e:
            print(f"tikmatecc error: {e}")
            return None

    def download_tiktok(self, url: str):
        # Attempt to get the download link using each method in sequence
        video_url = self.snaptikpro(url)
        if video_url:
            return video_url
        video_url = self.tiktapiocom(url)
        if video_url:
            return video_url
        video_url = self.tikmatecc(url)
        if video_url:
            return video_url
        return None



def get_shortcode(url: str) -> str:
    """
    Extract the shortcode from an Instagram URL.
    """
    path = urlparse(url).path
    if path.startswith('/reels/'):
        return path.split('/')[2]
    elif path.startswith('/p/'):
        return path.split('/')[2]
    else:
        raise ValueError("Unsupported URL format")

def instagram_get_url(url_media: str) -> dict:
    try:
        shortcode = get_shortcode(url_media)
        API_URL = f"https://instagram-bulk-scraper-latest.p.rapidapi.com/media_info_from_shortcode/{shortcode}"
        headers = {
            'x-rapidapi-key': "7dc4306dacmshb56c036b0656a2bp1b870ajsnfe5e11495a88",
            'x-rapidapi-host': "instagram-bulk-scraper-latest.p.rapidapi.com"
        }

        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        data = response.json()
        media = data['data']

        if media['is_video']:
            # Extract video URL
            video_url = media.get('video_url')
            return {'video_url': video_url}
        else:
            # Extract image URL
            display_url = media.get('display_url')
            return {'image_url': display_url}

    except Exception as e:
        print(f"Error: {e}")
        return {'error': str(e)}


def download_pinterest(url: str) -> dict:
    conn = http.client.HTTPSConnection("pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com")

    payload = json.dumps({"id": url})

    headers = {
        'x-rapidapi-key': "7dc4306dacmshb56c036b0656a2bp1b870ajsnfe5e11495a88",
        'x-rapidapi-host': "pinterest-downloader-download-pinterest-image-video-and-reels.p.rapidapi.com",
        'Content-Type': "application/json"
    }

    try:
        conn.request("POST", "/api/server", payload, headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))

        media_urls = {}

        if data.get('data'):
            media = data['data']

            # Handle images
            images = media.get('images', {})
            if images:
                best_image = max(images.values(), key=lambda x: x.get('width', 0))
                image_url = best_image.get('url', '')
                if image_url:
                    media_urls['image'] = image_url

            # Handle videos
            stories = media.get('stories', [])
            if stories:
                for story in stories:
                    video_list = story.get('video', {}).get('video_list', {})
                    if video_list:
                        mp4_videos = [v for v in video_list.values() if v.get('url', '').endswith('.mp4')]
                        if mp4_videos:
                            best_video = max(mp4_videos, key=lambda x: x.get('width', 0))
                            video_url = best_video.get('url', '')
                            if video_url:
                                media_urls['video'] = video_url

        return media_urls

    except Exception as e:
        print(f"Pinterest download error: {e}")
        return {}

# Function to download a file (used for other media)
def download_file(url: str, filename: str) -> str:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded {filename}")
        return filename
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
        return ''

# Telegram bot handlers
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('AwesomeBoy personal downloader')

async def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text

    # Handle Pinterest links
    if 'https://www.pinterest.com/pin/' in text or 'https://pin.it/' in text:
        media_urls = download_pinterest(text)
        if media_urls:
            response = ""
            if 'image' in media_urls:
                response += f"Image URL: {media_urls['image']}\n"
            if 'video' in media_urls:
                response += f"Video URL: {media_urls['video']}\n"
            if response:
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("No media found.")
        else:
            await update.message.reply_text("Failed to retrieve Pinterest media.")

    # Handle TikTok links
    elif 'https://www.tiktok.com/@' in text and '/video/' in text or 'https://vm.tiktok.com/' in text:
        downloader = Downloader(output_name="tiktok_video.mp4")
        video_url = downloader.download_tiktok(text)
        if video_url:
            await update.message.reply_text(f"TikTok video download link: {video_url}")
        else:
            await update.message.reply_text("Failed to retrieve TikTok video link.")

    # Handle YouTube links
    elif 'https://www.youtube.com/watch?v=' in text or 'https://youtu.be/' in text:
        video_id = extract_video_id(text)
        if video_id:
            try:
                download_link = get_video_download_link(video_id)
                if download_link:
                    await update.message.reply_text(f"Here is your download link: {download_link}")
                else:
                    await update.message.reply_text("Failed to retrieve download link.")
            except Exception as e:
                await update.message.reply_text(f"An error occurred while processing YouTube video: {e}")
        else:
            await update.message.reply_text("Invalid YouTube URL.")

    # Handle Instagram links
    elif 'instagram.com' in text:
        urls = instagram_get_url(text)
        if 'error' in urls:
            await update.message.reply_text(f"Failed to retrieve Instagram media: {urls['error']}")
        else:
            response = ""
            if 'video_url' in urls:
                response += f"Video URL: {urls['video_url']}\n"
            if 'image_url' in urls:
                response += f"Image URL: {urls['image_url']}\n"
            if response:
                await update.message.reply_text(response)
            else:
                await update.message.reply_text("No media found.")
                
    else:
        await update.message.reply_text("Unsupported URL or format.")



def main() -> None:
    updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(...)

updater.start_polling()
updater.idle()

if __name__ == '__main__':
    main()
