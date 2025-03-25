import os
import requests
import json
from bs4 import BeautifulSoup
from openai import OpenAI
from IPython.display import Markdown, display, update_display
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key or not api_key.startswith('sk-'):
    raise ValueError("Invalid OpenAI API key. Please check your .env file.")

# Initialize OpenAI client
openai = OpenAI(api_key=api_key)
MODEL = "gpt-4"  # or "gpt-3.5-turbo" if you prefer

# Headers for web scraping
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """Class to represent and scrape a website"""
    
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.body = response.content
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
                
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            self.title = "Error loading page"
            self.text = ""
            self.links = []

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

def get_relevant_links(website):
    """Use OpenAI to identify relevant links for the brochure"""
    system_prompt = """You are provided with a list of links from a webpage. 
    Select the most relevant links for a company brochure (About, Careers, Products, etc.).
    Respond in JSON format with 'links' array containing objects with 'type' and 'url'."""
    
    user_prompt = f"""Here are links from {website.url}. 
    Select relevant ones for a company brochure (skip Terms, Privacy, email links).
    Links:\n""" + "\n".join(website.links)
    
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error getting links: {str(e)}")
        return {"links": []}

def generate_brochure(company_name, url, humorous=False):
    """Generate a brochure for the given company"""
    # Collect website content
    main_page = Website(url)
    content = f"Landing page:\n{main_page.get_contents()}"
    
    # Get relevant links and their content
    links_data = get_relevant_links(main_page)
    print(f"Found relevant links: {links_data}")
    
    for link in links_data.get("links", []):
        try:
            page = Website(link["url"])
            content += f"\n\n{link['type']}:\n{page.get_contents()}"
        except Exception as e:
            print(f"Error processing {link['url']}: {str(e)}")
    
    # Generate brochure
    system_prompt = """You create company brochures from website content. 
    Include company culture, products, and career opportunities."""
    
    if humorous:
        system_prompt = """You create funny, entertaining company brochures. 
        Use humor while including key information about the company."""
    
    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Create a brochure for {company_name} using this content:\n{content}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error generating brochure: {str(e)}")
        return "Failed to generate brochure."

def main():
    """Main function to run the brochure generator"""
    print("=== Company Brochure Generator ===")
    company_name = input("Enter company name: ")
    url = input("Enter company website URL: ")
    style = input("Professional or humorous brochure? (p/h): ").lower()
    
    brochure = generate_brochure(
        company_name, 
        url, 
        humorous=(style == 'h')
    )
    
    print("\n=== Generated Brochure ===\n")
    display(Markdown(brochure))
    
    # Option to save to file
    save = input("\nSave to file? (y/n): ").lower()
    if save == 'y':
        filename = f"{company_name.lower().replace(' ', '_')}_brochure.md"
        with open(filename, 'w') as f:
            f.write(brochure)
        print(f"Brochure saved to {filename}")

if __name__ == "__main__":
    main()