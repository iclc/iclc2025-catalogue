from io import StringIO
import yaml
import os
import random
from datetime import datetime
import markdown
import unicodedata
import shutil 
import pprint

EXPORT_MAIL = False
MASTER_SCHEDULE_DO_HIDE = True
RENDER_PROOF = False

CAL_FOLDER = "catalogue/"
PROOF_INCLUDE_ABSTRACTS = False
HEADER = "ICLC 2025 Catalogue"
INCLUDE_STATUS_OVERVEW = False
ACTIVE_STATUS_FLAGS = ["ready", "proof"]
ALL_STATUS_FLAGS_OK = False
CAT_HOME = "catalogue/"

if RENDER_PROOF:
    CAL_FOLDER = 'catalogue/proof/'
    PROOF_INCLUDE_ABSTRACTS = True
    HEADER = "ICLC 2025 Catalogue PROOF VERSION"
    INCLUDE_STATUS_OVERVEW = True
    ACTIVE_STATUS_FLAGS = ["ready", "proof"]
    ALL_STATUS_FLAGS_OK = True
    CAT_HOME = "catalogue/proof/"

CAT_OUT_PATH = 'output/2025/' + CAL_FOLDER
STATUS_REL_PATH = '../../'


TYPES = {
    "keynote": "Keynote",
    "panel": "Discussion",
    "event": "Event",
    "person": "Person",
    'committee': "Committee",
    "Performance": "Performance",
    "Paper-Long": "Paper",
    "Paper-Short": "Paper",
    "Community-Written": "Community Report Paper",
    "Workshop": "Workshop",
    "Community-Video": "Community Report Video",
    "Video-Long": "Video",
    "Video-Short": "Video"
}

store = {}
emails = {}

now = datetime.now()


# prepare folders for output
for folder in ["performance", "person", "workshop", "video", "paper", "keynote", "event", "other", "assets"]:
    path = CAT_OUT_PATH + folder + "/"
    if not os.path.exists(path):
        os.makedirs(path)

# copy assets
shutil.rmtree(CAT_OUT_PATH + "assets/")
shutil.copytree("data/assets/", CAT_OUT_PATH + "assets/")

if EXPORT_MAIL:
    with open("data/secret/emails.yaml", 'r') as file:
        emails = yaml.safe_load(file.read())

def clean_cell(cell):
    if cell.strip() == "NULL": cell = ""
    return unicodedata.normalize("NFC", cell.strip()).replace("\r", "")


def sanitize_time(time):
    if time.startswith("t"):
        return time[1:]
    else:
        return time

def url_for_item(item):
    if item.get("external"):
        return item['external']
    else:
        return CAL_FOLDER + item["type"] + "/" + item["slug"] + ".html"

def path_for_item(item):
    return CAT_OUT_PATH + item["type"] + "/" + item["slug"] + ".html"

def render_name(person, display="default"):

    if not display: display = "default"

    ret = person["first_name"] + " " + person["last_name"]

    reverse = "reverse" in display

    if reverse:
        ret = "<strong>" + person["last_name"] + "</strong>, " + person["first_name"]

    use_alias = not "no_alias" in display

    if use_alias and person.get("alias", None):
        ret = f"{ret} ({person['alias']})"

    only_alias = "only_alias" in display

    if only_alias:
        ret = person['alias']
    
    if EXPORT_MAIL:
        email = emails.get(person['slug'])
        if email:
            ret = f"{ret}&nbsp;&lt;{email}&gt;"
    
    return ret.replace(" ", "&nbsp;")

def load_md(path):
    print("LOAD " + path)
    with open(path, 'r') as file:
        data = file.read()
    yaml_data = data.split("---")[1]
    body = "---".join(data.split("---")[2:])
    obj = yaml.safe_load(yaml_data)
    obj["body"] = body


    if obj["type"] == "event":
        for item in obj["schedule"]:
            try:
                item["time"] = sanitize_time(item["time"])
            except:
                pass

    store[obj["slug"]] = obj

# load all data
for root, dirs, files in os.walk("data"):
    for file in files:
        if file.endswith('.md') and not "__unused" in root:
            load_md(root + "/" + file)

def link_item(item, to, what):
    if not to.get(what): to[what] = []
    to[what].append(item)

# link entries (person -> contribution, etc.)
for slug in store.keys():
    item = store[slug]
    if item.get("contributors"):
        for contributor in item["contributors"]:
            person = contributor["person"]
            if person.startswith("$"):
                link_item(item, store[person[1:]], "contributions")
    
    if item.get("schedule"):
        for schedule_item in item["schedule"]:
            if type(schedule_item) == str: continue
            if schedule_item.get('item'):
                if schedule_item['item'].startswith("$"):
                    store[schedule_item['item'][1:]]["event"] = item
                if schedule_item.get('visuals'):
                    store[schedule_item['visuals'][1:]]["event"] = item

