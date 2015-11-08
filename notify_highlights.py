#!/usr/bin/env python

import sys
import time
import logging
import ScoreReporter

DEBUG = True
ROOT_LOGGER = logging.getLogger()
PREV_MATCH_ID = None

def main():

    score_reporter = ScoreReporter.ScoreReporter(ROOT_LOGGER)

    global PREV_MATCH_ID
    if not PREV_MATCH_ID:
        match_id = score_reporter.get_match_id()
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


