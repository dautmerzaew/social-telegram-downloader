# Social Telegram Downloader

[![GitHub license](https://img.shields.io/github/license/Bennitenni111/social-telegram-downloader)](https://github.com/Bennitenni111/social-telegram-downloader/blob/main/LICENSE)

This is a Telegram bot that allows users to download videos from TikTok, Instagram, YouTube, and Pinterest. The bot is written in Python and uses the `python-telegram-bot` library along with various API integrations.

## Features

- **TikTok Video Downloads**
  - Supports various TikTok video download methods (snaptik.pro, tiktokio.com, tikmate.cc).
- **Instagram Media Downloads**
  - Extracts video or image URLs from Instagram posts, reels, and stories.
- **YouTube Video Downloads**
  - Fetches direct video download links using RapidAPI.
- **Pinterest Media Downloads**
  - Retrieves images and videos from Pinterest links.

## Requirements

- Python 3.7+
- Telegram Bot Token (from [BotFather](https://core.telegram.org/bots#botfather))
- RapidAPI Key (for YouTube, Instagram, and Pinterest integrations)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Bennitenni111/social-telegram-downloader.git
   cd social-telegram-downloader
   ```

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your API credentials:
   - Open `main.py` and replace the following placeholders:
     - `TOKEN` with your Telegram Bot Token.
     - `RAPIDAPI_KEY` with your RapidAPI key.

4. Run the bot:
   ```bash
   python main.py
   ```

## Usage

- **Start the bot:**
  Send the `/start` command to the bot to receive a welcome message.

- **Download Media:**
  Send a link to the bot for TikTok, Instagram, YouTube, or Pinterest, and it will respond with the download link.

## Example URLs

- TikTok: `https://www.tiktok.com/@username/video/1234567890`
- Instagram: `https://www.instagram.com/p/shortcode/`
- YouTube: `https://www.youtube.com/watch?v=video_id`
- Pinterest: `https://www.pinterest.com/pin/1234567890/`

## File Structure

```
.
├── main.py         # Main bot script
├── requirements.txt # Dependencies
└── README.md       # Project documentation
```

## Libraries Used

- `python-telegram-bot`: For Telegram bot integration
- `requests`: For HTTP requests to APIs
- `bs4` (BeautifulSoup): For web scraping and parsing
- `re`: For regular expressions
- `http.client`: For interacting with APIs

## Notes

- Ensure that your API keys remain private and secure. Do not hardcode them in public repositories.
- The bot requires a stable internet connection to interact with APIs and download media.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Bennitenni111/social-telegram-downloader/blob/main/LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality.

---

### Author
Developed by rahim. Connect on [GitHub](https://github.com/rahimprz).
