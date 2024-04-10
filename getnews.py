# RSS Feed Harvest: Python script designed to parse news feeds from a specified file (news_feeds.md) 
# and save new entries into a Markdown file (news_{current_datetime}.md) at the desktop.

import feedparser
import os
from datetime import datetime
from dateutil import parser
import re
import html
import requests
import logging

# Function to read RSS feeds from a file
def read_rss_feeds_from_file(file_path):
    rss_feeds = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            rss_feeds.append(line.strip())
    return rss_feeds

# Function to get the group name from a line starting with "##"
def get_group_name(line):
    return line.strip(" #")

# Function to parse the news feeds and group them
def parse_news_feeds(file_path):
    grouped_feeds = {}
    current_group = None

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line.startswith("##"):
                current_group = get_group_name(line)
                grouped_feeds[current_group] = []
            elif line.startswith("http"):
                if current_group:
                    grouped_feeds[current_group].append(line)

    return grouped_feeds

# Function to get the current date and time as a formatted string
def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to create a folder if it doesn't exist
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Function to remove soft hyphens from text
def remove_soft_hyphens(text):
    return text.replace("\xad", "")

# Function to clean the title text
def clean_title(title):
    # Remove new lines
    title = title.replace("\n", "")

    # Replace "*in" with ":in"
    title = title.replace('*in', ':in')

    # Replace non-breaking space characters with regular space
    title = title.replace("\xa0", " ")

    # Shorten after 300 characters with "[...]"
    title = title[:300] + "[...]" if len(title) > 300 else title

    return title

# Function to clean the description text
def clean_description(description):

    # Remove HTML tags and other unwanted HTML entities
    description = re.sub(r'<[^>]*>|\[link\]|\[comments\]|\[...\]|&#\d+;|&[^;]+;', '', description)
    
    # Replace "*in" with ":in"
    description = description.replace('*in', ':in')
    
    # Replace consecutive spaces with a single space
    description = re.sub(r'\s+', ' ', description)

    # Replace non-breaking space characters with regular space
    description = description.replace("\xa0", " ")

    # Remove leading and trailing spaces
    description = description.strip()
    
    return description

# Prompt the user in the terminal
print("\nWelcome to RSS Feed Harvest.\nParsing RSS-feeds:")

# Function to read existing URLs from MD files in the output folder
def read_existing_urls(output_folder):
    existing_urls = set()
    for root, _, files in os.walk(output_folder):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as md_file:
                    text = md_file.read()
                    urls = re.findall(r'URL:\s*([^\n]+)', text)
                    existing_urls.update(urls)
    return existing_urls

# Get the news feeds from the "news_feeds.md" file
news_feeds = parse_news_feeds("news_feeds.md")

# Get the current date and time for the output
current_datetime = get_current_datetime()

# Extract the current year from the current date
current_year = datetime.now().year

# Desktop path
desktop_path = os.path.expanduser("~/Desktop")

# Update the subfolder variable to "RSS/news"
subfolder = "RSS/news"

# Update the subfolder_path to create the subfolder within "RSS" on the desktop
subfolder_path = os.path.join(desktop_path, subfolder)

# Ensure the subfolder exists, create it if it doesn't
if not os.path.exists(subfolder_path):
    os.makedirs(subfolder_path)

# Output file name within the subfolder
output_file = os.path.join(subfolder_path, f"news_{current_datetime}.md")

# Set to store unique URLs from new matches
unique_urls = set()

# Read existing URLs from MD files in the output folder
existing_urls = read_existing_urls(subfolder_path)

