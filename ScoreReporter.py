import json
import urllib2
import PlatformDetector

# Uses the APIs provided by http://cricscore-api.appspot.com/

MATCH_URL = "http://cricscore-api.appspot.com/csa"
SUPPORTING_TEAM = "Nepal"
PREV_TEAM_SCORE = None

class ScoreReporter:

    def __init__(self, logger):
        self.logger = logger

    def get_match_id(self):

        try:
            matches_json = json.load(urllib2.urlopen(MATCH_URL))
        except Exception, e:
            self.logger.error("Not able to connect to the URL - Error: " + str(e))
            self.logger.info("Trying to connect again...")
            self.get_match_id()
        team_found = False
        match_id = -1
        for match in matches_json:
            for key, value in match.iteritems():
                if key == "id":
                    temp_id = value
                if key == "t1" or key == "t2":
                    if value == SUPPORTING_TEAM:
                        team_found = True
                if team_found:
                    match_id = temp_id
                    break
            if team_found:
                break
        return match_id

    def notify(self, title, msg, sound=None):

        plat_notifier = PlatformDetector.PlatformDetector().get_platform_notifier()
        plat_notifier.notify(title, msg, sound)

    def match_over_stumps(self, desc):

        match_status_list = desc.split("-")
        status = None
        if len(match_status_list) > 1:
            status = match_status_list[1].strip()
        if "over" in status or "Stumps" in status:
            return True

    def get_team_score(self, match_id):

        if match_id != -1:
            # URL is in the format of http://cricscore-api.appspot.com/csa?id=931390
            try:
                scores_json = json.load(urllib2.urlopen(MATCH_URL + "?id=" + str(match_id)))
            except Exception, e:
                self.logger.error("Not able to connect to the URL - Error: " + str(e))
                self.logger.info("Trying to connect again...")
                self.get_team_score(match_id)
            team_score_found = False

            # Sample response: [{"de":"Zim 82/5 (27.1 ov, E Chigumbura 16*, MN Waller 1*, Mashrafe Mortaza 1/6)","id":931390,"si":"Bangladesh 273/9 v Zimbabwe 80/5 *"}]
            for key, value in scores_json[0].iteritems():
                if key == "de":
                    if self.match_over_stumps(value):
                        self.logger.info("Match is over/stumps for the day")
                        self.notify("STATUS", value)
                        exit(0)
                    team_score = str(value.split("(")[0]).strip()
                    team_score_found = True
                if team_score_found:
                    break

            self.logger.debug("Team Score: " + team_score)
            return team_score
        else:
            return None

    def get_runs_wickets(self, team_score):

        # Sample team score: Zim 82/5

        team, score = team_score.split(" ")
        score.strip()
        return score.split("/")

    def compare_scores(self, team_score):

        if team_score:

            global PREV_TEAM_SCORE
            if PREV_TEAM_SCORE == None:
                PREV_TEAM_SCORE = team_score
                self.notify("SCORE", team_score, None)
            else:
                prev_runs, prev_wickets = self.get_runs_wickets(PREV_TEAM_SCORE)
                curr_runs, curr_wickets = self.get_runs_wickets(team_score)

                diff_runs = int(curr_runs) - int(prev_runs)
                diff_wickets = int(curr_wickets) - int(prev_wickets)

                self.logger.debug("Run Diff: " + str(diff_runs) + ", Wicket diff: " + str(diff_wickets))

                if diff_runs == 4:
                    self.notify("FOUR", team_score, None)
                elif diff_runs == 6:
                    self.notify("SIX", team_score, None)
                elif diff_wickets != 0:
                    self.notify("WICKET", team_score, None)
                PREV_TEAM_SCORE = team_score