def render_schedule(event, do_hide=True, do_link=True, no_time=False, no_small=False):
    c = ""

    for item in event["schedule"]:
        title = item['item']
        authors = ""
        authors_sm = ""
        time = ""
        try:
            time = item['time']
        except:            
            no_time = True

        if item.get('hide_time'):
            time = ""
    
        item_venue = ""

        if item.get('hidden') and do_hide:
            continue

        if title.startswith("$"):
            obj = store[title[1:]]
            
            if item.get("venue", None) and do_hide:
                item_venue = f"<br><br><span style='position:relative;top:-10px;'>Venue: <em>{item['venue']}</em></span>"
            
            list_title = obj.get('list_title')
            if not list_title: list_title = obj['title']

            title = list_title

            if do_link and not item.get("no_link"):
                title = link_to_item(f"<em>{title}</em>", obj)

            if item.get("screening"):
                item_venue = "<br><br><span style='position:relative;top:-10px;'>(Video Screening)</span>"

            for contributor in obj["contributors"]:
                if authors != "":
                    authors += "<br>"
                    authors_sm += ", "
                
                if contributor["person"].startswith("$"):
                    author = store[contributor["person"][1:]]

                    author_text = render_name(author, display="reverse")

                    if do_link:
                        author_text = link_to_item(author_text, author)

                    authors += author_text
                    authors_sm += author_text
                else:
                    authors += contributor["person"]
                    authors_sm += contributor["person"]
        else:
            title = f"{title}"

        time_cell = f"<td class='time-cell'>{time}</td>"
        if no_time: time_cell = ""

        if authors_sm != "":
            authors_sm = f"<div class='d-md-block mt-0 d-lg-none' style='margin-bottom: 10px;'>{authors_sm}</div>"

        if no_small: authors_sm = ""
                
        if item.get("visuals", None):
            vis = store[item["visuals"][1:]]
            vis_cont = vis["contributors"][0]["person"][1:]
            vis_person = store[vis_cont]
            vis_auth = render_name(vis_person, display="reverse")

            vis_title = vis['title']

            if do_link:
                vis_title = link_to_item(vis_title, vis)
                vis_auth = link_to_item(vis_auth, vis_person)

            vis_auth_sm = f"<span class='d-md-inline mt-0 d-lg-none' style='margin-bottom: 6px;'><br>{vis_auth} &ndash; </span>"

            if no_small: vis_auth_sm = ""
            vis_time_cell = "<td></td>"
            if no_time: vis_time_cell = ""
            c = c + f"<tr style='border:none;'>{time_cell}<td>{authors_sm}<strong>{title}</strong>{item_venue}</td><td class='d-md-none d-sm-none d-none d-lg-table-cell'>{authors}</td></tr>\n"
            c = c + f"<tr style='border:none;'>{vis_time_cell}<td>Visuals: {vis_auth_sm}<strong><em>{vis_title}</em></strong>{item_venue}</td><td class='d-md-none d-sm-none d-none d-lg-table-cell'>{vis_auth}</td></tr>\n"
            c = c + "<tr></tr>"
        else:
            c = c + f"<tr>{time_cell}<td>{authors_sm}<strong>{title}</strong>{item_venue}</td><td class='d-md-none d-sm-none d-none d-lg-table-cell'>{authors}</td></tr>\n"
                    
    return c

def master_schedule_event(slug):
    print("Master Schedule - processing: " + slug)
    event = store[slug]
    c = ""

    venue = ""
    if event['venue']:
        venue = f", <em>{event['venue']}</em>"

    chair_string = ""
    if event.get('chair'):
        chair = store[event['chair'][1:]]
        chair_string = f"<br><br>Chair: {link_to_item(render_name(chair, 'no_alias'), chair)}"

    c = c + f"<tr><td colspan='3'><h3>{event['title']}</h3>\n{event['date_time']}{venue}{chair_string}</td></tr>"

    c = c + render_schedule(event, MASTER_SCHEDULE_DO_HIDE, False, False, True)

    c = c + "<tr><td style='padding-bottom: 50px;'></td></tr>\n"
    return c

