# Company Brochure Generator

This Python project scrapes a company's website to collect relevant content and generates a company brochure using OpenAI's GPT model. The brochure can be either professional or humorous, depending on user preference.

## Features

- Scrapes website content using `requests` and `BeautifulSoup`
- Identifies relevant links for the brochure (e.g., About, Careers, Products)
- Uses OpenAI's GPT model to generate a structured company brochure
- Supports professional and humorous styles
- Allows saving the generated brochure to a Markdown file

## Prerequisites

Before running this project, ensure you have:

- Python 3.x installed
- An OpenAI API key
- Required Python libraries installed

## Installation

1. Clone this repository:
   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```
   ```

   ```
2. Create a `.env` file and add your OpenAI API key:
   ```sh
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

1. Run the script:
   ```sh
   python brochure_generator.py
   ```
2. Enter the company name and website URL.
3. Choose between a professional or humorous brochure.
4. The generated brochure will be displayed and can be saved as a Markdown file.

## Dependencies

- `requests`
- `beautifulsoup4`
- `openai`
- `python-dotenv`
- `IPython`

## Example

```sh
=== Company Brochure Generator ===
Enter company name: Example Corp
Enter company website URL: https://example.com
Professional or humorous brochure? (p/h): p

=== Generated Brochure ===
# Welcome to Example Corp
...

Save to file? (y/n): y
Brochure saved to example_corp_brochure.md
```

## License

This project is licensed under the MIT License.

## Author

Your Name
