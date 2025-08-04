# api/howlongtobeat.py

import aiohttp
from .constants import (
    BASE_URL, 
    SEARCH_ENDPOINT, 
    GAME_DETAILS_ENDPOINT,
    DEFAULT_BUILD_ID,
    HEADERS, 
    GAME_DETAILS_HEADERS,
    COOKIES, 
    DEFAULT_SEARCH_OPTIONS
)


class HowLongToBeatAPI:
    """API client for HowLongToBeat.com"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.build_id = DEFAULT_BUILD_ID
    
    async def search_games(self, game_name: str, page: int = 1, size: int = 20) -> list[dict] | None:
        """
        Search for games by name
        
        Args:
            game_name: Name of the game to search for
            page: Page number (default: 1)
            size: Number of results per page (default: 20)
            
        Returns:
            List of game dictionaries or None if failed
        """
        search_terms = game_name.strip().split()
        
        payload = {
            "searchType": "games",
            "searchTerms": search_terms,
            "searchPage": page,
            "size": size,
            "searchOptions": DEFAULT_SEARCH_OPTIONS,
            "useCache": True
        }
        
        url = f"{self.base_url}{SEARCH_ENDPOINT}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=HEADERS, cookies=COOKIES, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_search_results(data)
                    else:
                        print(f"Search failed with status: {response.status}")
                        return None
                        
        except aiohttp.ClientError as e:
            print(f"Search request failed: {e}")
            return None
    
    async def get_game_details(self, game_id: int) -> dict | None:
        """
        Get detailed information for a specific game
        
        Args:
            game_id: The game ID from search results
            
        Returns:
            Game details dictionary or None if failed
        """
        url = f"{self.base_url}{GAME_DETAILS_ENDPOINT.format(build_id=self.build_id, game_id=game_id)}"
        params = {"gameId": game_id}
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=GAME_DETAILS_HEADERS, cookies=COOKIES, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_game_details(data)
                    else:
                        print(f"Game details failed with status: {response.status}")
                        return None
                        
        except aiohttp.ClientError as e:
            print(f"Game details request failed: {e}")
            return None
    
    async def search_and_get_first(self, game_name: str) -> dict | None:
        """
        Search for a game and return detailed info for the first result
        
        Args:
            game_name: Name of the game to search for
            
        Returns:
            Detailed game info dictionary or None if failed
        """
        search_results = await self.search_games(game_name)
        
        if search_results and len(search_results) > 0:
            first_game = search_results[0]
            game_id = first_game.get('id')
            
            if game_id:
                return await self.get_game_details(game_id)
        
        return None
    
    def _parse_search_results(self, data: dict) -> list[dict]:
        """Parse search API response into clean format"""
        games = []
        
        for game in data.get('data', []):
            games.append({
                'id': game.get('game_id'),
                'name': game.get('game_name'),
                'image_url': f"https://howlongtobeat.com/games/{game.get('game_image', '')}" if game.get('game_image') else None,
                'main_hours': self._seconds_to_hours(game.get('comp_main', 0)),
                'plus_hours': self._seconds_to_hours(game.get('comp_plus', 0)),
                'completionist_hours': self._seconds_to_hours(game.get('comp_100', 0)),
                'all_styles_hours': self._seconds_to_hours(game.get('comp_all', 0)),
                'platforms': game.get('profile_platform', ''),
                'release_year': game.get('release_world'),
                'review_score': game.get('review_score')
            })
        
        return games
    
    def _parse_game_details(self, data: dict) -> dict:
        """Parse game details API response into clean format"""
        try:
            game = data['pageProps']['game']['data']['game'][0]
            
            return {
                'id': game.get('game_id'),
                'name': game.get('game_name'),
                'image_url': f"https://howlongtobeat.com/games/{game.get('game_image', '')}" if game.get('game_image') else None,
                'summary': game.get('profile_summary', ''),
                'developer': game.get('profile_dev', ''),
                'publisher': game.get('profile_pub', ''),
                'platforms': game.get('profile_platform', ''),
                'genre': game.get('profile_genre', ''),
                'release_date': game.get('release_world', ''),
                'review_score': game.get('review_score'),
                'times': {
                    'main_story': self._seconds_to_hours(game.get('comp_main', 0)),
                    'main_plus_extras': self._seconds_to_hours(game.get('comp_plus', 0)),
                    'completionist': self._seconds_to_hours(game.get('comp_100', 0)),
                    'all_styles': self._seconds_to_hours(game.get('comp_all', 0))
                },
                'player_counts': {
                    'completed': game.get('count_comp', 0),
                    'backlog': game.get('count_backlog', 0),
                    'playing': game.get('count_playing', 0),
                    'retired': game.get('count_retired', 0),
                    'reviews': game.get('count_review', 0)
                }
            }
        except (KeyError, IndexError, TypeError):
            print("Error parsing game details response")
            return {}
    
    @staticmethod
    def _seconds_to_hours(seconds: int) -> float:
        """Convert seconds to hours, rounded to 1 decimal place"""
        if not seconds:
            return 0.0
        return round(seconds / 3600, 1)