def render_master_schedule():
    c = ""

    for item in store["__master"]["schedule"]:
        if type(item) == str:
            if not item.startswith("$"):
                c = c + f"<tr><td colspan='3'><h2>{item}</h2></td></tr>"
            else:
                c = c + master_schedule_event(item[1:])
        else:
            if item.get('hidden') and MASTER_SCHEDULE_DO_HIDE:
                continue

            venue = item.get('venue')

            if venue == None:
                venue = ""
            else:
                venue = "<br><br><span style='position:relative;top:-10px;'>Venue: <em>" + venue + "</em></span>"

            c = c + f"<tr><td style='padding-bottom: 50px;'>{sanitize_time(item['time'])}</td><td colspan='2'><strong>{item['title']}</strong>{venue}</td></tr>"
    
    with open("templates/master.html", "r") as file:
        master_template = file.read()

    master_content = master_template.replace("$CONTENT", c)
    master_content = master_content.replace("$VERSION", now.strftime('%d.%m.%Y'))

    with open("output/master-schedule.html", "w") as file:
        file.write(master_content)


# ---
# *** Render Status OVerview
# ---

with open("templates/status.html", "r") as file:
    status_template = file.read()

def render_status_overview():
    c = ""
    entries = []
    for slug in store.keys():
        entry = store[slug]
        if entry["type"] != "master":
            title = ""
            if entry["type"] == "person":
                title = render_name(entry)
            else:
                title = entry["title"]

            entries.append([entry["type"], slug, title, entry.get("status", "n/a"), entry])
    
    entries.sort(key=lambda x: (x[0] + x[1]).lower())


    for entry in entries:
        color = "#ff80ff"
        if entry[3] == "n/a": color = "white"
        if entry[3] == "proof": color = "#FFD580"
        if entry[3] == "ready": color = "#7CFC00"

        url = url_for_item(entry[4])
        if not entry[4].get("external"):
            c += f"<tr style='background-color: {color};'><td>{entry[0]}</td><td>{entry[1]}</td><td><a href='{STATUS_REL_PATH}{url}'>{entry[2]}</a></td><td><strong>{entry[3]}</strong></tr>\n"

    with open(CAT_OUT_PATH + "status-overview.html", "w") as file:
        file.write(status_template.replace("$CONTENT", c).replace("$VERSION", now.strftime('%d.%m.%Y')))

if INCLUDE_STATUS_OVERVEW:
    render_status_overview()    

# ---
# *** CATALOUGE
# ---


if not os.path.exists(CAT_OUT_PATH): os.makedirs(CAT_OUT_PATH)

with open("templates/catalogue.html", "r") as file:
    cat_template = file.read()

cache_bust = "99442"

cat_template = cat_template.replace("$CACHEBUST", cache_bust)
cat_template = cat_template.replace("$HEADER", HEADER)
cat_template = cat_template.replace("$CAT_HOME", CAT_HOME)

def write_cat_html(path, title, content):
    html = cat_template
    html = html.replace("$TITLE", title)
    html = html.replace("$MAINCONTENT", content)
    html = html.replace("$PATH", path.replace(CAT_OUT_PATH, ""))

    with open(path, "w") as file:
        file.write(html)
    print("Wrote: " + path)

def title_for_item(item, include_type=False):
    ret = ""
    post = ""
    if include_type:
        post = " (" + type_description_for_item(item) + ")"
    
    if item["type"] == "person": ret = render_name(item)
    else: ret = str(item["title"])

    return ret + post

def link_to_item(text, item, always_link=False):
    do_link = True
    if not always_link:
        status = item.get("status", "not")

        do_link = ALL_STATUS_FLAGS_OK
        for flag in ACTIVE_STATUS_FLAGS:
            do_link = do_link or status.startswith(flag)
    
    if do_link:
        return f"<a href='{url_for_item(item)}'>{text}</a>"
    else:
        return text

def transform_body(md):
    return markdown.markdown(md, extensions=['footnotes'])

def get_body_chunk(body, chunk):
    tokens = body.split(chunk)
    if len(tokens) == 1: return body
    token = tokens[1]
    return clean_cell(token.split("# $")[0])


def content_for_person(item):
    print("Rendering person: " + item['slug'])
    affiliations = ""
    num_affiliations = len(item["affiliations"])
    if num_affiliations == 1:
        affiliations = f"<p>Affiliation: <strong>{item['affiliations'][0]}</strong></p>"
    if num_affiliations > 1:
        affiliations = "<p class='list-header'>Affiliations:</p><ul>"
        for affiliation in item["affiliations"]:
            affiliations += f"<li><strong>{affiliation}</strong></li>"
        affiliations += "</ul>"

    contributions = "<p class='list-header'>Contributions:</p><ul>"
    for contribution in item["contributions"]:
        if contribution['type'] != 'other':
            contributions += "<li><strong>" + link_to_item(title_for_item(contribution, True), contribution) + "</strong></li>"
    contributions += "</ul>"

    return f"""
        {affiliations}
        {contributions}
        <h4>Biography</h4>
        {transform_body(item["body"])}
    """

