import re
import numpy as np
import random
import math

def main():
  details_list = parse_msg()
  timeslots = generate_timeslots(details_list)
  player_teams = generate_teams(timeslots)
  export_teams(player_teams)

def parse_msg():
  print('Parsing Message...')

  f = open('msg.csv', 'r')
  return f.readlines()

# Details in format ["name, time-time", "name, time-time"]
def generate_timeslots(details):
  print('Generating Teams...')

  timeslots = {}
  for person in details:
    p = person.split(',')
    name = p[0]
    # Assume all times are in PM lol i lazy code the AM thing
    times = re.sub(r'[pmPM]', '', p[1]) # format: time-time (e.g. 9-11). Some ppl may put 9pm-11pm, 9-11pm etc. so need to trim.

    time_range = range(int(times.split('-')[0]), int(times.split('-')[1]))

    for time in time_range:
      time = str(time)
      if time not in timeslots:
        timeslots[time] = []
      timeslots[time].append(name)
  return timeslots

def generate_teams(timeslots):
  # Each row should be list of: [name, timeslot, team]
  final_list = []
  for time, players in timeslots.items():
    print(f"Generating teams for {time}pm timeslot...")
    print(f"Number of players is: {len(players)}")
    # Randomize player order
    random.shuffle(players)
    np_players = np.array(players)
    teams = np.array_split(np_players, calculate_num_teams(players))
    print(f"Generated {len(teams)} teams of sizes: ", end='')
    for team in teams:
      print(len(team), end=' ')
    print('')

    for team, members in enumerate(teams):
      for member in members:
        final_list.append([member, str(time), str(team + 1)])
  # print(final_list)
  return final_list
    

def calculate_num_teams(players):
  num = math.ceil(len(players) / 5)
  if num % 2 != 0:
    num += 1
  return num

# Each row should be list of: [name, timeslot, team]
def export_teams(player_teams):
  print('Exporting Teams...')

  f = open('teams.csv', 'w')
  f.write(u'username, timeslot, team\n')
  for player in player_teams:
    f.write(', '.join(player) + "\n")
  f.close()

main()
