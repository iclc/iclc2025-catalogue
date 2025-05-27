---
slug: kabelsalat-live-coding-audio-visual-graphs-on-the-web-and-beyond
status: proof
title: Kabelsalat -  Live Coding Audio-Visual Graphs on the Web and Beyond
event: papers-4
type: paper
submission_type: Papers
time: Thursday 29th, 12h-13:30h
contributors:
- person: $roos-felix
- person: $forment-raphael-maurice
doi_link: https://doi.org/10.5281/zenodo.15527772
---

# $ABSTRACT

This paper introduces KabelSalat, a graph-based live coding environment that targets multiple platforms and languages. It
works by translating a Domain Specific Language (DSL) based on JavaScript into a signal flow graph. This graph can
be compiled into a sequence of instructions optimized for real time signal processing. The compiler can either output
JavaScript code to run in the browser or optimized C code to run natively. The possibility of adding other target languages
is an integral part of KabelSalat’s design. The browser version includes a REPL and features a range of audio DSP nodes
reminiscent of modular synthesizers. Notable features include single sample feedback and multi-channel expansion inspired
by the SuperCollider audio engine. The core module of KabelSalat has also been used to implement a stripped down
version of the Hydra video synthesizer, thus demonstrating that the same underlying principles can be adapted both to audio
and video processing. In the future, KabelSalat might become an alternative audio engine for Strudel, offering more sound
design capabilities, compared to the current SuperDough engine, which uses the browser’s built-in Web Audio graph
