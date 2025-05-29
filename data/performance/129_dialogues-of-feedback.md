---
slug: dialogues-of-feedback
status: proof
title: Signals
event: concert-8-laut
type: performance
submission_type: Performance
time: Saturday, May 31, 19:45 - 23:00
contributors:
- person: $zybinska-paulina
- person: $zaccuri-andrea
- person: $sanz-luis

---

# $PROGRAM_NOTE

unsorted.love’s live coding performance centers on creating a dynamic feedback loop
between the audience, the code, and the music, transforming spectators into active
participants. Using a custom-built balloon equipped with movement and location sensors,
audience members generate real-time data that is streamed into both the visual and audio
live coding environments. This input influences visual elements in p5live and hydra, while
also shaping the music generated in SuperCollider, allowing the audience to directly affect
the sonic and visual aspects of the performance.

# $ABSTRACT

unsorted.love performance is grounded in the belief that creating a feedback loop between
the audience and the live coding system can significantly enhance the audience’s experience
(Burland, K. and McLean, A. (2016) “Understanding live coding events,” International Journal of
Performance Arts and Digital Media, 12(2), pp. 139–151. doi:10.1080/14794713.2016.1227596).
The feedback loop introduces an element of unpredictability and interactivity, making the
performance feel more dynamic and alive. To accomplish this, we aim to integrate human
feedback directly into the live coding process, allowing the audience to play an active role in
shaping the visual and auditory elements of the show. This is crucial to our practice because,
based on feedback from our mostly Swiss-based audiences, participation plays a vital role in
their perception that the audiovisual performance is truly happening in real time. When the
audience can see their actions having a direct impact on the visuals or sound, the sense of
immersion and involvement intensifies. As a result, the boundary between coder, audience,
and system becomes more fluid, enhancing the sense of “liveness” and immediacy that is
core to live coding performances.

Previously, we’ve used cameras and microphones to give the audience a way to interact with
the visuals. However, this form of interaction often feels too straightforward and fails to
engage audience members who are standing further away from the live coders. To overcome
these limitations, we have designed a custom-made balloon equipped with multiple sensors
that is handed to the audience during performances. This balloon captures real-time
data—such as movement and location—through gyroscope sensors. The data is streamed
from an Arduino system to a web browser using the MQTT protocol, and this information is
mapped to various parameters driving the visuals within the p5live and hydra coding
environment.

We've recognized that, as live coders, we often fall back on familiar code snippets and ideas.
However, by allowing the audience to influence aspects of the code, the generative process
becomes unpredictable for us as well. This disruption breaks our habitual routines and encourages 
us to think outside of the box, explore new creative directions, and improvise in
response to the ever-changing input from the audience. Audience participation not only adds
variety to the performance but forces us to continually adapt, leading to more dynamic and
innovative results (Françoise, J., Alaoui, S.F. and Candau, Y. (2022) “CO/DA: Live-Coding
Movement-Sound Interactions for Dance Improvisation,” in CHI Conference on Human Factors
in Computing Systems. doi:10.1145/3491102.3501916).

One of the challenges we’ve encountered with this approach is balancing the level of
audience influence so that it feels meaningful but not overwhelming. Too much control could
shift the focus away from the core narrative of the performance, while too little might make
the participation feel insignificant (Bakker, S.S. and Niemantsverdriet, K.K. (2016) 'The
Interaction-Attention Continuum: Considering various levels of human attention in interaction
design,' International Journal of Design, 10(2), pp. 1–14.

https://pure.tue.nl/ws/files/30619768/bakkinte2016.pdf.). Additionally, managing the
real-time data from multiple sensors presents technical challenges in terms of stability and
latency, which are crucial for maintaining the sense of immediacy in the performance.
Looking forward, we aim to further refine this system, experimenting with more complex data
inputs and exploring new ways to deepen the interaction between the audience and the
performance. Our goal is to continue evolving this dialogue between live coders, algorithms,
and the audience, reinforcing the sense of liveness and shared creativity
