---
slug: adding-live-coding-music-capabilities-to-the-microblocks
status: proof
title: Adding Live Coding Music Capabilities to the MicroBlocks Educational Programming Language
event: papers-1
type: paper
submission_type: Papers
time: Wednesday 28th, 10h-11:30h
contributors:
- person: $romagosa-bernat
- person: $mor-enric
- person: $maloney-john

---

# $ABSTRACT

his paper describes the process of adding live music coding capabilities to a programming language for microcontrollers not originally designed for that purpose. MicroBlocks, both developed and used by the authors, was designed from the ground up to be interactive, concurrent, and welcoming and intuitive to beginners. Those features, along with a visual code representation that makes the code more readable by the audience in a live-coding performance, make MicroBlocks attractive for live coding music.

When designing a live coding music language, two of the most essential components are the timing engine and the sound generation engine. Although MicroBlocks had neither of those components, testing showed that its virtual machine is fast and efficient, with low-latency task switches. Those properties allowed us to build rhythm abstractions in MicroBlocks with timing precision comparable to many production live coding languages.

Adding sound generation to MicroBlocks posed more of a problem. After exploring three different methods, our preferred solution is to externalize sound generation by sending commands to a General MIDI sound module.

In this paper, we describe a set of libraries that make it possible to perform live-coded music with MicroBlocks. We explain the reasoning behind each abstraction and show examples of its use.

MicroBlocks has now been used in numerous live coding performances in Barcelona and elsewhere. Overall, we've found MicroBlocks to be a viable option for live music performances. Furthermore, since MicroBlocks is easy to learn, it may be useful in music education and welcoming to experienced musicians with limited coding experience.


