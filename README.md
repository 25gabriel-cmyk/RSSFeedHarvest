<p align="center">
<a href = "https://github.com/25gabriel-cmyk/RSSFeedHarvest" > <img src = "https://github.com/25gabriel-cmyk/RSSFeedHarvest/assets/134001939/386ae276-b801-4e86-b513-7352be3147ad" alt = "tgcf logo"  width=480> </a>
</p>

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

Output sample : 
```
Total New Entries: 15    
Current Date and Time: 2024-04-01 07:50:31

## MASHABLE

***

How to watch the 2024 Japanese Grand Prix online for free
URL: https://mashable.com/uk/deals/japan-gp-f1-live-stream-for-free
Date: 2024-04-01 04:00:00
Description: Watch the 2024 Japanese Grand Prix for free from anywhere in the world.

***

Wordle today: Here's the answer and hints for April 1
URL: https://mashable.com/article/wordle-today-answer-april-1-2024
Date: 2024-04-01 02:00:00
Description: Here's the answer for "Wordle" #1017 on April 1, as well as a few hints, tips, and clues to help you solve it yourself.

## ZDNet

***

Buy Microsoft Visual Studio Pro for just $40 right now
URL: https://www.zdnet.com/article/buy-microsoft-visual-studio-pro-for-just-40-right-now/#ftag=RSSbaffb68
Date: 2024-03-31 19:00:23
Description: Code faster and work smarter with a license to Microsoft Visual Studio Professional 2022, available at a big discount now.

[...]
```
