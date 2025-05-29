---
slug: istories-20-years-of-freesound
status: proof
title: Ιstoríes (20 Years of Freesound)
event: concert-3-wed-sala-beckett
type: performance
submission_type: Performance
time: Wednesday, May 28, 18:00 - 21:30
contributors:
- person: $anastasopoulou-panagiota

---

# $PROGRAM_NOTE

This live coding performance titled Ιstoríes celebrates Freesound’s 20th anniversary,
highlighting the platform’s impact on sound sharing and creativity. Using SuperCollider, we
retrieve and manipulate sounds from Freesound's heterogeneous collection of over 650,000
user-uploaded audio files in real time, creating an improvised composition that reflects the
diversity and unpredictability of the database. The performance navigates Freesound’s sonic
landscape through the Broad Sound Taxonomy, which categorizes sounds into semantic-based
classes. By embracing the dynamic nature of sound retrieval and remixing, this performance
transforms Freesound into a live instrument. It honors the platform’s collaborative spirit and
open-source ethos while demonstrating the platform’s role in fostering innovation within the
live coding and sound art communities.

# $ABSTRACT

As Freesound marks its 20th anniversary, this live coding performance, titled storíesΙ , is a
tribute to the platform's impact on sound sharing and creative collaboration. Freesound1 is a
website that hosts over 650,000 diverse sounds released under Creative Commons (CC) licenses
and contributed by a wide community of users. It has many different kinds of sounds, ranging
from natural field recordings to speech, music samples and abstract electronic textures. This
performance aims to emphasize both the platform's extensive sound library and its history by
featuring a selection of heterogeneous sounds as its sound material.

This performance draws on the wide heterogeneity of crowdsourced sounds from Freesound to
explore themes of diversity, remix culture, and transformation through a real-time dialogue
between humans (collaborative database) and the machine (algorithmic creation). To embrace
the unpredictability inherent in such a large database, the sounds are selected and retrieved in
real time during the performance. When making a query in Freesound, the order of the
returned sounds may change to factors such as new additions of sounds (~120 sounds per day),
which leads to varying results even when using the same queries. To manage navigating such a
big and diverse database, we use the Broad Sound Taxonomy which categorizes sounds into
broad yet semantically rich classes (see Fig. 1). The taxonomy enables the performance to
traverse a landscape of audio possibilities, resulting in a composition that reflects Freesound’s
extensive sonic diversity. With this approach, we have the benefit of being able to explore
different kinds of sounds while ensuring coverage of different areas within the database.
Filtering queries according to this taxonomic structure, allows us for targeted sound discovery,
reducing the ambiguities that often result from broad queries, and instead focusing on specific
types of sounds. Each sound is categorized using sound classification techniques based on
machine learning tools that predict the most appropriate category. This information is
precomputed and accessed through the Freesound API.