def build_contributors_list(item, seperator=", "):
    contributors = ""
    for contributor in item["contributors"]:
        if contributors != "": contributors += ", "
        person = contributor["person"]
        if person.startswith("$"):
            person = store[person[1:]]
            contributors += link_to_item(render_name(person, contributor.get("display")), person)
        else:
            contributors += person
    
    return contributors

def render_event_info(event, display_venue=True):
    venue = event.get('venue', "")
    if not venue: venue = ""

    if venue != "":
        venue = ", <em>" + venue + "</em>"
    
    if not display_venue: venue = ""

    if not 'date_time' in event: event_text = ""
    else:
        event_text = f"""
        <span style='font-weight: bold; font-size: 18px;'>{event['title']}</span><br>
        {event['date_time']}{venue}
        """
       
    return link_to_item(event_text, event)

def render_associated_event(item):
    if not item.get("event"): return ""
    event = item["event"]
    return render_event_info(event)

proof_abstract_disclaimer = "<p><em><br>The abstract is displayed here for proof-reading and will only be part of the published proceedings, not of the final version of this web catalogue.</em></p>"

def render_stream_recording_url(item):
    if item.get("stream_recording_url"):
        return f"<br><br><strong><a href='{item['stream_recording_url']}'>Live Stream Recording (YouTube)</strong></a>"
    else:
        return ""

