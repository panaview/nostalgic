+++
date = '2026-07-25T23:05:50+01:00'
title = 'Networking: Taking the CCNP as a Software Engineer'
draft = false
+++

The CCNP is a certification network engineers usually target after a couple
of years. It's considered a major step-up from an associate-level certification like
the CCNA, and an important step towards specialization in a sub-field of networking.

I've decided to pass the CCNA myself this year, which I thought was a good first-step
into validating my networking expertise. I spent a month studying for the
exam, which I think is reasonable considering my profile:
- Bachelors in Computer and Communications engineering
- Masters in IoT and Embedded Systems
- ~3 Years of experience as a Software Engineer in the Networking industry

(NB: I have a lot of respect for those completing the exam with no prior computer science background. I can imagine its quite challenging!)

Although my current role does not involve day-to-day configuration of network equipment,
I still work with network-adjacent code and features. Having a good understanding of protocols
and their limitations can help anticipate roadblocks and customer demands.

The CCNA has been a great stepping block, but as my day-to-day work
starts involving a larger breadth of protocols and concepts (BGP, MPLS, RSPAN, VPNs..),
I took the decision to start studying the CCNP material to have a better understanding
of current standards.

# Which CCNP Exam ?

![CCNP Exams](https://learningnetwork.cisco.com/sfc/servlet.shepherd/version/renditionDownload?rendition=THUMB720BY480&versionId=0686e00000hyDs1&operationContext=CHATTER&contentId=05T6e00002B07fL&page=0)

There are multiple possible tracks to obtain the CCNP. My current target is to pass the CCNP ENCOR (core) / CCNP ENARSI (specialization) exams, as I have been working mostly on enterprise-networking oriented features.

Other tracks I've considered are:
- ENCOR + ENSLD: Prefered ENARSI over ENSLD, as the later deals more with architecture challenges and not how protocols work in-depth
- AUTOCOR: provides knowledge about automation / infra-as-code, but not much about protocols themselves.
- SPCOR: provides knowledges on important service-provider protocols (MPLS, SR/SRv6), but not as much breadth.   

There are concepts of direct interest to me that I will be missing with the path I selected, which include:
- Segment Routing (covered in SPCOR)

# Timelines and Learning objectives

After skimming through the CCNP ENCOR/ENARSI material, a good first objective would be to pass ENCOR in 3 month's time (by end-of-October 2026)
and then assess how to approach the ENARSI.

Effectively, this requires:
- Selecting which material to follow consistenly (OCG, Cisco U)
- Setting a consistent labbing strategy - works gives me access to Cisco CML but I can also consider Containerlab - having a repo to submit my lab topology with CI/CD would be a nice touch
- Flashcards to keep myself up-to-date on key definitions and topics
