# Telegram Channel Scraper

A Python tool for collecting, exporting, and archiving messages and media from Telegram channels.

This project exports Telegram channel content into a structured CSV file. It can export text messages, message metadata, and optionally download media files from accessible Telegram channels.

## Features

- Export Telegram channel messages to CSV
- Export message ID, date, sender ID, message text, and media status
- Optional media downloading
- Supports public and accessible Telegram channels
- Saves exported files inside an `exports/` directory
- Uses environment variables to protect Telegram API credentials
- Simple command-line usage
- Suitable for archiving, research, and content analysis

## Project Structure

```text
telegram-channel-scraper/
│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

## Requirements

- Python 3.8 or higher
- A Telegram account
- Telegram API ID
- Telegram API Hash
- Required Python packages listed in `requirements.txt`

## Prerequisites

Before using this tool, a Telegram API ID and API Hash must be created from Telegram’s official developer website.

1. Go to: https://core.telegram.org/api/obtaining_api_id
2. Log in using a Telegram phone number.
3. Create a new Telegram application.
4. Copy the generated `api_id` and `api_hash`.
5. Add the credentials to the project `.env` file.

> Important: API credentials, phone numbers, authentication codes, and Telethon session files must not be shared publicly or committed to GitHub.

## Installation

Clone the repository:

```bash
git clone https://github.com/ibrahim-zebary/telegram-channel-scraper.git
cd telegram-channel-scraper
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment on Windows:

```bash
.venv\Scripts\activate
```

Activate the virtual environment on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root directory.

On macOS/Linux:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
copy .env.example .env
```

Then add Telegram API credentials inside the `.env` file:

```env
TELEGRAM_API_ID=123456
TELEGRAM_API_HASH=example_api_hash_here
TELEGRAM_PHONE=+1234567890
```

The `.env` file must remain private and must not be committed to GitHub.

## Usage

Export text messages from a Telegram channel:

```bash
python main.py channel_username
```

Export messages with a custom CSV file name:

```bash
python main.py channel_username --output my_export.csv
```

Export messages and download media files:

```bash
python main.py channel_username --media
```

## Output

By default, exported files are saved inside the `exports/` directory.

Example output structure:

```text
exports/
│
├── channel_messages.csv
└── media/
```

The CSV file contains the following columns:

| Column | Description |
|---|---|
| `message_id` | Telegram message ID |
| `date` | Message date and time |
| `sender_id` | Sender ID, if available |
| `message_text` | Message text content |
| `has_media` | Shows whether the message contains media |
| `media_path` | Local path of downloaded media, if media export is enabled |

## First Login

During the first run, Telegram may request a verification code.

After successful login, Telethon creates a local session file. This session file allows future runs without entering the verification code again.

Session files are private and must not be uploaded to GitHub.

## Security Notice

The following files and values must remain private:

- Telegram API ID
- Telegram API Hash
- Telegram phone number
- Telegram login code
- `.env` file
- `.session` files

The included `.gitignore` file prevents sensitive local files from being committed.

## Responsible Use

This tool is intended for archiving, research, and analysis of Telegram channel content.

Usage must comply with Telegram rules, privacy expectations, and applicable laws. Content should only be collected from channels where access is permitted.

This project does not bypass Telegram restrictions. Private channels require proper access from the authenticated Telegram account.

## License

This project is licensed under the MIT License.