def content_for_performance(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    proof_abstract = ""
    if PROOF_INCLUDE_ABSTRACTS:
        proof_abstract += "<h4>Abstract</h4>"
        proof_abstract += proof_abstract_disclaimer
        proof_abstract += transform_body(get_body_chunk(item["body"], "$ABSTRACT"))

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p class="list-header">Was performed at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>
        <h4>Program Notes</h4>
        {transform_body(body)}
        {proof_abstract}
    """

def content_for_paper(item):
    body = get_body_chunk(item["body"], "$ABSTRACT")

    doi_string = ""
    if item.get('doi_link'):
        doi_string = f"<p class='mt-4'>Publication: <a href='{item['doi_link']}'><strong>{item['doi_link']}</strong></a></p>"

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p class="list-header">Was presented at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>
        {render_stream_recording_url(item)}
        {doi_string}
        <h4>Abstract</h4>
        {transform_body(body)}
    """

def content_for_keynote(item):
    body = item["body"]
    # put in time and place
    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <p class="list-header">Was presented at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>
        {render_stream_recording_url(item)}
        <h4>Abstract</h4>
        {transform_body(body)}
    """

def content_for_workshop(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    proof_abstract = ""
    if PROOF_INCLUDE_ABSTRACTS:
        proof_abstract += "<h4>Abstract</h4>"
        proof_abstract += proof_abstract_disclaimer
        proof_abstract += transform_body(get_body_chunk(item["body"], "$ABSTRACT"))

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        <!-- <p><em>Put time/place here</em></p> -->
        {transform_body(body)}
        <!-- <p><em>Put requirements here (???)</em></p> -->
        {proof_abstract}
    """

def content_for_video(item):
    body = get_body_chunk(item["body"], "$PROGRAM_NOTE")

    yt_string = ""
    if item.get('youtube_url'):
        yt_string = f"<p class='mt-4'><strong><a href='{item['youtube_url']}'>Watch Video on YouTube</a></strong></a></p>"


    presented = ""
    if item["submission_type"] == "Community-Video":
        presented = f"""<p class="list-header">Was presented at:</p>
        <ul>
            <li>{render_associated_event(item)}</li>
        </ul>"""

    return f"""
        <p><strong>{build_contributors_list(item, ", ")}</strong></p>
        {yt_string}
        {presented}
        <h4>Description</h4>
        {transform_body(body)}
    """

def render_photo_gallery(item):
    if item.get("photo_gallery"):
        return f"<br><br><strong><a href='{item['photo_gallery']}'>Photo Gallery on Flickr</strong></a>"
    else:
        return ""

def content_for_event(item):
    body = item["body"]

    schedule = render_schedule(item, True, True)
    schedule = f"<table>{schedule}</table>"

    schedule_title = "Schedule"
    if item["event_type"] == "Concert": schedule_title = "Line-Up"

    venue_string = ""
    if item.get("venue"):
        venue = item.get('venue')
        
        if item.get('venue_url'):
            venue = f"<a href={item['venue_url']}>{venue}</a>"
        
        venue_string = f"<strong>Venue: <em>{venue}</em></strong>"

        if item.get("venue_address"):
            venue_string = f"{venue_string} ({item['venue_address']})"

    tickets_string = ""
    if item.get('tickets_url'):
        tickets_string = f"<br><br><strong>Find tickets <a href='{item['tickets_url']}'>here</strong>!</a>"

    chair_string = ""
    if item.get('chair'):
        chair = store[item['chair'][1:]]
        chair_string = f"<br><br>Chair: {link_to_item(render_name(chair, 'no_alias'), chair)}"

    return f"""
        <p><strong>{item["date_time"]}</strong><br>
        {venue_string}{tickets_string}{chair_string}{render_stream_recording_url(item)}{render_photo_gallery(item)}</p>
        {transform_body(body)}
        <h4>{schedule_title}</h4>
        {schedule}
    """

def content_for_other(item):
    body = item["body"]

    schedule = render_schedule(item, True, True, True)
    schedule = f"<table>{schedule}</table>"

    return f"""
        {transform_body(body)}
        <br>
        {schedule}
    """

def type_description_for_item(item):
    t = item.get("submission_type")
    if not t: t = item.get("type")
    return TYPES[t]

def content_for_item(item):
    if item["type"] == "person": return content_for_person(item)
    if item["type"] == "performance": return content_for_performance(item)
    if item["type"] == "paper": return content_for_paper(item)
    if item["type"] == "keynote": return content_for_keynote(item)
    if item["type"] == "workshop": return content_for_workshop(item)
    if item["type"] == "event": return content_for_event(item)
    if item["type"] == "other": return content_for_other(item)
    if item["type"] == "video": return content_for_video(item)


    return "<h2>No Content</h2>"

def render_item(item):
    if not item["type"] == "master":
        if item.get("external"):
            print("Skipping resource with external URL: " + item["external"])
        else:
            write_cat_html(path_for_item(item), title_for_item(item), content_for_item(item))

for slug in store.keys():
    render_item(store[slug])


# CATALOGUE INDEX

with open("templates/catalogue-index.html", "r") as file:
    cat_index_template = file.read()

def render_event_list(title, list):
    ret = ""
    ret += "<h4>" + title + "</h4>\n"
    ret += "<ul class='event-list'>\n"
    for slug in list:
        ret += "<li>"
        ret += render_event_info(store[slug], False)
        ret += "</li>"
    ret += "</ul>\n"
    return ret

#pprint.pp(store)

# THE SLUGS IN THE SLUG LIST HERE HAVE TO BE IN "EVENTS"
def render_catalogue_index():
    c = ""
    
    #c += render_event_list("Paper Presentations", ["paper-session-1", "paper-session-2", "paper-session-3", "paper-session-4", "paper-session-5"])

    #c += render_event_list("Community Reports", ["community-session-1", "community-session-2"])

    #c += render_event_list("Keynote Sessions", ["keynote-1", "keynote-2", "keynote-3"])
    
    c += render_event_list("Concerts", [
        "opening-concert",
        "concert-2",
        "concert-3-wed-sala-beckett",
        "concert-4",
        "concert-5-thu-sala-beckett",
        "concert-6",
        "concert-7-la-nau",        
        "concert-8-laut"    
    ])
    
    c += render_event_list("Workshops", ["workshops-1","workshops-2", "workshops-3"])

    #c += "<h4 class='mt-5'><a href='catalogue/other/video-gallery.html'>Video Gallery</a></h4>";

    #c += "<h4 class='mt-5'><a href='catalogue/other/community-report-videos.html'>Community Report Videos</a></h4>";


    #c += "<h4 class='mt-5'><a href='catalogue/other/programming-committee.html'>Programming Committee</a></h4>";

    
    c += "<br><br><h3>Contributor Overview</h3>\n"

    persons = []
    for slug in store.keys():
        if store[slug]["type"] == "person":
            persons.append([render_name(store[slug], "reverse"), slug])
    
    persons.sort(key=lambda x: x[0].lower())

    c += "<ul>"
    for person in persons:
        c += "<li>" + link_to_item(person[0], store[person[1]]) + "</li>"
    c += "</ul>"
        
    cat_index_template_t = cat_index_template.replace("$CACHEBUST", cache_bust)

    with open(CAT_OUT_PATH + "index.html", "w") as file:
        file.write(cat_index_template_t.replace("$MAINCONTENT", c))


#render_master_schedule()
render_catalogue_index()
