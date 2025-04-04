import csv
import unicodedata
from io import StringIO
from slugify import slugify
import yaml
import os
import re
from pathlib import Path

"""
Video: prog_note
Paper: abstract
Workshop: abstract, prog_note
Performace: abastract, prog_note
"""

EXPORT_MAIL = True

BASIC_TYPES = {
    "Performance": "performance",
    "Paper-Long": "paper",
    "Paper-Short": "paper",
    "Community-Written": "paper",
    "Workshop": "workshop",
    "Community-Video": "video",
    "Video-Long": "video",
    "Video-Short": "video"
}

FOLDERS = ["performance", "person", "workshop", "video", "paper", "secret"]

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

authors = read_as_clean_dict(authors_string)
ws_time_abstract_list = read_as_clean_dict(ws_time_abstract_string)
ws_time_abstract = {}

# dict with ID
for item in ws_time_abstract_list:    
    ws_time_abstract[item["ID"]] = item

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

Path("output/assets/").mkdir(parents=True, exist_ok=True)
Path("output/workshop/").mkdir(parents=True, exist_ok=True)
Path("output/event/").mkdir(parents=True, exist_ok=True)
Path("output/person/").mkdir(parents=True, exist_ok=True)

# RENDER PEOPLE TO MD, JUST SO THE LINKS ARE NOT DEAD (FOR NOW)
for slug, workshop in workshops.items():
    authors = ""
    
    for author in workshop["authors"]:
        authors += "- person: $" + author[0] +"\n"
        content = person_template % (author[0], author[1], author[2])
        with open('output/person/' + author[0] + ".md", 'w') as file:
            file.write(content)

# RENDER WORKSHOPS TO MD
for slug, workshop in workshops.items():
    authors = ""
    
    for author in workshop["authors"]:
        authors += "- person: $" + author[0] +"\n"
            
    content = ws_template % (workshop['slug'], workshop['title'], workshop["time"], authors, workshop['program_note'], workshop['abstract'])

    with open('output/workshop/' + workshop["filename"], 'w') as file:
        file.write(content)
        

# RENDER WORKSHOP EVENT TO MD
workshops = {k: v for k, v in sorted(workshops.items(), key=lambda item: item[1]["time"])}

workshop_schedule = ""
for slug, workshop in workshops.items():
    workshop_schedule += "  -  time: %s\n     item: $%s\n     venue: Canòdrom - %s\n" % (workshop['time'], slug, workshop["room"])

    with open('output/event/workshops.md' , 'w') as file:
        file.write(ws_event_template % workshop_schedule)

    
    
