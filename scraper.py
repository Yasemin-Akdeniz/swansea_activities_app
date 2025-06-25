import requests
from bs4 import BeautifulSoup
from app import app, db, Activity
import time

def scrape_and_save_activities():
    """
    Scrapes activity data from predefined URLs and saves it to the database.
    """
    print("Starting web scraping...")

    # Define URLs for different scraping strategies
    urls = [
        "https://www.swansea.gov.uk/swanseaprom",
        "https://www.wales247.co.uk/things-to-do-in-swansea-this-half-term" # New URL added here
    ]

    for url in urls:
        try:
            print(f"Attempting to fetch URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')

            print(f"Successfully fetched and parsing data from: {url}")

            # --- Scraping Logic Based on URL ---
            if "swansea.gov.uk" in url:
                # Logic for Swansea Council pages (structured listings)
                activity_items = soup.find_all('div', class_='item--article')
                if not activity_items:
                    activity_items = soup.find_all('div', class_='grid__cell--listitem')
                    
                if not activity_items:
                    print(f"No suitable activity items found on {url}. Skipping this URL.")
                    continue

                activities_saved_count = 0
                for item in activity_items:
                    title_tag = item.find('h2', class_='item__title')
                    description_tag = item.find('div', class_='item__body')
                    link_tag = None
                    if title_tag:
                        link_tag = title_tag.find('a', class_='item__link')

                    title = title_tag.get_text(strip=True) if title_tag else "No Title"
                    description = description_tag.get_text(strip=True) if description_tag else "No Description"
                    source_url = "https://www.swansea.gov.uk" + link_tag['href'] if link_tag and 'href' in link_tag else url

                    date = "See individual page"
                    location = "Swansea Prom Area"
                    cost = "Check website"

                    new_activity = Activity(
                        title=title,
                        description=description,
                        date=date,
                        location=location,
                        cost=cost,
                        source_url=source_url
                    )

                    with app.app_context():
                        db.session.add(new_activity)
                        db.session.commit()
                    activities_saved_count += 1
                
                print(f"'{url}' from Swansea Council: {activities_saved_count} activities saved.")

            elif "wales247.co.uk" in url:
                # Logic for Wales247 article (text-based content)
                print(f"Attempting to scrape article content from {url}")
                
                # Find the main article content block. Common class for this theme.
                # You might need to inspect the page in your browser's developer tools (F12)
                # to find the exact class/tag for the main article content.
                article_content_div = soup.find('div', class_='td-post-content')
                
                if not article_content_div:
                    print(f"Could not find main article content div (td-post-content) on {url}. Trying 'article' tag.")
                    article_content_div = soup.find('article') # Fallback to generic article tag
                    if not article_content_div:
                        print(f"Could not find main article content on {url}. Skipping this URL.")
                        continue

                # Extract all paragraph texts within the article content
                paragraphs = article_content_div.find_all('p')
                article_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

                # For articles, it's harder to get individual structured activities.
                # We'll save the entire article summary as a single entry for now,
                # or you can implement more complex text parsing here.
                
                # Let's try to extract main headings (h2 or strong tags) as potential activities
                # and use surrounding text as description. This is a simplified approach.
                potential_activities = []
                # Look for strong tags which often highlight activity names in such articles
                for strong_tag in article_content_div.find_all('strong'):
                    title = strong_tag.get_text(strip=True)
                    # Get the next sibling paragraph as description, if available
                    description = ""
                    next_p = strong_tag.find_next_sibling('p')
                    if next_p:
                        description = next_p.get_text(strip=True)
                    
                    if title and len(title) > 5 and not title.lower().startswith(("read more", "click here")): # Filter out generic links
                        potential_activities.append({
                            'title': title,
                            'description': description,
                            'source_url': url # Link back to the article itself
                        })

                if not potential_activities:
                    # If no strong-tagged activities found, save the whole article as one "activity"
                    print(f"No specific activities identified by strong tags on {url}. Saving whole article.")
                    article_title_tag = soup.find('h1', class_='entry-title') # Get article main title
                    article_title = article_title_tag.get_text(strip=True) if article_title_tag else "Wales247 Article"
                    
                    new_activity = Activity(
                        title=article_title,
                        description=article_text[:500] + "..." if len(article_text) > 500 else article_text, # Truncate description for brevity
                        date="See article",
                        location="Swansea Area",
                        cost="Check article",
                        source_url=url
                    )
                    with app.app_context():
                        db.session.add(new_activity)
                        db.session.commit()
                    print(f"'{url}' from Wales247: Whole article saved as one activity.")
                else:
                    activities_saved_count = 0
                    for act_data in potential_activities:
                        new_activity = Activity(
                            title=act_data['title'],
                            description=act_data['description'],
                            date="See article", # Dates are often not structured for each item in articles
                            location="Swansea Area", # Location often inferred from article context
                            cost="Check article", # Cost also inferred
                            source_url=act_data['source_url']
                        )
                        with app.app_context():
                            db.session.add(new_activity)
                            db.session.commit()
                        activities_saved_count += 1
                    print(f"'{url}' from Wales247: {activities_saved_count} potential activities saved.")
            
            else:
                print(f"No specific scraping logic for URL: {url}. Skipping.")
                continue

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
        except Exception as e:
            print(f"An error occurred while parsing {url}: {e}")

        time.sleep(2) # Be polite to the server by waiting for 2 seconds between requests.

    print("Web scraping completed.")

# This block executes when the script is run directly (e.g., 'python scraper.py').
if __name__ == '__main__':
    # IMPORTANT: Ensure your Flask application (app.py) is running in a SEPARATE terminal window.
    # This scraper script will connect to the same database instance.
    scrape_and_save_activities()