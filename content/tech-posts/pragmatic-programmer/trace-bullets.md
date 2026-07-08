+++
date = '2025-04-29T22:54:34+02:00'
draft = true
title = 'Pragmatic Programmer - Tracer Bullets'
+++

Reference: The Pragmatic Programmer, David Thomas, Andrew Hunt

Key Term: **Trace bullet development**

Tip #20: Use Trace bullets to find the target

Pragmatic, fast feedback loop is required during iteration. May it be when iterating on learning concepts chunks
by chunks, or working on a relatively large feature that cannot be completed in one-go.

Implement only required sections from each layer of knowledge/requirement, and get a complete end-to-end solution
working quickly.
Go from one requirement to some aspect of the final system quickly, visibly and repeatably. Get something working
early to show off, get feedback and buy in from your users.
Look for areas where you have doubts and the biggest risk lies, and then prioritize development so these are the first
area you address or code.

Tracer code/doc should not be just throwaway, but built for keeps, and containing all checking, structuring,
and documentation necessary. Project are never finished, there are always changes needed and functions to add. It
is an incremental approach.

Once the end-to-end tracer code/doc is setup, you can see how far or close you are from your target, and adjust
if necessary. Don't be surprised if the first attempts do not hit.

Tracer code is not the same as prototyping. With a prototype, we'd like to explore final aspects of a system and once
lessons have been learned, throw away and recode everything i.e. prototyping generates disposable code. With tracer
code, it is used to know how the code/doc as whole hangs together, and give developers an architectural skeleton on
which to hang code i.e. tracer code is lean and forms parts of the skeleton of the final system.

Protyping is reconnaissance and intelligence gathering which is done before any tracer code is written.

"The most daunting piece of paper is the one with nothing written on it"
