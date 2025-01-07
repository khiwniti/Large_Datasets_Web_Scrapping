import requests
import json
from typing import Dict
import time
from requests.exceptions import RequestException
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WongnaiAPIClient:
    def __init__(self, rate_limit: float = 1.0):
        """
        Initialize the Wongnai API client
        
        Args:
            rate_limit: Minimum time between requests in seconds
        """
        self.session = self._create_session()
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.base_url = "https://www.wongnai.com/_api"

    def _create_session(self) -> requests.Session:
        """Create and configure requests session with appropriate headers"""
        session = requests.Session()
        session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
            "Referer": "https://www.wongnai.com/",
            "Origin": "https://www.wongnai.com"
        })
        return session

    def _rate_limit_request(self):
        """Implement rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def get_businesses(
        self,
        region_id: int = 9681,
        category_group_id: int = 9,
        page_size: int = 10,
        featured: bool = True,
        featured_size: int = 2
    ) -> Dict:
        """
        Fetch business listings from Wongnai API
        
        Args:
            region_id: Region identifier
            category_group_id: Category group identifier
            page_size: Number of results per page
            featured: Whether to include featured listings
            featured_size: Number of featured listings to include
            
        Returns:
            Dict containing the API response
        """
        self._rate_limit_request()
        
        params = {
            "_v": "6.126",
            "locale": "th",
            "regions": region_id,
            "categoryGroupId": category_group_id,
            "rerank": "false",
            "domain": 1,
            "featured": str(featured).lower(),
            "featuredSize": featured_size,
            "page.size": page_size,
            "wref": "sr"
        }

        try:
            response = self.session.get(
                f"{self.base_url}/businesses.json",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return response.json()
        
        except RequestException as e:
            logger.error(f"Error fetching businesses: {str(e)}")
            raise

    def save_response(self, data: Dict, filename: str):
        """Save API response to a JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Data saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise

def main():
    # Initialize client
    client = WongnaiAPIClient(rate_limit=1.0)  # 1 second between requests
    
    try:
        # Fetch business listings
        data = client.get_businesses(
            region_id=9681,
            category_group_id=9,
            page_size=10
        )
        
        # Print some basic information
        if 'businesses' in data:
            print(f"\nFound {len(data['businesses'])} businesses")
            for business in data['businesses']:
                print(f"- {business.get('title', 'No title')} "
                      f"({business.get('businessType', 'No type')})")
                
        # Save the full response to a file
        client.save_response(data, 'wongnai_businesses.json')
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main()
