import logging
import os
import re

import html2text
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlunparse, ParseResult, unquote
import time


def get_unique_urls_from_base_page(start_url):
    base_url = urlsplit(start_url)
    current_url = start_url
    all_links = set()
    visited_urls = set()

    while current_url not in visited_urls:
        print(f"Scraping: {current_url}")
        visited_urls.add(current_url)

        response = requests.get(current_url)
        if response.status_code != 200:
            print(f"Failed to fetch {current_url}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links in the main content area
        content_div = soup.find("div", class_="mw-allpages-body")
        if content_div:
            links = content_div.find_all("a")
            for link in links:
                href = link.get("href")
                if href:
                    all_links.add(urljoin("https://" + base_url.netloc, href))

        # Find the next page link
        nav_div = soup.find("div", class_="mw-allpages-nav")
        if nav_div:
            # Find all links in the nav div
            # Get the last link if there are multiple (it will be "Next page")
            # or the only link if there's just one

            nav_links = nav_div.find_all("a")
            next_link = nav_links[-1] if nav_links else None
            if next_link and "Next page" in next_link.text:
                current_url = urljoin("https://" + base_url.netloc, next_link["href"])
            else:
                print("No more pages to scrape")
                break
        else:
            print("Navigation element not found")
            break

    return list(all_links)


def clean_filename(filename):
    # Then remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*\']', "_", filename)

    # Replace multiple underscores with a single one
    filename = re.sub(r"_+", "_", filename)

    return filename


def clean_markdown_content(content):

    # Remove image markdown syntax
    content = re.sub(r"!\[.*?]\(.*?\)", "", content)
    # Remove empty lines that might be left after removing images
    content = re.sub(r"\n\s*\n\s*\n" "", "\n\n", content)
    return content


def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    for img in soup.find_all("img"):
        img.decompose()

    for figure in soup.find_all("figure"):
        figure.decompose()

    for navbox in soup.find_all("table", class_="navbox"):
        navbox.decompose()

    converter = html2text.HTML2Text()
    converter.ignore_images = True
    converter.ignore_links = False
    converter.ignore_tables = False
    converter.body_width = 0  # Don't wrap lines

    # Convert HTML to Markdown
    raw_markdown = converter.handle(str(soup))
    return raw_markdown


def scrape_wiki_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the main content div
            content_div = soup.find("div", {"class": "mw-parser-output"})

            if content_div:
                # Convert the content to markdown
                markdown_content = html_to_markdown(str(content_div))
                return markdown_content
            else:
                return None
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None


def main():
    start_url = "https://reddead.fandom.com/wiki/Special:AllPages"

    urls = get_unique_urls_from_base_page(start_url)

    print(f"\nTotal unique links found: {len(urls)}")

    # Save to file
    # with open("wiki_links.txt", "w", encoding="utf-8") as f:
    #     for link in links:
    #         f.write(f"{link}\n")

    # Create output directory if it doesn't exist
    output_dir = "rdr2_fandom_pages"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Read URLs from file
    # with open("wiki_links.txt", "r", encoding="utf-8") as f:
    #     urls = f.read().splitlines()

    urls.sort()
    for i, url in enumerate(urls):
        # url = "https://reddead.fandom.com/wiki/Arthur_Morgan"
        # Extract page title from URL
        try:
            page_name = url.split("/")[-1]
            clean_name = clean_filename(page_name)
            output_file = os.path.join(output_dir, f"{clean_name}.md")

            # Skip if file already exists
            if os.path.exists(output_file):
                print(f"Skipping {page_name} - already exists")
                continue

            print(f"Processing {i+1}/{len(urls)}: {page_name}")

            # Scrape and convert content
            raw_markdown = scrape_wiki_page(url)
            clean_markdown = clean_markdown_content(raw_markdown)
            if clean_markdown:
                # Save to file
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(clean_markdown)
                print(f"Saved {output_file}")
        except Exception as e:
            logging.exception(f"Error scraping {url}: {str(e)}")


if __name__ == "__main__":
    main()
