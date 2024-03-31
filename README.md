# RSS Feed Harvest
Basically, this is a Python script that parse news feeds listed in a specific file called "news_feeds.md" and saves the new stuff it finds into a MarkDown file (news_{current_datetime}.md) at the desktop

It makes things super easy to read by sorting all the new entries into different categories, just like how you might organize your stuff into folders on your computer. Plus, it's smart enough to not save the same news more than once.

The first time you run it, it'll grab a bunch of older news too, building up a kind of archive for you. After that, it'll just show you the latest news each day.

## Features

- Grouping Feeds: RSS feeds are grouped based on categories defined by lines starting with "##" in the input file.
- Parsing Feeds: The script extracts news entries from the specified feeds and organizes them by group in the output Markdown file.
- URL checking: Existing URLs from previously parsed feeds in the archive are checked to avoid duplication.
- Date Filtering: Entries from previous years are skipped, ensuring only current-year entries are included.
- Cleaning Text: The script cleans titles and descriptions, removing at least the majority of unwanted characters and formatting issues.

## Dependencies

- feedparser: Used for parsing RSS feeds.
- dateutil.parser: Used for parsing dates from feed entries.

pip install feedparser python-dateutil

## Usage

- Create a file named news_feeds.md with RSS feed URLs grouped by categories using lines starting with "##". An example file with news feeds from the tech sector can be found in this repo.
- Run the script.
- The parsed and organized news entries will be saved to a Markdown file on your desktop in the "RSS/news" subfolder.

## Output

The output file (news_{current_datetime}.md) includes new entries grouped by categories. Each entry includes the title, URL, date, and a cleaned description.
