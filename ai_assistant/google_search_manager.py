"""
Google Search Integration with Offline Caching
Prioritizes Google as primary online source when not using AI
"""

import requests
import json
import logging
import time
from typing import Dict, Any, List, Optional
from bs4 import BeautifulSoup
import re
from urllib.parse import quote_plus
from .offline_manager import OfflineDataManager

class GoogleSearchManager:
    def __init__(self, offline_data_manager: OfflineDataManager = None):
        """Initialize Google Search Manager"""
        self.offline_data = offline_data_manager or OfflineDataManager()
        self.session = requests.Session()
        
        # Set up headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Search settings
        self.max_results = 5
        self.search_delay = 1  # Delay between searches to be respectful
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("Google Search Manager initialized")

    def search_google(self, query: str, num_results: int = None) -> Dict[str, Any]:
        """
        Search Google and cache results offline
        
        Args:
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Dictionary containing search results
        """
        try:
            # First check offline cache
            cached_result = self.offline_data.get_search_cache(query)
            if cached_result:
                self.logger.info(f"Found cached result for: {query}")
                return {
                    "success": True,
                    "query": query,
                    "response": cached_result['response'],
                    "source": "google_cache",
                    "results": [],
                    "cached": True,
                    "cache_timestamp": cached_result['timestamp']
                }
            
            # Perform Google search
            self.logger.info(f"Searching Google for: {query}")
            
            # Build search URL
            search_url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results or self.max_results}"
            
            # Add delay to be respectful
            time.sleep(self.search_delay)
            
            # Perform search
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Parse results
            results = self._parse_google_results(response.text, query)
            
            if results:
                # Create summary response
                summary = self._create_search_summary(results, query)
                
                # Cache the results
                self.offline_data.cache_online_search(query, summary, "google")
                
                return {
                    "success": True,
                    "query": query,
                    "response": summary,
                    "source": "google",
                    "results": results,
                    "cached": False
                }
            else:
                return {
                    "success": False,
                    "error": "No search results found",
                    "query": query,
                    "source": "google"
                }
                
        except requests.RequestException as e:
            self.logger.error(f"Google search request failed: {e}")
            return {
                "success": False,
                "error": f"Search request failed: {str(e)}",
                "query": query
            }
        except Exception as e:
            self.logger.error(f"Google search failed: {e}")
            return {
                "success": False,
                "error": f"Search failed: {str(e)}",
                "query": query
            }

    def _parse_google_results(self, html_content: str, query: str) -> List[Dict[str, Any]]:
        """Parse Google search results from HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            results = []
            
            # Find search result containers
            search_results = soup.find_all('div', class_='g')
            
            for result in search_results[:self.max_results]:
                try:
                    # Extract title
                    title_elem = result.find('h3')
                    title = title_elem.get_text() if title_elem else ""
                    
                    # Extract URL
                    link_elem = result.find('a')
                    url = link_elem.get('href') if link_elem else ""
                    
                    # Extract snippet
                    snippet_elem = result.find('span', class_='aCOpRe') or result.find('div', class_='VwiC3b')
                    snippet = snippet_elem.get_text() if snippet_elem else ""
                    
                    if title and url and snippet:
                        # Calculate relevance score
                        relevance = self._calculate_google_relevance(query, title, snippet)
                        
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet,
                            'relevance': relevance
                        })
                        
                except Exception as e:
                    self.logger.warning(f"Error parsing individual search result: {e}")
                    continue
            
            # Sort by relevance
            results.sort(key=lambda x: x['relevance'], reverse=True)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error parsing Google results: {e}")
            return []

    def _calculate_google_relevance(self, query: str, title: str, snippet: str) -> float:
        """Calculate relevance score for Google search results"""
        score = 0.0
        query_words = query.lower().split()
        
        # Title relevance (highest weight)
        title_lower = title.lower()
        for word in query_words:
            if word in title_lower:
                score += 2.0
        
        # Snippet relevance
        snippet_lower = snippet.lower()
        for word in query_words:
            if word in snippet_lower:
                score += 1.0
        
        # Boost for exact phrase matches
        if query.lower() in title_lower:
            score += 3.0
        if query.lower() in snippet_lower:
            score += 2.0
        
        return score

    def _create_search_summary(self, results: List[Dict[str, Any]], query: str) -> str:
        """Create a summary from Google search results"""
        if not results:
            return "No relevant information found."
        
        # Use the most relevant results
        top_results = results[:3]
        
        summary_parts = []
        summary_parts.append(f"Based on Google search for '{query}':")
        
        for i, result in enumerate(top_results, 1):
            snippet = result['snippet']
            # Clean up the snippet
            snippet = re.sub(r'\s+', ' ', snippet).strip()
            if len(snippet) > 150:
                snippet = snippet[:147] + "..."
            
            summary_parts.append(f"{i}. {snippet}")
        
        # Add source information
        if len(results) > 3:
            summary_parts.append(f"\n(Found {len(results)} total results from Google)")
        
        return "\n\n".join(summary_parts)

    def search_specific_site(self, query: str, site: str) -> Dict[str, Any]:
        """Search within a specific site using Google"""
        site_query = f"site:{site} {query}"
        return self.search_google(site_query)

    def search_academic(self, query: str) -> Dict[str, Any]:
        """Search for academic information using Google Scholar approach"""
        academic_query = f"{query} academic research scholarly"
        return self.search_google(academic_query)

    def search_definition(self, term: str) -> Dict[str, Any]:
        """Search for definition using Google"""
        definition_query = f"define {term}"
        return self.search_google(definition_query)

    def search_news(self, query: str) -> Dict[str, Any]:
        """Search for recent news using Google"""
        news_query = f"{query} news recent"
        return self.search_google(news_query)

    def get_wikipedia_summary(self, topic: str) -> Dict[str, Any]:
        """Get Wikipedia summary via Google search"""
        wikipedia_query = f"site:wikipedia.org {topic}"
        result = self.search_google(wikipedia_query, num_results=1)
        
        if result.get('success') and result.get('results'):
            # Try to get more detailed content from Wikipedia
            wiki_result = result['results'][0]
            try:
                # Extract Wikipedia content
                wiki_content = self._extract_wikipedia_content(wiki_result['url'])
                if wiki_content:
                    # Cache the detailed content
                    self.offline_data.cache_online_search(
                        f"wikipedia {topic}", 
                        wiki_content, 
                        "wikipedia"
                    )
                    result['response'] = wiki_content
                    result['detailed'] = True
            except Exception as e:
                self.logger.warning(f"Could not extract detailed Wikipedia content: {e}")
        
        return result

    def _extract_wikipedia_content(self, url: str) -> Optional[str]:
        """Extract content from Wikipedia page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the first few paragraphs
            content_div = soup.find('div', class_='mw-parser-output')
            if content_div:
                paragraphs = content_div.find_all('p')
                content_parts = []
                
                for p in paragraphs[:3]:  # First 3 paragraphs
                    text = p.get_text().strip()
                    if len(text) > 50:  # Skip very short paragraphs
                        content_parts.append(text)
                
                if content_parts:
                    return "\n\n".join(content_parts)
            
            return None
            
        except Exception as e:
            self.logger.warning(f"Error extracting Wikipedia content: {e}")
            return None

    def smart_search(self, query: str, prefer_offline: bool = True) -> Dict[str, Any]:
        """
        Smart search that tries offline first, then Google
        
        Args:
            query: Search query
            prefer_offline: Whether to prefer offline results
            
        Returns:
            Search results
        """
        # First try offline if preferred
        if prefer_offline:
            offline_results = self.offline_data.search_offline_data(query)
            if offline_results:
                best_result = offline_results[0]
                return {
                    "success": True,
                    "query": query,
                    "response": best_result['answer'],
                    "source": "offline",
                    "confidence": best_result['confidence'],
                    "offline_first": True
                }
        
        # Try cached Google results
        cached_result = self.offline_data.get_search_cache(query)
        if cached_result and cached_result['source'] == 'google':
            return {
                "success": True,
                "query": query,
                "response": cached_result['response'],
                "source": "google_cache",
                "cached": True
            }
        
        # Perform new Google search
        return self.search_google(query)

    def batch_search_and_cache(self, queries: List[str]) -> Dict[str, Any]:
        """Batch search multiple queries and cache them"""
        results = {}
        
        for query in queries:
            try:
                result = self.search_google(query)
                results[query] = result
                
                # Add delay between searches
                time.sleep(self.search_delay * 2)  # Longer delay for batch operations
                
            except Exception as e:
                self.logger.error(f"Error in batch search for '{query}': {e}")
                results[query] = {
                    "success": False,
                    "error": str(e),
                    "query": query
                }
        
        return {
            "batch_results": results,
            "total_queries": len(queries),
            "successful_queries": sum(1 for r in results.values() if r.get('success'))
        }

    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics"""
        offline_stats = self.offline_data.get_statistics()
        
        return {
            "cached_searches": offline_stats.get('cached_searches', 0),
            "most_accessed_searches": offline_stats.get('most_accessed', []),
            "knowledge_entries": offline_stats.get('knowledge_entries', 0),
            "categories": offline_stats.get('categories', [])
        }