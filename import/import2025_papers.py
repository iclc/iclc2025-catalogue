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

with open('papers.csv', 'r') as file:
    paper_time_abstract_string = file.read()

authors = read_as_clean_dict(authors_string)

paper_time_abstract_list = read_as_clean_dict(paper_time_abstract_string)
paper_time_abstract = {}

# dict with ID
for item in paper_time_abstract_list:    
    paper_time_abstract[item["ID"]] = item

paper_template = """---
slug: %s
status: proof
title: %s
event: %s
type: paper
submission_type: Papers
time: %s
contributors:
%s
---

# $ABSTRACT

TBD

"""

person_template = """---
slug: %s
status: proof
type: person
first_name: %s
last_name: %s
alias: null
affiliations:
- TBD
---

TBD

"""

paper_event_template = """---
slug: %s
type: event
status: ready
event_type: Paper Session
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
Path("output/paper/").mkdir(parents=True, exist_ok=True)
    
# PAPERS
papers = {}
paper_events = {}
paper_event_titles = {}

# GET PAPERS
for author in authors: 
    if author["Type"] == "paper" and author["Status"] == "Accepted" :
        title = author["Title"].replace(":", " - ")
        slug = make_slug(title)
        author_slug = make_slug(author["lastname"] + "-" + author["Firstname"])
        id = author["ID"]

        try: 
            a = paper_time_abstract[id]["SessionID"]
        except:
            continue
        
        abstract = "" # tbd
                
        papers.setdefault(slug, {
            "authors": [],
            "slug": slug,                
            "title": title,
            "filename": "%s_%s.md" % (id, slug),
            #"abstract": abstract,
            "event": make_slug(paper_time_abstract[id]["SessionID"]),
            "event_title": paper_time_abstract[id]["SessionName"],
            #"program_note": program_note,
            # order": papertime_abstract[id]["order"],
            "time": paper_time_abstract[id]["Day"] + ", " + paper_time_abstract[id]["SessionTime"],
            #"venue": paper_time_abstract[id]["Venue"],
        })["authors"].append([author_slug, author["Firstname"], author["lastname"]])

        
# RENDER PEOPLE TO MD, JUST SO THE LINKS ARE NOT DEAD (FOR NOW)
for slug, paper in papers.items():    
    for author in paper["authors"]:
        content = person_template % (author[0], author[1], author[2])
        with open('output/person/' + author[0] + ".md", 'w') as file:
            file.write(content)

# RENDER PAPERS TO MD
for slug, paper in papers.items():
    authors_string = ""
    
    for author in paper["authors"]:
        authors_string += "- person: $" + author[0] +"\n"
            
    content = paper_template % (paper['slug'], paper['title'], paper['event'],
                               paper["time"], authors_string)

    with open('output/paper/' + paper["filename"], 'w') as file:
        file.write(content)

# COLLECT PAPER EVENTS
for slug, paper in papers.items():
    paper_events.setdefault(paper["event"], []).append(paper)
    paper_event_titles.setdefault(paper["event"], paper["event_title"])

for event, papers in paper_events.items():
    event_schedule = ""
    venue = ""
    date_time = papers[0]["time"]
    event_title = paper_event_titles[event]
    event_title = event_title.replace("\n", " - ")
    event_title = event_title.replace(":", "&#58;")
    event_title = event_title.replace("|", "&#124;")

    # perfs = sorted(papers, key=lambda item: item["order"])
    
    for paper in papers:
        event_schedule += "  -  item: $%s\n" % (paper['slug'])
        venue = "UOC"

    with open('output/event/%s.md' % event , 'w') as file:
        file.write(paper_event_template % (event, event_title, venue, date_time, event_schedule))
