import race_parser as rp
import numpy as np

def horse_game(race : list, pick: int):
    """
    params:
        race (list): races[racecode], racecode (str)
        pick (int): race index
    """
    if int(race[pick]['rcOrd']) <= 3 and len(race) > 8:
        return 1 # win
    elif int(race[pick]['rcOrd']) <= 2 and len(race) > 7: 
        return 1 # win

    return 0 # lose


def main():
    races = rp.load_races()

    for racecode, race in races.items():
        #print( len(race))
        print(bet_horseracing(race, np.random.randint(len(race))))
