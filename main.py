import os
import csv
import argparse
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient

# Load environment variables from the .env file
load_dotenv()

# Telegram API credentials
# Values must be stored in .env, not hardcoded in the source code
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE_NUMBER = os.getenv("TELEGRAM_PHONE")

# Telethon session name
# A local .session file is created after the first successful login
SESSION_NAME = "telegram_channel_scraper"

# Default export directory
EXPORT_DIR = Path("exports")


def validate_environment() -> None:
    """Validate required environment variables."""
    missing_values = []

    if not API_ID:
        missing_values.append("TELEGRAM_API_ID")
    if not API_HASH:
        missing_values.append("TELEGRAM_API_HASH")
    if not PHONE_NUMBER:
        missing_values.append("TELEGRAM_PHONE")

    if missing_values:
        missing = ", ".join(missing_values)
        raise ValueError(f"Missing required environment variable(s): {missing}")


def clean_channel_username(channel: str) -> str:
    """
    Normalize Telegram channel username.

    Accepted formats:
    - channelname
    - @channelname
    - https://t.me/channelname
    - http://t.me/channelname
    """
    channel = channel.strip()

    if channel.startswith("https://t.me/"):
        channel = channel.replace("https://t.me/", "", 1)
    if channel.startswith("http://t.me/"):
        channel = channel.replace("http://t.me/", "", 1)
    if channel.startswith("@"):
        channel = channel[1:]

    return channel.rstrip("/")


async def export_channel_content(
    channel_username: str,
    output_file: str,
    download_media: bool = False,
    limit: int | None = None,
) -> None:
    """
    Export Telegram channel messages into a CSV file.

    Parameters:
        channel_username: Telegram channel username
        output_file: CSV output file name
        download_media: Whether media files should be downloaded
        limit: Optional maximum number of messages to export
    """
    validate_environment()
    channel_username = clean_channel_username(channel_username)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    media_dir = EXPORT_DIR / "media"
    if download_media:
        media_dir.mkdir(parents=True, exist_ok=True)

    # Prevent directory traversal by keeping only the file name
    output_path = EXPORT_DIR / Path(output_file).name

    client = TelegramClient(SESSION_NAME, int(API_ID), API_HASH)

    # Start the Telegram client
    # On first login, Telegram may request a verification code
    await client.start(phone=PHONE_NUMBER)

    try:
        channel = await client.get_entity(channel_username)

        with open(output_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "message_id",
                "date",
                "sender_id",
                "message_text",
                "has_media",
                "media_path",
            ])

            async for message in client.iter_messages(channel, reverse=True, limit=limit):
                message_text = message.text or ""
                has_media = bool(message.media)
                media_path = ""

                if download_media and has_media:
                    downloaded_file = await message.download_media(file=str(media_dir))
                    media_path = downloaded_file if downloaded_file else ""

                writer.writerow([
                    message.id,
                    message.date.isoformat() if message.date else "",
                    message.sender_id if message.sender_id else "",
                    message_text,
                    has_media,
                    media_path,
                ])

        print(f"Export completed successfully: {output_path}")

    except Exception as error:
        print(f"Export failed: {error}")

    finally:
        await client.disconnect()


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Export messages and optional media from Telegram channels."
    )
    parser.add_argument(
        "channel",
        help="Telegram channel username, @username, or https://t.me/channelname",
    )
    parser.add_argument(
        "--output",
        default="channel_messages.csv",
        help="CSV output file name. Default: channel_messages.csv",
    )
    parser.add_argument(
        "--media",
        action="store_true",
        help="Download media files from channel messages",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of messages to export. Default: export all messages",
    )
    return parser.parse_args()


async def main() -> None:
    """Main application entry point."""
    args = parse_arguments()
    await export_channel_content(
        channel_username=args.channel,
        output_file=args.output,
        download_media=args.media,
        limit=args.limit,
    )


if __name__ == "__main__":
    asyncio.run(main())
