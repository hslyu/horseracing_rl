#!/usr/bin/env python
# coding: utf-8
# Auther: Hyeonsu Lyu
# Contact: hslyu4@gmail.com

# ## Fetch XML data from data.go.kr

# In[397]:


import requests
import json
import xmltodict


# In[436]:


def download_horse_ability(filters: list = ['hrNm', 'hrEngNm', 'rnCnt', 'fstCnt', 'sndCnt', 'trdCnt', 'forthCnt', 
                                        'fifthCnt', 'outCnt', 'amt', 'condAmt', 'winRate', 'quinRate', 'avgWinDist']):
    horse_ability_url = 'http://apis.data.go.kr/B551015/API42/totalHorseInfo'

    page = 1

    horse_abilities = {}
    while True:
        print(f'Downloading page {page}')

        horse_ability_params = {'serviceKey' : service_key, 'pageNo' : str(page), 'numOfRows' : '5000' }

        response = requests.get(horse_ability_url, params=horse_ability_params)
        if response.status_code != 200:
            raise ConnectionError(f'status code not 200. Failed with code {response.status_code}')

        horse_ability_xml = response.content.decode('utf8')

        horse_ability_dict = xmltodict.parse(horse_ability_xml)

        if 'items' not in horse_ability_dict['response']['body'].keys() or horse_ability_dict['response']['body']['items'] is None:
            # If it exceeds the last page, horse_ability will have no items.
            break

        horse_ability_dict_list = horse_ability_dict['response']['body']['items']['item']
        for horse_ability in horse_ability_dict_list:
            horse_ability_filtered = {key: horse_ability[key] for key in horse_ability.keys() if key in filters }
            horse_abilities[horse_ability['hrNo']] = horse_ability_filtered

        page += 1

    print(f'{len(horse_abilities) = }')

    # save horse abilities
    with open('horse_ability.json', 'w') as f:
        json.dump(horse_abilities, f, ensure_ascii=False, indent=4)


# In[437]:


def load_horse_ability(path: str = 'horse_ability.json'):
    # load horse_abilities
    with open(path, 'r') as f:
        horse_ability = json.load(f)
    return horse_ability


# In[438]:


def print_horse(horse: dict, filter_tags: list = None):
    """
    params:
        horse (ElementTree): 
        filter_tags (str or list): tag(s) to print
    return (None)
    """
    # convert str to list
    if isinstance(filter_tags, str):
        filter_tags = [filter_tags]
    for element, value in horse.items():
        if filter_tags is not None:
            if element in filter_tags:
                print(f'{element:10s} {value}')
        else:
            print(f'{element:10s} {value}')


# ### Rearrange the data (group by race, not horse)

# In[439]:


def download_race():
    #service_key = 'uOnq3a%2FhTeOMpTjruRiBY0S4cYo%2BVXoKXXs13PF1CdJkwOOQ2qmNqYphHwsMpDqgprL6zng2R3hO4knPqD8wdA%3D%3D'
    service_key = 'uOnq3a/hTeOMpTjruRiBY0S4cYo+VXoKXXs13PF1CdJkwOOQ2qmNqYphHwsMpDqgprL6zng2R3hO4knPqD8wdA=='

    race_url = 'http://apis.data.go.kr/B551015/API186/SeoulRace'
    race_params ={'serviceKey' : service_key, 'pageNo' : '1', 'numOfRows' : '200', 'rc_date_fr' : '20160101'}
    response = requests.get(race_url, params=race_params)
    race_xml = response.content.decode('utf8')

    race = xmltodict.parse(race_xml)
    horses = race['response']['body']['items']['item']
    
    return horses
    #print(horses[0])
    #print_horse(horses[0], 'hrName')


# In[440]:


def rearrange_horses(horses: dict, horse_abilities: dict, filters : list = ['hrNo', 'meet', 'noracefl', 'rcRank', 'rcDate', 
                                                                       'rcDist', 'rcNo', 'rcOrd', 'rcP1Odd', 'rcP2Odd', 'rcP3Odd']):
    """
    params:
        horse (dict): Race data of the horses
    return races (dict)
    """

    races = {}
    for horse in horses:
        # Horses in rank 06 don't have ratings.
        if horse['rcRank'] == '06':
            continue
        # Get horse ability from horse_abilities
        horse_ability_dict = horse_abilities[horse['hrNo']]
        
        horse_filtered = {key: horse[key] for key in horse.keys() if key in filters }
        horse_filtered.update(horse_ability_dict)
        
        racecode = f"{horse['rcDate']}_{horse['rcNo']}"
        # race code = date_no
        if racecode in races.keys():
            races[racecode].append(horse_filtered)
        else:
            races[racecode] = [horse_filtered]
    return races


# In[443]:


def main():
    horse_abilities = load_horse_ability()
    horses = download_race()

    races = rearrange_horses(horses, horse_abilities)
    
    print(horse_abilities[races['20160102_4'][0]['hrNo']])

    for racecode, horses in races.items():
        print(racecode)
        for horse in horses:
            print_horse(horse)
            print('\n')


# In[ ]:


if __name__ == '__main__':
    main()

