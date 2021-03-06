'''
Displays external dependencies of the next future stories
works only in PDA network for now
based on https://jira.readthedocs.io/

credentials are saved in a separate file credentials.py, ie:
username = "john.doe@srf.ch"
password = "MySuperSecret"
'''

import sys, re, credentials
from jira import JIRA
jira = JIRA(server="https://srfmmz.atlassian.net", basic_auth=(credentials.username, credentials.password))

print("x > y: x blocks y")

jqls = {
    "current sprint": 'type in (task, bug, story, improvement) and project in (AIS, AISK) and sprint in (openSprints()) ORDER BY rank ASC',
    "future sprint": 'type in (task, bug, story, improvement) and project in (AIS, AISK) and sprint in (futureSprints()) ORDER BY sprint ASC, rank ASC',
    }

currentsprint = ""
for title,jql in jqls.items():
    page = 0;
    #print("{delimiter} {title} {delimiter}".format(delimiter="-"*10, title=title))
    while(1):
        stories = jira.search_issues(jql, maxResults=100, startAt=page)
        #stories = [jira.issue("AIS-18819")]
        if (len(stories) == 0):
            break

        page += 100
        for story in stories:
            link_in = []
            link_out = []
            for link in story.fields.issuelinks:
                #print(link, vars(link))
                if hasattr(link, "inwardIssue") and not link.inwardIssue.key.startswith("AIS-") \
                and not re.search("(clone|relates)", link.type.inward) \
                and not link.inwardIssue.key in link_in:
                    #print("*", link.inwardIssue.key, link.type.inward)
                    link_in.append("{key}:{status}".format(key=link.inwardIssue.key, status=link.inwardIssue.fields.status.name))
                    #print("{key} < {link}".format(key=story.key, link=link.inwardIssue.key))
                if hasattr(link, "outwardIssue") \
                and not link.outwardIssue.key.startswith("AIS-") \
                and not re.search("(clone|relates)", link.type.outward) \
                and not link.outwardIssue.key in link_out:
                    #print("*", link.outwardIssue.key, link.type.outward)
                    link_out.append("{key}:{status}".format(key=link.outwardIssue.key, status=link.outwardIssue.fields.status.name))
                    #print("{key} > {link}".format(key=story.key, link=link.outwardIssue.key))

            story_key = "{k}:{s}".format(k=story.key, s=story.fields.status.name)

            if (link_in or link_out):
                sprint = currentsprint
                try:
                    sprints = [b for x in story.fields.customfield_10265 for w in x.split(",") for a,b in [w.split("=")] if a == "name"]
                    sprint = sorted(sprints, key=str.lower, reverse=True)[0]
                except:
                    pass

                if (sprint != currentsprint):
                    currentsprint = sprint
                    print("\n{delimiter}\n{sprint}\n{delimiter}".format(delimiter="*"*80, sprint=sprint))

            #print("*", story.key, sprint)
            print("{link_in:30s} > {key}\n".format(key=story_key, link_in = link_in[0]) if link_in else "", end="")
            if len(link_in) > 1:
                for l in link_in[1:]:
                    print(" {l:29s} >".format(l=l))
            print("{key:30s} > {link_out}\n".format(key=story_key, link_out = link_out[0]) if link_out else "", end="")
            if len(link_out) > 1:
                for l in link_out[1:]:
                    print("{s:30s} > {l}".format(s=" ", l=l))
            sys.stdout.flush()
