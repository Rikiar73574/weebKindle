# Manga Subscription Bot

### Overview
**Manga Subscription Bot** is a Telegram bot designed to provide an automated service for manga enthusiasts. Once subscribed, the bot regularly scans specified sources for new chapters of your favorite manga. If it discovers a newly-released chapter, the bot will:

1. **Download the PDF**: Fetches the PDF file containing the latest manga chapter.
2. **Compress if Necessary**: If the PDF exceeds certain size limits or preferences, the bot compresses the file to ensure it's compatible with Kindle devices.
3. **Send to Kindle**: The bot then sends the compressed PDF to your Kindle device, using the email address defined in your `.env` configuration file.
4. **Update on Telegram**: Simultaneously, the bot sends you a notification via Telegram to keep you informed about the update.

### Bot Workflow
Here's a more detailed workflow of what the Manga Subscription Bot would do behind the scenes:

### Manga Subscription Bot Checklist

- [ ] **Scan for Updates**: Every few hours, the bot scans predefined manga sources based on the user's subscriptions.
- [ ] **Detect New Chapter**: Once a new chapter is detected, the bot proceeds to download it.
- [x] **Handle File Formats**: If the source provides a format other than PDF (e.g., image files), the bot can convert them into a PDF document.
- [x] **Check and Compress**: After obtaining the PDF, if the file size does not meet Kindle's requirements, the bot compresses the PDF to reduce its size without significantly impacting quality.
- [ ] **Dispatch to Kindle**: Using SMTP, the bot emails the PDF document to the user's Kindle email address, which is provided through environment variables in the `.env` file.
- [ ] **Notify User**: Upon successful delivery to Kindle, the bot sends a Telegram message to the user as a confirmation along with details such as the manga title and chapter number.


## Features
- **Search Mangas**: Users can use the `/search` command followed by their query to look for mangas.
- **Subscribe**: Ability to subscribe to manga updates and get notified of new chapters.
- **Receive Updates**: Users can directly receive updates within Telegram.

## Prerequisites
- Python 3.6 or higher installed on your system.
- A Telegram Bot Token. You can obtain one by talking to [BotFather](https://t.me/botfather) on Telegram.
- Ghostscript (gs) installed, required for compressing pdf files


## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/Rikiar73574/weebKindle.git
   cd WeebKindle
   ```

2. Install required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory of the project with the following content:
   ```
   BOT_TOKEN=your_telegram_bot_token_here
   ```

4. Run the bot:
   ```sh
   python main.py
   ```

## Usage
Once the bot is running, you can interact with it on Telegram:

- Use the `/search <query>` command to search for mangas.
- Click the "Subscribe" button to subscribe to a manga.

## Development
This bot uses the `python-telegram-bot` library. Please refer to their [documentation](https://python-telegram-bot.readthedocs.io/) for more details on how to extend and customize the bot.


## License
This project is licensed under the MIT License - see the LICENSE file for details.

---
