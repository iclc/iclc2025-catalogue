import csv
import unicodedata
from io import StringIO
from slugify import slugify
import yaml
import os
import re
from pathlib import Path

"""
Paper: abstract
Workshop: abstract, prog_note
Performace: abastract (TBD), prog_note
"""

def make_slug(input):
    return slugify(input, True, True, True, 64, True)

def clean_cell(cell):
    if cell.strip() == "NULL": cell = ""
    return unicodedata.normalize("NFC", cell.strip()).replace("\r", "")

def clean_text(cell):
    return re.sub(' +', ' ', cell)

def read_as_clean_dict(data):
    ret = []
    csvRows = csv.reader(StringIO(data))
    
    # clean up cell content
    csvRows = list(map(lambda row : list(map(clean_cell, row)), csvRows))

    keys = csvRows[0]

    csvRows = csvRows[1:]
    
    # build a dictionary out of it
    for row in csvRows:

        if row[0] == "": continue # if slug is empty then skip row
        
        entry = {}
        for i in range(len(keys)):
            entry[keys[i]] = row[i]

        ret.append(entry)
    
    return ret

with open('authors.csv', 'r') as file:
    authors_string = file.read()

with open('workshop_time_abstract.csv', 'r') as file:
    ws_time_abstract_string = file.read()

with open('perf.csv', 'r') as file:
    perf_time_abstract_string = file.read()

authors = read_as_clean_dict(authors_string)

ws_time_abstract_list = read_as_clean_dict(ws_time_abstract_string)
ws_time_abstract = {}
perf_time_abstract_list = read_as_clean_dict(perf_time_abstract_string)
perf_time_abstract = {}

# dict with ID
for item in ws_time_abstract_list:    
    ws_time_abstract[item["ID"]] = item

# dict with ID
for item in perf_time_abstract_list:    
    perf_time_abstract[item["ID"]] = item

ws_template = """---
slug: %s
status: proof
title: %s
type: workshop
submission_type: Workshop
time: %s
contributors:
%s
---

# $PROGRAM_NOTE

%s

# $ABSTRACT

%s

"""

perf_template = """---
slug: %s
status: proof
title: %s
event: %s
type: performance
submission_type: Performance
time: %s
contributors:
%s
---

# $PROGRAM_NOTE

%s

# $ABSTRACT

%s

"""

person_template = """---
slug: %s
status: proof
type: person
last_name: %s
first_name: %s
alias: null
affiliations:
- TBD
---

TBD

"""

ws_event_template = """---
slug: workshops
type: event
status: ready
event_type: Workshops
title: Workshops
venue: null
date_time: Saturday, May 31st, 11:00&#8209;18:15
schedule:
%s
---
"""

perf_event_template = """---
slug: %s
type: event
status: ready
event_type: Performances
title: %s
venue: %s
date_time: tba
schedule:
%s
---
"""

# create folders
Path("output/assets/").mkdir(parents=True, exist_ok=True)
Path("output/workshop/").mkdir(parents=True, exist_ok=True)
Path("output/event/").mkdir(parents=True, exist_ok=True)
Path("output/person/").mkdir(parents=True, exist_ok=True)
Path("output/performance/").mkdir(parents=True, exist_ok=True)

workshops = {}

# GET WORKSHOPS
for author in authors: 
    if author["Type"] == "workshop" and author["Status"] == "Accepted" :
        title = author["Title"].replace(":", " - ")
        slug = make_slug(title)
        author_slug = make_slug(author["lastname"] + "-" + author["Firstname"])
        id = author["ID"]

        abstract = ws_time_abstract[id]["Abstract"]
        program_note = ws_time_abstract[id]["ProgramNotes"]
        
        workshops.setdefault(slug, {
            "authors": [],
            "slug": slug,                
            "title": title,
            "filename": "%s_%s.md" % (id, slug),
            "abstract": abstract,
            "program_note": program_note,
            "time": ws_time_abstract[id]["Schedule"],
            "room": ws_time_abstract[id]["Room"],
        })["authors"].append([author_slug, author["Firstname"], author["lastname"]])

# RENDER PEOPLE TO MD, JUST SO THE LINKS ARE NOT DEAD (FOR NOW)
for slug, workshop in workshops.items():
    authors_string = ""
    
    for author in workshop["authors"]:
        authors_string += "- person: $" + author[0] +"\n"
        content = person_template % (author[0], author[1], author[2])
        with open('output/person/' + author[0] + ".md", 'w') as file:
            file.write(content)

# RENDER WORKSHOPS TO MD
for slug, workshop in workshops.items():
    authors_string = ""
    
    for author in workshop["authors"]:
        authors_string += "- person: $" + author[0] +"\n"
            
    content = ws_template % (workshop['slug'], workshop['title'], workshop["time"], authors_string, workshop['program_note'], workshop['abstract'])

    with open('output/workshop/' + workshop["filename"], 'w') as file:
        file.write(content)
        

# RENDER WORKSHOP EVENT TO MD
workshops = {k: v for k, v in sorted(workshops.items(), key=lambda item: item[1]["time"])}

workshop_schedule = ""
for slug, workshop in workshops.items():
    workshop_schedule += "  -  time: %s\n     item: $%s\n     venue: Canòdrom - %s\n" % (workshop['time'], slug, workshop["room"])

    with open('output/event/workshops.md' , 'w') as file:
        file.write(ws_event_template % workshop_schedule)

    
# PERFORMANCES
performances = {}
performance_events = {}

# GET PERFORMANCES
for author in authors: 
    if author["Type"] == "performance" and author["Status"] == "Accepted" :
        title = author["Title"].replace(":", " - ")
        slug = make_slug(title)
        author_slug = make_slug(author["lastname"] + "-" + author["Firstname"])
        id = author["ID"]
        
        abstract = "" # tbd
        # some are withdrawn
        try:
            program_note = perf_time_abstract[id]["ProgramNotes"]
        except:
            continue
        
        performances.setdefault(slug, {
            "authors": [],
            "slug": slug,                
            "title": title,
            "filename": "%s_%s.md" % (id, slug),
            "abstract": abstract,
            "event": perf_time_abstract[id]["event"],
            "program_note": program_note,
            "time": perf_time_abstract[id]["Schedule"],
            "room": perf_time_abstract[id]["Room"],
        })["authors"].append([author_slug, author["Firstname"], author["lastname"]])



        
# RENDER PEOPLE TO MD, JUST SO THE LINKS ARE NOT DEAD (FOR NOW)
for slug, performance in performances.items():    
    for author in performance["authors"]:
        content = person_template % (author[0], author[1], author[2])
        with open('output/person/' + author[0] + ".md", 'w') as file:
            file.write(content)

# RENDER PERFORMANCES TO MD
for slug, performance in performances.items():
    authors_string = ""
    
    for author in performance["authors"]:
        authors_string += "- person: $" + author[0] +"\n"
            
    content = perf_template % (performance['slug'], performance['title'], performance['event'], performance["time"], authors_string, performance['program_note'], performance['abstract'])

    with open('output/performance/' + performance["filename"], 'w') as file:
        file.write(content)

# COLLECT PERFORMANCE EVENTS
for slug, performance in performances.items():
    performance_events.setdefault(performance["event"], []).append(performance)

for event, perfs in performance_events.items():
    event_schedule = ""
    venue = ""
    for perf in perfs:
        event_schedule += "  -  time: %s\n     item: $%s\n" % (perf['time'], perf['slug'])
        venue = perf['room']

    with open('output/event/%s.md' % event , 'w') as file:
        file.write(perf_event_template % (event, event, venue, event_schedule))
