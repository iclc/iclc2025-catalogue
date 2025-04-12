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

with open('perf.csv', 'r') as file:
    perf_time_abstract_string = file.read()

authors = read_as_clean_dict(authors_string)

perf_time_abstract_list = read_as_clean_dict(perf_time_abstract_string)
perf_time_abstract = {}

# dict with ID
for item in perf_time_abstract_list:    
    perf_time_abstract[item["ID"]] = item

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

perf_event_template = """---
slug: %s
type: event
status: ready
event_type: Performances
title: %s
venue: %s
date_time: %s
schedule:
%s
---
"""

# create folders
Path("output/assets/").mkdir(parents=True, exist_ok=True)
Path("output/event/").mkdir(parents=True, exist_ok=True)
Path("output/person/").mkdir(parents=True, exist_ok=True)
Path("output/performance/").mkdir(parents=True, exist_ok=True)
    
# PERFORMANCES
performances = {}
performance_events = {}
performance_event_titles = {}

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
            "event": make_slug(perf_time_abstract[id]["event"]),
            "event_title": perf_time_abstract[id]["event_title"],
            "program_note": program_note,
            "order": perf_time_abstract[id]["order"],
            "time": perf_time_abstract[id]["Date"] + ", " + perf_time_abstract[id]["Schedule"],
            "venue": perf_time_abstract[id]["Venue"],
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
            
    content = perf_template % (performance['slug'], performance['title'], performance['event'],
                               performance["time"], authors_string, performance['program_note'],
                               performance['abstract'])

    with open('output/performance/' + performance["filename"], 'w') as file:
        file.write(content)

# COLLECT PERFORMANCE EVENTS
for slug, performance in performances.items():
    performance_events.setdefault(performance["event"], []).append(performance)
    performance_event_titles.setdefault(performance["event"], performance["event_title"])

for event, perfs in performance_events.items():
    event_schedule = ""
    venue = ""
    date_time = perfs[0]["time"]
    event_title = performance_event_titles[event]
    event_title = event_title.replace("\n", " - ")
    event_title = event_title.replace(":", "&#58;")
    event_title = event_title.replace("|", "&#124;")

    perfs = sorted(perfs, key=lambda item: item["order"])
    
    for perf in perfs:
        event_schedule += "  -  item: $%s\n" % (perf['slug'])
        venue = perf['venue']

    with open('output/event/%s.md' % event , 'w') as file:
        file.write(perf_event_template % (event, event_title, venue, date_time, event_schedule))
