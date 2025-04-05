---
slug: music-on-the-fly-with-pharo
status: proof
title: Music on-the-fly with Pharo
type: workshop
submission_type: Workshop
time: 11:00 - 13:00
contributors:
- person: $cipriani-domenico

---

# $PROGRAM_NOTE

The workshop is articulated in 4 sections of different durations.
During the first section, the participants will be supervised while installing 
Pharo, Coypu, SuperCollider and SuperDirt (for Linux, macOS or Windows).
In the second section, the focus shifts to introducing the syntax of Pharo and
Coypu, their main features and their most relevant classes and methods to
program music on-the-fly.
In the third section we will explore the polysemic nature of Coypu, i.e.
different ways to compose and manipulate patterns encouraging the
participants to compose their own performance using SuperDirt as an audio
engine for Pharo.
In the last section we will explain how to install the Phausto package for
Pharo; this packages enables the generation of sounds from within Pharo
without the need of any external audio client; participants will be guided on
how to load sound kits from the Phausto standard library and to perform with
them, and simple DSPs can be written in Phausto.
The goal of the workshop is to allow the participants to program music on-the-fly 
with Pharo and Coypu using both SuperDirt and Phausto for audio
generation. Additionally we aim to underline the fundamental principles of
pure object-oriented programming, highlighting the power of inheritance and
abstraction. Also we want to exemplify the elegance of Pharo's reflective nature
and the ease of use of its class browser provides to implement new classes and
methods live.

# $ABSTRACT

Pharo is a fully open-source, dynamic, and reflective pure object-oriented language, forked from Squeak in 2008 by Stephane Ducasse and Marcus Denker. It implements the Smalltalk-80 paradigm and features an immersive development environment with live code evaluation. Pharo’s concise Smalltalk-based syntax—its instructions fit on a postcard—along with intuitive manipulation of Collections and Strings, forms the foundation of Coypu, a package we have developed over two years for live-coding music.

Coypu is designed for beginners with little or no computer skills, yet appreciated by experts for its simplicity and power. Drawing on Godfried T. Toussaint's research on musical rhythm geometry, Coypu provides a rich vocabulary for quickly creating and manipulating musical patterns, generating rhythms, timelines, chords, and arpeggios. Originally created as a server for OSC and MIDI clients, Coypu now integrates seamlessly with the SuperDirt audio engine for SuperCollider, taking inspiration from Tidal Cycles' mini-notation.

Together with Coypu, another library called Phausto that allows users to generate sounds, playback audio file by embedding the Faust programming language and dynamic interpreter in Pharo,

This workshop will guide participants in live-coding music using Pharo, Coypu, SuperDirt, and Phausto, while highlighting core principles of pure object-oriented programming, including inheritance and abstraction. We will also demonstrate Pharo’s reflective capabilities and the ease of creating new classes and methods on-the-fly. Following John M. Carroll’s minimalist instruction design, participants will actively shape their learning experience, making Pharo especially suited to constructivist approaches that help beginners form cognitive models of programming and live coding.

