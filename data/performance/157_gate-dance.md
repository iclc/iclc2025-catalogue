---
slug: gate-dance
status: proof
title: Gate dance
event: concert-8-laut
type: performance
submission_type: Performance
time: Saturday, May 31, 19:45 - 23:00
contributors:
- person: $roma-gerard

---

# $PROGRAM_NOTE

In this performance, rhythmic patterns are produced by live coding binary signals 
using an embedded computer. The computer has a small screen and keyboard 
connection but very limited processing power. Sounds are improvised as
bit-wise operations between bit sequences. There is no difference between sound
or pattern. Life is reduced to an oscillation between two states.

# $ABSTRACT

Digital computers are often used to create models of the physical world. For
example, many digital sound synthesis techniques attempt to imitate musical
instrument sounds or are inspired by physical sound production or perception.
A different approach is looking at the specific affordances of the computer as
an instrument, without trying to reproduce other instruments. For example,
several non-standard synthesis techniques were developed by early computer
music practitioners [1].
0001 is a project that explores one-bit music [2] from an experimental live-coding
perspective. As found in early game consoles, one-bit sound is produce by
directly converting digital signals to voltage. Thinking in terms of bit sequences
makes it hard to reproduce analog instruments or sounds. Algorithmic one-bit
music can be seen as a form of low-complexity art [3].
So far, the project was based on SuperCollider as a live coding environment.
Coding was restricted to a few binary unit generators which were combined
to produce binary signals. However, strictly speaking this was not purely one-
bit. Multiple streams had to be mixed digitally in some non-binary way. The
ultimate solution was to build a custom computer that allowed multiple binary
outputs to be mixed in analog domain.
Gate dance is the first performance using a custom computer. While the system
is still in development, the current iteration is based on the Tiny Lisp Computer
by David Johnson-Davies 1. A picture is shown in the figure below. The ma-
chine is programmed in uLisp, an embedded Lisp implementation by the same
author. An Arduino Nano board is used during development for convenience,
although the final version will use an Atmega processor directly. The uLisp
implementation has been modified to allow writing binary signals at high speed
to four different ports. The resulting analog signals are mixed using potentiome-
ters. The Atmega chip is very limited in memory and processing power, which
demands creative solutions in the spirit of early game consoles. The perfor-
mance will be rhythm-oriented using a combination of square oscillators, noise
and binary patterns.

(IMAGE ONE BIT)


