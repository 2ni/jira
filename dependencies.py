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
    "current sprint": 'type in (task, bug, story, improvement) and project in (AIS, AISK) and sprint in (openSprints()) ORDER BY Rank ASC',
    "future sprint": 'type in (task, bug, story, improvement) and project in (AIS, AISK) and sprint in (futureSprints()) ORDER BY Rank ASC',
    }

for title,jql in jqls.items():
    print("{delimiter} {title} {delimiter}".format(delimiter="-"*10, title=title))
    stories = jira.search_issues(jql, maxResults=100)
    #stories = [jira.issue("AIS-18819")]
    for story in stories:
        link_in = []
        link_out = []
        for link in story.fields.issuelinks:
            #print(link, vars(link))
            if hasattr(link, "inwardIssue") and not link.inwardIssue.key.startswith("AIS-") \
            and not re.search("(clone|relates)", link.type.inward) \
            and not link.inwardIssue.key in link_in:
                #print(link.type.inward)
                link_in.append("{key}:{status}".format(key=link.inwardIssue.key, status=link.inwardIssue.fields.status.name))
                #print("{key} < {link}".format(key=story.key, link=link.inwardIssue.key))
            if hasattr(link, "outwardIssue") \
            and not link.outwardIssue.key.startswith("AIS-") \
            and not re.search("(clone|relates)", link.type.outward) \
            and not link.outwardIssue.key in link_out:
                link_out.append("{key}:{status}".format(key=link.outwardIssue.key, status=link.outwardIssue.fields.status.name))
                #print("{key} > {link}".format(key=story.key, link=link.outwardIssue.key))

        story_key = "{k}:{s}".format(k=story.key, s=story.fields.status.name)
        print("{link_in:30s} > {key}\n".format(key=story_key, link_in = link_in[0]) if link_in else "", end="")
        if len(link_in) > 1:
            for l in link_in[1:]:
                print(" {l:29s} >".format(l=l))
        print("{key:30s} > {link_out}\n".format(key=story_key, link_out = link_out[0]) if link_out else "", end="")
        if len(link_out) > 1:
            for l in link_out[1:]:
                print(" {l:29s} >".format(l=l))
        sys.stdout.flush()
