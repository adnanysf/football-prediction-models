from math import exp, factorial

class PoissonModel:
    def __init__(self, home, away):
        self.home = home
        self.away = away

    def poisson_probability(self, k, lamb):
        return (lamb**k * exp(-lamb)) / factorial(k)

    def predict(self):
        homeTeamName = self.home['team_name']
        awayTeamName = self.away['team_name']
        self.home_goals = self.home['goals']['for']['average']['home']
        self.away_goals = self.away['goals']['for']['average']['away']
        self.home_conceded = self.home['goals']['against']['average']['home']
        self.away_conceded = self.away['goals']['against']['average']['away']
        league_average = 1.4
        
        home_attack_strength = self.home_goals / league_average
        away_attack_strength = self.away_goals / league_average
        home_defense_strength = self.home_conceded / league_average
        away_defense_strength = self.away_conceded / league_average
        
        expected_home_goals = home_attack_strength * away_defense_strength * league_average
        expected_away_goals = away_attack_strength * home_defense_strength * league_average
        
        max_goals = 5
        home_win_prob = 0
        draw_prob = 0
        away_win_prob = 0
        
        for home_score in range(max_goals + 1):
            for away_score in range(max_goals + 1):
                home_prob = self.poisson_probability(home_score, expected_home_goals)
                away_prob = self.poisson_probability(away_score, expected_away_goals)
                match_prob = home_prob * away_prob
                
                if home_score > away_score:
                    home_win_prob += match_prob
                elif home_score == away_score:
                    draw_prob += match_prob
                else:
                    away_win_prob += match_prob
        
        return {
            'expected_goals': {
                homeTeamName : round(expected_home_goals, 2),
                awayTeamName : round(expected_away_goals, 2)
            },
            'probabilities': {
                homeTeamName + ' home_win': round(home_win_prob * 100, 1),
                'draw': round(draw_prob * 100, 1),
                awayTeamName + ' away_win': round(away_win_prob * 100, 1)
            }
        }
