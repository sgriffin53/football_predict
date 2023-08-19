import csv
import numpy as np
from scipy.stats import poisson
class DataStruct:
    def __init__(self):
        self.totHomeGoals = 0
        self.totAwayGoals = 0
        self.avgHomeGoalsPerMatch = 0
        self.avgAwayGoalsPerMatch = 0
        self.totMatches = 0

class TeamStruct:
    def __init__(self):
        self.avgHomeGoalsScored = 0
        self.avgHomeGoalsAllowed = 0
        self.totHomeGoalsScored = 0
        self.totHomeGoalsAllowed = 0
        self.avgAwayGoalsScored = 0
        self.avgAwayGoalsAllowed = 0
        self.totAwayGoalsScored = 0
        self.totAwayGoalsAllowed = 0
        self.matches = 0
        self.homeMatches = 0
        self.awayMatches = 0


def get_data(dataStruct, teamDict):
    totLeagueHomeGoals = 0
    totLeagueAwayGoals = 0
    totMatches = 0
    i = 0
    with open('data/final_dataset.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
     #       print(row[2])
            if row[4] == 'FTHG': continue
            totHomeGoals = int(row[4])
            totAwayGoals = int(row[5])
            totLeagueHomeGoals += totHomeGoals
            totLeagueAwayGoals += totAwayGoals
            homeTeam = row[2]
            awayTeam = row[3]
            if homeTeam not in teamDict:
                teamDict[homeTeam] = TeamStruct()
            if awayTeam not in teamDict:
                teamDict[awayTeam] = TeamStruct()
            teamDict[homeTeam].totHomeGoalsScored += totHomeGoals
            teamDict[homeTeam].totHomeGoalsAllowed += totAwayGoals
            teamDict[awayTeam].totAwayGoalsScored += totAwayGoals
            teamDict[awayTeam].totAwayGoalsAllowed += totHomeGoals
            teamDict[homeTeam].matches += 1
            teamDict[awayTeam].matches += 1
            teamDict[homeTeam].homeMatches += 1
            teamDict[awayTeam].awayMatches += 1
            totMatches += 1
            i += 1
    dataStruct.totHomeGoals = totLeagueHomeGoals
    dataStruct.totAwayGoals = totLeagueAwayGoals
    dataStruct.avgHomeGoalsPerMatch = totLeagueHomeGoals / totMatches
    dataStruct.avgAwayGoalsPerMatch = totLeagueAwayGoals / totMatches
    dataStruct.totMatches = totMatches
    for team in teamDict.keys():
        teamDict[team].avgHomeGoalsScored = teamDict[team].totHomeGoalsScored / teamDict[team].matches
        teamDict[team].avgHomeGoalsAllowed = teamDict[team].totHomeGoalsAllowed / teamDict[team].matches
        teamDict[team].avgAwayGoalsScored = teamDict[team].totAwayGoalsScored / teamDict[team].matches
        teamDict[team].avgHomeGoalsAllowed = teamDict[team].totAwayGoalsAllowed / teamDict[team].matches
    #print(dataStruct, teamDict)
    return dataStruct, teamDict
    pass

def predict_result(home_team, away_team, dataStruct, teamDict):
    homeGoalAvg = (teamDict[home_team].totHomeGoalsScored) / teamDict[home_team].homeMatches
    awayGoalAvg = (teamDict[away_team].totAwayGoalsScored) / teamDict[away_team].awayMatches
    homeAllowedAvg = (teamDict[home_team].totHomeGoalsAllowed) / teamDict[home_team].homeMatches
    awayAllowedAvg = (teamDict[away_team].totAwayGoalsAllowed) / teamDict[away_team].awayMatches
    homeAllowedAvg = teamDict[home_team].totHomeGoalsAllowed / teamDict[home_team].homeMatches
    awayAllowedAvg = teamDict[away_team].totHomeGoalsAllowed / teamDict[away_team].awayMatches
    leagueGoalAvg = (dataStruct.totHomeGoals + dataStruct.totAwayGoals) / dataStruct.totMatches
    leagueGoalAvgHome = dataStruct.totHomeGoals / dataStruct.totMatches
    leagueGoalAvgAway = dataStruct.totAwayGoals / dataStruct.totMatches
    homeAttack = homeGoalAvg / leagueGoalAvgHome
    awayAttack = awayGoalAvg / leagueGoalAvgAway
    homeDefence = homeAllowedAvg / leagueGoalAvgHome
    awayDefence = awayAllowedAvg / leagueGoalAvgAway
    mostLikelyScore = "-1"
    mostLikelyValue = -9999
    homeGoalExpectency = homeAttack * awayDefence
    awayGoalExpectency = awayAttack * homeDefence
    for i in range(0, 6):
        for j in range(0,6):
            prob = poisson.pmf(i, homeGoalExpectency) * poisson.pmf(j, awayGoalExpectency) * 100
            if prob > mostLikelyValue:
                mostLikelyScore = str(i) + " - " + str(j)
                mostLikelyValue = prob
    return mostLikelyScore, mostLikelyValue
    pass

teamDict = {} # map team names to structs
dataStruct = DataStruct()
dataStruct, teamDict = get_data(dataStruct, teamDict)
teams = ["Liverpool vs Bournemouth",
         "Wolves vs Brighton",
         "Tottenham vs Man United",
         "Man City vs Newcastle",
         "Aston Villa vs Everton",
         "West Ham vs Chelsea",
         "Crystal Palace vs Arsenal"]
tot_prob = 1
for team in teams:
    home_team = team.split(" vs ")[0]
    away_team = team.split(" vs ")[1]
    pred_score, pred_prob = predict_result(home_team, away_team, dataStruct, teamDict)
    tot_prob *= (pred_prob / 100)
    print(home_team + " vs " + away_team + ": " + pred_score + " (" + str(round(pred_prob,2)) + "%)")
print("Probability: 1/" + str(int(1 / tot_prob)))