# Open the output file for writing
with open(output_file, "w", encoding="utf-8") as file:

    # Initialize a count for new entries
    new_entries_count = 0

    # Write the total new entries count at the beginning with initial pad of spaces
    file.write(f"Total New Entries:      ")

    # Write the date at the beginning of the file
    file.write(f"\nCurrent Date and Time: {current_datetime}\n\n")

    # Iterate through the grouped news feeds
    for group, feeds in news_feeds.items():
        # Write the group name as a subheading
        file.write(f"## {group}\n\n")
        print(f"\n{group}")

        # Iterate through the RSS feeds in the current group
        for rss_feed in feeds:
            # Extract and print only the domain from the URL
            domain = re.search(r"https?://(?:www\.)?(.+?)/", rss_feed)
            if domain:
                domain = domain.group(1)
                print(f"... {domain}")

            try:
                # Parse the feed
                feed = feedparser.parse(rss_feed)
                status_code = feed.status

                if 400 <= status_code < 600:
                    # Print a warning message for 4xx and 5xx status codes
                    print(f"\n{rss_feed} returned HTTP status code {status_code}\n")
                else:
                    # Feed parsing was successful or is a redirection (3xx), continue processing entries
                    for entry in feed.entries:
                        entry_link = entry.link            

                        # Remove tracking parameters from URLs
                        entry_link = re.sub(r'\?utm_source=[^&]+&utm_medium=[^&]+&utm_campaign=[^&]+|\?wt_mc=rss.red.unbekannt.unbekannt.atom.beitrag.beitrag|#ref=rss', '', entry_link)

                        # Check if the URL is unique in the new matches and not in existing URLs
                        if entry_link not in unique_urls and entry_link not in existing_urls:
                            unique_urls.add(entry_link)

                            # Try to parse the date using dateutil.parser
                            try:
                                entry_date = parser.parse(entry.published)
                            except (ValueError, AttributeError):
                                entry_date = None

                            # Initialize entry_date_str as "N/A" if entry_date is None, or format it as a string if available
                            entry_date_str = "N/A" if entry_date is None else entry_date.strftime("%Y-%m-%d %H:%M:%S")

                            # Check if the entry_date is available and in the current year or newer
                            if entry_date is not None:
                                entry_year = entry_date.year
                                if entry_year < current_year:
                                    continue  # Skip entries from previous years

                            # Initialize other attributes as empty strings
                            description = entry.get("description", "")
                            title = entry.get("title", "")  # Get the title of the feed entry

                            # Increment the count of new entries
                            new_entries_count += 1

                            # Clean the title text
                            title = clean_title(title)

                            # Clean the description text
                            description = clean_description(description)

                            # Truncate the description to 500 characters or less
                            description = description[:500] + "[...]" if len(description) > 500 else description

                            # Add three asterisks before each entry in the output file
                            file.write("***\n\n")

                            # Write entry details
                            file.write(f"{remove_soft_hyphens(title)}\n")
                            file.write(f"URL: {remove_soft_hyphens(entry_link)}\n")

                            # Add the date if available (or leave it as "N/A" if it's not available)
                            file.write(f"Date: {entry_date_str}\n")
                            
                            # Add the cleaned description to the output
                            file.write(f"Description: {remove_soft_hyphens(description)}\n\n")

            except Exception as e:
                # Handle other exceptions (e.g., network issues)
                print(f"\nError parsing {rss_feed}: {e}\n")

    # Go back to the beginning of the file
    file.seek(0)

    # Convert the count to a string
    count_str = str(new_entries_count)

    # Rewrite the total new entries count at the beginning without adding extra spaces
    file.write(f"Total New Entries: {count_str}")

# Count the total number of feeds
with open("news_feeds.md", "r") as file:
    rss_feeds = [line.strip() for line in file if not line.strip().startswith("##")]

# Initialize counters and lists for unresponsive feeds and their reasons
total_feeds = len(rss_feeds)

# Configure logging
logging.basicConfig(filename='rss_parser.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

# Function to log errors
def log_error(feed_url, error):
    logging.error(f"Error parsing {feed_url}: {error}")

# Inside the main loop where feed parsing occurs
try:
    feed = feedparser.parse(rss_feed)
    status_code = feed.status

    if 400 <= status_code < 600:
        log_error(rss_feed, f"HTTP status code {status_code}")
    else:
        # Feed parsing was successful or is a redirection (3xx), continue processing entries
        for entry in feed.entries:
            # Parsing and processing entries
except Exception as e:
    log_error(rss_feed, e)

# Prompt the user with the number of feeds checked
print(f"\n[{total_feeds}] feeds checked.")
print(f"\n[{new_entries_count}] new entries found and saved to:\n{output_file}\n")
