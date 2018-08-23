# What is it
Code snippet to extract dependencies between Stories in Jira
Stories must contain "depends on" or similar. "is linked to" is ignored

If [Script Runner](https://marketplace.atlassian.com/plugins/com.onresolve.jira.groovy.groovyrunner) installed you can use
"issueFunction in hasLinks(blocks)"

# How to setup
Depends on Python 3

```
mkvirtualenv --system-site-packages srf
workon srf
pip install -r requirements.txt
```

create credentials.py file
```
username = "john.doe@srf.ch"
password = "MySuperSecret"
```

# How to run
python dependencies.py
