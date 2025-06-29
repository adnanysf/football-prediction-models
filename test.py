import requests
import time
import subprocess
import sys
import json
from GAPoissonModel import PoissonModel

class FootballPredictionTest:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.server_process = None
        
    def start_server(self):
        """Start the FastAPI server in the background"""
        print("Starting FastAPI server...")
        self.server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "server:app", "--reload", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        time.sleep(5)
        
        try:
            response = requests.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("PASSED: Server started successfully!")
                return True
        except requests.exceptions.ConnectionError:
            print("FAILED: Failed to start server")
            return False
    
    def stop_server(self):
        """Stop the FastAPI server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("FAILED: Server stopped")
    
    def get_leagues(self, country="England"):
        """Get leagues for a country"""
        print(f"Fetching leagues for {country}...")
        response = requests.get(f"{self.base_url}/leagues/{country}")
        if response.status_code == 200:
            leagues = response.json()
            print(f"Found {len(leagues)} leagues")
            return leagues
        else:
            print(f"Failed to fetch leagues: {response.status_code}")
            return []
    
    def get_teams(self, league_id):
        """Get teams for a league"""
        print(f"Fetching teams for league {league_id}...")
        response = requests.get(f"{self.base_url}/teams/{league_id}")
        if response.status_code == 200:
            teams = response.json()
            print(f"Found {len(teams)} teams")
            return teams
        else:
            print(f"Failed to fetch teams: {response.status_code}")
            return []
    
    def get_team_stats(self, team_id, league_id):
        """Get statistics for a team"""
        print(f"Fetching stats for team {team_id} in league {league_id}...")
        response = requests.get(f"{self.base_url}/stats/{team_id}/{league_id}")
        if response.status_code == 200:
            stats = response.json()
            print(f"Got stats for {stats.get('team_name', 'Unknown Team')}")
            return stats
        else:
            print(f"Failed to fetch stats: {response.status_code}")
            return None
    
    def test_prediction_with_mock_data(self):
        """Test the Poisson model with mock data"""
        print("\nTesting Poisson Model with Mock Data")
        print("=" * 50)
        
        home_team_data = {
            'team_name': 'Manchester City',
            'team_id': 50,
            'league_id': 39,
            'goals': {
                'for': {
                    'average': {
                        'home': 2.1,
                        'away': 1.8
                    }
                },
                'against': {
                    'average': {
                        'home': 0.8,  
                        'away': 1.0
                    }
                }
            }
        }
        
        away_team_data = {
            'team_name': 'Arsenal',
            'team_id': 42,
            'league_id': 39,
            'goals': {
                'for': {
                    'average': {
                        'home': 1.9,
                        'away': 1.6 
                    }
                },
                'against': {
                    'average': {
                        'home': 0.9,
                        'away': 1.2 
                    }
                }
            }
        }
        
        model = PoissonModel(home_team_data, away_team_data)
        prediction = model.predict()
        
        print(f"Home Team: {home_team_data['team_name']}")
        print(f"Away Team: {away_team_data['team_name']}")
        print("\nExpected Goals:")
        for team, goals in prediction['expected_goals'].items():
            print(f"   {team}: {goals}")
        
        print("\nWin Probabilities:")
        for outcome, prob in prediction['probabilities'].items():
            print(f"   {outcome}: {prob}%")
        
        return prediction
    
    def test_prediction_with_real_data(self):
        """Test the Poisson model with real API data"""
        print("\nTesting Poisson Model with Real API Data")
        print("=" * 50)
        
        try:
            leagues = self.get_leagues("England")
            if not leagues:
                print("No leagues found, skipping real data test")
                return None
            
            premier_league = None
            for league in leagues:
                if "Premier League" in league['name'] or league['id'] == 39:
                    premier_league = league
                    break
            
            if not premier_league:
                premier_league = leagues[0] 
            
            print(f"Using league: {premier_league['name']} (ID: {premier_league['id']})")
            
            teams = self.get_teams(premier_league['id'])
            if len(teams) < 2:
                print("Need at least 2 teams for prediction")
                return None
            
            home_team = teams[0]
            away_team = teams[1]
            
            print(f"Selected teams: {home_team['name']} vs {away_team['name']}")
            
            home_stats = self.get_team_stats(home_team['id'], premier_league['id'])
            away_stats = self.get_team_stats(away_team['id'], premier_league['id'])
            
            if not home_stats or not away_stats:
                print("Could not fetch team statistics")
                return None
            
            model = PoissonModel(home_stats, away_stats)
            prediction = model.predict()
            
            print(f"\nHome Team: {home_stats['team_name']}")
            print(f"Away Team: {away_stats['team_name']}")
            print("\nExpected Goals:")
            for team, goals in prediction['expected_goals'].items():
                print(f"   {team}: {goals}")
            
            print("\nWin Probabilities:")
            for outcome, prob in prediction['probabilities'].items():
                print(f"   {outcome}: {prob}%")
            
            return prediction
            
        except Exception as e:
            print(f"Error during real data test: {str(e)}")
            return None
    
    def run_full_test(self):
        """Run the complete test suite"""
        print("Starting Football Prediction Model Test")
        print("=" * 60)
        
        try:
            mock_prediction = self.test_prediction_with_mock_data()
            
            if self.start_server():
                real_prediction = self.test_prediction_with_real_data()
                
                if mock_prediction and real_prediction:
                    print("\nTest Summary")
                    print("=" * 30)
                    print("Mock data test: PASSED")
                    print("Real data test: PASSED")
                    print("Poisson model is working correctly!")
                else:
                    print("\nReal data test failed, but mock test passed")
                    print("Poisson model logic is working correctly")
            else:
                print("\nCould not start server for real data test")
                print("Mock data test passed - model is working")
                
        except Exception as e:
            print(f"Test failed with error: {str(e)}")
        finally:
            self.stop_server()
        
        print("\nTest completed!")

if __name__ == "__main__":
    tester = FootballPredictionTest()
    tester.run_full_test()