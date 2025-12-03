"""
Academic Content Search and Retrieval module with OpenAI and Google Scholar integration
"""
import os
from scholarly import scholarly

def search_content(query):
    """
    Search Google Scholar for academic content
    """
    try:
        print(f"[Search] Searching Google Scholar for: {query}")

        # Search Google Scholar
        search_query = scholarly.search_pubs(query)

        # Get first result
        result = next(search_query, None)

        if result:
            title = result.get('bib', {}).get('title', 'No title')
            abstract = result.get('bib', {}).get('abstract', 'No abstract available')
            authors = result.get('bib', {}).get('author', 'Unknown authors')
            year = result.get('bib', {}).get('pub_year', 'Unknown year')

            # Format response
            response = f"Title: {title}\n"
            response += f"Authors: {authors}\n"
            response += f"Year: {year}\n"
            response += f"Abstract: {abstract[:300]}..." if len(abstract) > 300 else f"Abstract: {abstract}"

            print(f"[Search] Google Scholar result found")
            return response
        else:
            print(f"[Search] No results found")
            return f"Sorry, could not find academic papers for '{query}'."

    except Exception as e:
        print(f"[Search] Error: {e}")
        return f"Sorry, could not search Google Scholar for '{query}'. Error: {str(e)}"

def search_with_openai(query, api_key=None):
    """
    Use OpenAI to enhance search results and provide intelligent responses
    """
    try:
        from openai import OpenAI

        # Get API key from environment or parameter
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')

        if not api_key or api_key == "your-openai-api-key-here":
            return "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file"

        client = OpenAI(api_key=api_key)

        # Create prompt for OpenAI
        prompt = f"""You are an academic research assistant. Please provide a comprehensive explanation about: {query}

Include:
1. A clear definition or explanation
2. Key concepts and theories
3. Important researchers or contributors in this field
4. Real-world applications or examples
5. Recent developments or current research trends

Keep the response educational and accessible for students."""

        print(f"[OpenAI] Sending query to OpenAI...")

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful academic research assistant for students with visual impairments."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )

        result = response.choices[0].message.content
        print(f"[OpenAI] Response received")
        return result

    except Exception as e:
        print(f"[OpenAI] Error: {e}")
        return f"Sorry, could not get response from OpenAI. Error: {str(e)}"
