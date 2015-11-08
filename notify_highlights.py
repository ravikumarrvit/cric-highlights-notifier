#!/usr/bin/env python

import sys
import time
import logging
import ScoreReporter

INDIA_INDEX = None
ROOT_LOGGER = logging.getLogger()
PREV_MATCH_ID = None

def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def display_teams(team_list):

    global INDIA_INDEX

    index = 0
    for team in team_list:
        if team.lower() == "india":
            INDIA_INDEX = index
        index = index + 1
        serial_no = str(index) + ". "
        print '%s' % serial_no.rjust(4) + team

    if INDIA_INDEX != None:
        print "Press enter to proceed with India"

def get_team_choice(no_of_teams):

    choice = raw_input("Enter the team number: ")
    ROOT_LOGGER.debug("Choice int check: " + str(is_int(choice)) + ", No of teams: " + str(no_of_teams))
    if is_int(choice) and int(choice) != 0 and int(choice) <= no_of_teams:
        return int(choice)
    elif choice == "":
        return INDIA_INDEX + 1
    else:
        print "Please enter one of the above team nos [eg. 1 as input for Team X]"
        get_team_choice(no_of_teams)

def main():

    score_reporter = ScoreReporter.ScoreReporter(ROOT_LOGGER)

    team_list = score_reporter.get_team_list()
    if team_list:
        display_teams(team_list)
    else:
        ROOT_LOGGER.info("No top teams are playing cricket currently")
        sys.exit(0)

    chosen_team_index = get_team_choice(len(team_list))

    global PREV_MATCH_ID
    if not PREV_MATCH_ID:
        match_id = score_reporter.get_match_id(team_list[chosen_team_index - 1])
        PREV_MATCH_ID = match_id

    ROOT_LOGGER.debug("Match ID: " + str(PREV_MATCH_ID))

    team_score = score_reporter.get_team_score(PREV_MATCH_ID)

    score_reporter.compare_scores(team_score)

if __name__ == '__main__':

    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-10.10s] [%(levelname)-5.5s]  %(message)s")
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)
    ROOT_LOGGER.addHandler(console_handler)
    ROOT_LOGGER.setLevel(logging.DEBUG)

    while True:
        main()
        time.sleep(10)


