'''
Searches for specific labels and replaces them
cleanup script, ie aisEAI vs aisEai
based on https://jira.readthedocs.io/

credentials are saved in a separate file credentials.py, ie:
username = "john.doe@srf.ch"
password = "MySuperSecret"
'''

import sys, re, credentials
from jira import JIRA
jira = JIRA(server="https://srfmmz.atlassian.net", basic_auth=(credentials.username, credentials.password))

label_to_replace = "aisEai"
label_replacement = "aisEAI"

page = 0
while(1):
    print("page {page}".format(page=page))
    stories = jira.search_issues('project in (AIS, AISK) and labels in ({label})'.format(label=label_to_replace), startAt=page, maxResults=100, fields='labels')
    #stories = [jira.issue("AIS-19280")]
    if (len(stories) == 0):
        break

    page += 100
    for story in stories:
        if (label_to_replace in story.fields.labels):
            labels = story.fields.labels
            print("updating {id}: {labels}".format(id=story.key, labels=labels))
            labels.remove(label_to_replace)
            if label_replacement not in labels:
                labels.append(label_replacement)

            story.update(notify=False, fields={"labels": labels})

