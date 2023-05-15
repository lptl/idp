import requests
from bs4 import BeautifulSoup


def scrape_linkedin_posts(profile_url):
    # Send a GET request to the LinkedIn profile URL
    response = requests.get(profile_url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the post elements on the LinkedIn profile
    post_elements = soup.find_all('div', {'class': 'occludable-update'})

    # Extract the post text from each post element
    post_texts = []
    for post_element in post_elements:
        # Find the post text within the post element
        text_element = post_element.find('span', {'class': 'break-words'})
        if text_element:
            post_texts.append(text_element.text.strip())

    return post_texts



# Example usage
profile_url = 'https://www.linkedin.com/in/dmoskov'
posts = scrape_linkedin_posts(profile_url)

# Print the scraped post texts
for post in posts:
    print(post)
