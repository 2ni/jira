z = ['a[foo=bar,foo2=bar2]', 'b[gna=sab,gna2=sab2]']
z = ['foo=bar,foo2=bar2,name=super', 'name=mario,gna=sab,gna2=sab2']
z = ['com.atlassian.greenhopper.service.sprint.Sprint@45f63c5e[id=757,rapidViewId=115,state=ACTIVE,name=AIS-EAI 122-38 (14.09-27.09)W1,goal=,startDate=2018-09-14T07:00:18.722Z,endDate=2018-09-27T16:00:00.000Z,completeDate=<null>,sequence=770]']

names = []
for x in z:
    for w in x.split(","):
        a,b = w.split("=")
        if (a=="name"):
            names.append(b)

print(names);

# nested comprehensions keep order of nests (not as our mind would like to proceed)
comprehension = [
    b
    for x in z
    for w in x.split(",")
    for a,b in [w.split("=")]
    if a == "name"
]

print(comprehension)
