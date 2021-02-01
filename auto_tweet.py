import os
import us
import tweepy
import random
import requests
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return chrome_options

def get_driver_location():
    return '/Users/cutlersimpson/Personal/Projects/TwoToEight/chromedriver'

def get_national_url():
    return 'https://www.usdebtclock.org/'

def get_state_url(state):
    return 'https://www.usdebtclock.org/state-debt-clocks/state-of-' + state + '-debt-clock.html'

def get_national_debt(driver):
    return driver.find_element_by_id("X1a56929BW").text

def get_state_debt(driver):
    return driver.find_element_by_id('X2a5BWRG').text

def get_debt_per_person(driver):
    return driver.find_element_by_xpath('//span[@id="X2a5BWRG"]').text

def get_national_revenue(driver):
    return driver.find_element_by_css_selector('body').text.split("\n")[25]

def get_revenue_per_person(drvier):
    return driver.find_element_by_css_selector('body').text.split("\n")[26]

def get_national_tweet(driver):
    return (
        "US National Debt: " + get_national_debt(driver) +
        "\nUS National Debt per Citizen: " + get_debt_per_person(driver) +
        "\nFederal Revenue: " + get_national_revenue(driver) +
        "\nRevenue per Citizen: " + get_revenue_per_person(driver)
        )

def get_state_tweet(state_debts):
    tweets = []

    for state, debt in state_debts.items():
        tweets.append(state + ' debt: ' + debt)

    return tweets


def get_state_debts(states, driver):
    states_nums = get_states()
    state_urls = {}
    state_debts = {}
    states_map = {}

    for num in states_nums:
        state = states[num].name.lower().replace(' ', '-')
        state_urls[state] = get_state_url(state)
        states_map[state] = states[num].name

    for state, url in state_urls.items():
        driver.get(url)
        state_name = states_map[state]
        state_debts[state_name] = get_state_debt(driver)

    return state_debts

def get_states():
    path = 'states.txt'
    states = []

    # If file does not exist create it
    if not os.path.exists(path):
        with open (path, 'w+'): pass

    # If file is empty write randomized state num values to it
    if os.path.getsize(path) == 0:
        state_nums = list(range(50))
        random.shuffle(state_nums)

        with open(path, 'w+') as states_file:
            for num in state_nums:
                states_file.write(str(num) + "\n")

    # Get first 5 lines from file
    with open(path) as file:
        all_lines = file.readlines()
        lines = all_lines[0:5]

    # Delete file
    os.remove(path)

    # Rewrite after ignoring first 5 lines
    with open(path, "w+") as file:
        for l in all_lines[5:]:
            file.write(l)

    for line in lines:
        state = int(line.strip('\n'))
        states.append(state)

    return states


def send_national_tweet(driver):
    driver.get(get_national_url())
    send_tweet(get_national_tweet(driver))

def send_state_tweet(states, driver):
    send_tweet('\n'.join(get_state_tweet(get_state_debts(states,driver))))

def send_tweet(tweet):
    auth = tweepy.OAuthHandler("9Usj4sqG39FlX1RZyYFZzl24s", "TT6ZHWQCyd0GgxVUFiXrbV7FX0dCYRDZiZr7ABIZj3XoDczQtW")
    auth.set_access_token("1352810525885775872-WTSqrskq0sC36TlCnHZD9kDEY4TNTc", "6k0NueduhU0W1ampqLSUd0GVOn6zGfVRVFsvH8QgxkSeq")
    api = tweepy.API(auth)
    api.update_status(status = (tweet))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--type', required=True)

    tweet_type = parser.parse_args().type

    if tweet_type.lower() == 'state':
        driver = webdriver.Chrome(get_driver_location(), options=get_chrome_options())
        states = us.states.STATES
        send_state_tweet(states, driver)

    elif tweet_type.lower() == 'national':
        driver = webdriver.Chrome(get_driver_location(), options=get_chrome_options())
        send_national_tweet(driver)

    else:
        raise ValueError('Type must either be state or national')

    driver.close()

