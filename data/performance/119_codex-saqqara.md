---
slug: codex-saqqara
status: proof
title: Codex_Saqqara
event: opening-concert
type: performance
submission_type: Performance
time: Tuesday, May 27, 18:00 - 20:30
contributors:
- person: $dal-ri-francesco
- person: $zanghellini-francesca

---

# $PROGRAM_NOTE

Codex_Saqqara is a duo formed in 2022 by Francesco Ardan Dal Rí (live coding)
and Francesca Zanghellini (electric violin, effects). They aim at exploring
the possibilities of co-creations between different musical practices allowed by
interactive ecosystems. At the heart of the project, five recording slots that can
be filled by the violinist and recalled by the live coder, establishing a game of
mutual exchange of musical ideas, in which the live coder has no control over
the sound material, while the instrumentalist has no control over its structural
organization. The performance is improvised from scratch, always seeking new
musical solutions by exploiting the interaction and collaboration. As such,
rehearsals are carried out trough exercises designed to refine communication
mechanics. For this performance, only two constraints are predefined: 1) the
duration (10/15 minutes); and 2) the starting sound (a C3 pizzicato). From
there, anything can happen.

# $ABSTRACT

The Codex_Saqqara project was originated in 2022, from an idea by Francesco
Ardan Dal Rí (live coding) and Francesca Zanghellini (electric violin, effects).
Initially concieved as a series of experiments to explore novel forms of interactions
between different musical practices, as discussed in [^1], our duo has since evolved
into an established ensemble.

The underlying architecture which allows for mutual interaction is based on
SuperCollider. At the beginning of each performance, we allocate five empty
buffers. At any time, the violinist can record or overwrite short audio sampled
chuncked from her instrumental improvisation, which became instantly available
for the live coder to be processed and organized into structures using a custom
environment in TidalCycles. This fosters a dynamic interplay in real-time, in
which both musicians can manipulate each other’s contributions, thus making
the musical dialogue developing in a collaborative fashion. Moreover, this also
injects a further level of uncertainty: indeed, the violinist can decide which audio
materials to provide and when to overwrite them, but has no clue on how and
when they will be exposed; on the other hand, the live coder can elaborate such
materials and organize them into musical structures, but can’t know them a
priori and needs to quickly adapt to sudden changes. As such, musical directions
within the performances are mutually co-mediated. To help us navigating trough
this interaction, we exploited the visual component, consisting of five colored
circles arranged in two areas of the screen. The circles at the bottom represent
the five recording slots, and change color when they are overwritten. The larger
circles at the top appear and disappear whenever one of these slots is recalled
by the compiler. This visual feedback, coupled with a reasonably simple coding
style, is also intended to support audience appreciation of the musicians’ choices;
the projection of the screen, in line with common praxis [^2], is also in this case a
fundamental part of the performance itself.

Our experience with Codex_Saqqara is grounded into the concept of shared
agency within performance ecologies [^3]. As highlighted in [^1], several challenges
are posed by such ecosystem, e.g. the different reaction time between instrumen-
talist and live coder [^4]; the impact of mutual interaction on musical processes [^5];
or the blurriness of the boundaries between traditional musical roles [^6]. Since
our practice embrace an improvisational and from-scratch approach, we do not
tackle these challenges by following pre-estabilished structures. Rather, we build
and evolve our ideas trough autoethnographic processes [^7], usually via a series
of rehearsing, often in the form of exercises designed to refine our communication
mechanics and to test specific sonorities, at the end of which we discuss the
musical outcome in relation to what we were thinking while performing. Such
techniques helps us build awareness and improves our collaborative skills within
the performance, promoting flexibility and adaptability.

As such, the formal developing of the musical performance we present here cannot
be described in advance since it is not prededermined. For the performance here
presented, we only defined two constraints: 1) the duration, between 10 and 15
minutes; and 2) the starting sound, a short C3 pizzicato, the lowest notes on the
5-string electric violin.

Finally, although the musical outcome of our performance is strongly influenced
by our personal experience as a duo, the code is open-source and can be easily
tailored to be used by hybrid instrument/computer ensembles. We therefore
hope to stimulate other performers to build their collaborative projects.

[^1] Dal Rì, F. A., Zanghellini, F., & Masu, R. (2023). Sharing the Same Sound:
Reflecting on Interactions between a Live Coder and a Violinist. In Proceedings
of the International Conference on New Interfaces for Musical Expression.

[^2] Lee, S. W. (2019). Show Them My Screen: Mirroring a Laptop Screen
as an Expressive and Communicative Means in Computer Music. In NIME
(pp. 443-448).

[^3] Stapleton, P., Waters, S., Ward, N., & Green, O. (2016). Distributed Agency
in Performance. In Proc. of International Conference on Live Interfaces.

[^4] McLean, A., & Wiggins, G. (2009). Patterns of movement in live languages.

[^5] Magnusson, T. (2009). Of epistemic tools: Musical instruments as cognitive
extensions. Organised Sound, 14(2), 168-176.

[^6] Masu, R., Bettega, M., Correia, N. N., Romão, T., & Morreale, F. (2019).
ARCAA: A framework to analyse the artefact ecology in computer music per-
formance. In Proceedings of the 9th International Conference on Digital and
Interactive Arts (pp. 1-9).

[^7] Neustaedter, C., & Sengers, P. (2012). Autobiographical design in HCI
research: designing and learning through use-it-yourself. In Proceedings of the
Designing Interactive Systems Conference (pp. 514-523).
