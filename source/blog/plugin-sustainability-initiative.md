---
blogpost: true
date: Feb 22, 2026
author: Tim Monko
location: World
category: news, help-wanted
language: English
---

# Building the napari Plugin Sustainability Initiative

[napari](https://napari.org/) is an open-source, multidimensional image viewer for Python that provides core infrastructure for visualizing and annotating scientific imaging data. Its extendable GUI has empowered a diverse ecosystem of over 580 [community-developed plugins](https://napari-hub.org/). Since the public announcement of napari in 2019 and the addition of plugin support soon after, collaboration among core contributors, plugin authors, and users has enabled research workflows that no single library could accomplish alone. One advantage of napari and its plugin ecosystem is that it enables advanced scientific processing, without necessarily requiring any code, lowering the barrier to entry for domain scientists who need powerful tools to analyze their data. In this way, napari serves as an *entry point* into scientific programming for many researchers.

In recent years, however, collaboration between plugin developers and the napari core team has declined, leading to challenges in keeping plugins up to date and aligned with napari's evolving architecture. With financial support from the [United States Research Software Sustainability Institute (URSSI) Early Career Fellowship](https://urssi.us/blog/2025/07/02/call-for-proposals-urssi-early-career-fellows-round-2/), I've been working with the napari community since October 2025 to improve the plugin ecosystem's sustainability. Our goal is to build infrastructure and practices that other scientific software communities can learn from and adapt.

This post is an update on where the Plugin Sustainability Initiative stands after several months of active working group meetings and development.

## How I got here

In 2022, I was drawn in by the community and [Chan Zuckerberg Initiative's (CZI)](https://chanzuckerberg.com/) promotion of napari as a *fast* image viewer ready for complex, modern scientific imaging data. The plugin ecosystem was bolstered by a number of [CZI plugin grants](https://chanzuckerberg.com/rfa/napari-plugin-grants/), welcoming [instructional material](https://napari.org/stable/plugins/index.html), the [napari plugin template](https://github.com/napari/napari-plugin-template), and a growing community of enthusiastic developers. I started developing [napari-ndev](https://ndev-kit.github.io/) to bring bioimage analysis tools to my collaborators—without that opportunity to contribute a plugin, I never would have had the learning experience that led me to become a core contributor and community manager for napari.

## How ecosystems drift apart

The early growth of the plugin ecosystem was exciting, but it came with challenges: the plugin system was still maturing, many developers were new to Python and packaging, and there was little infrastructure for long-term maintenance.

- Many plugins were built on top of rapidly evolving napari and plugin APIs.
- Plugins, often developed by domain scientists, slowed in maintenance or stopped receiving updates.
- Dependency libraries naturally diverged, causing compatibility issues.

Our 2023 napari survey captured this well: 86% of respondents said creating a plugin was easy, but many mentioned the burden of maintenance. In community meetings, certain pain points keep coming up: lacking plugin discoverability and quality assessment, dependency hell due to complex environments, confusion about deep learning and GPU-accelerated tooling, and most tellingly, that domain scientists don't have the time, resources, or expertise to maintain software long-term.

These plugins are often *critical to the workflows of their users*. This creates a trust issue: users hesitate to adopt new versions of napari or novel plugins, fearing that their workflows might break. The disconnect went both ways—plugin developers felt dependent on napari but detached from its direction, while core contributors lost touch with what the broader ecosystem needed.

## What we've learned from the working group

In October 2025, we [recruited](https://napari.zulipchat.com/#narrow/channel/212875-general/topic/Announcing.20the.20plugin.20sustainability.20initiative!/) community members and established the Plugin Sustainability Initiative working group. The group [meets weekly](https://napari.org/stable/community/meeting_schedule.html) at alternating times for global participation, and includes members from diverse scientific backgrounds and napari roles—core team, plugin developers, facility engineers, and users. Our [working group notes](https://hackmd.io/@napari/plugin-wg) are public.

The most surprising outcome hasn't been the list of familiar challenges, but how much the community *wants to help build and shape solutions*. Plugin developers have volunteered to review each other's work. Instructors have offered to write documentation about Git and GitHub basics. Active developers have suggested programs where unmaintained plugins could find new maintainers. The conversation was never "what should napari do for us?" but rather "how can we work together to make this better?"

Several concrete themes have emerged from our meetings:

- **Plugin discoverability is broken in practice.** One developer described searching the plugin hub for deep-learning plugins with specific segmentation models and being unable to find the ones that actually work. Users need to know not just what exists, but what is maintained and what works with their version of napari.
- **The "composable tools vs. monolith toolbox" tension is real.** napari's documentation recommends small, composable widgets, but the community has gravitated toward large, self-contained toolboxes that replicate an ImageJ-like experience for domain-specific workflows. Both patterns are valid, but they need different infrastructure, documentation, and discovery mechanisms.
- **Reproducible environments are a solvable problem.** Working group members have championed the use of lock files with tools like [Pixi](https://pixi.sh/latest/) and [uv](https://docs.astral.sh/uv/) to create reproducible, fast-resolving environments. This opens the door to curated plugin bundles—think `pixi global install napari-essentials`—that are tested to work together.
- **Plugin donation and stewardship resonated.** The idea that developers could "donate" unmaintained plugins to the community for new stewards to pick up got shared smiles from every meeting where it came up. We're exploring how a community-led plugin organization could facilitate this program.

As one member put it: plugin developers often see the core napari team as shepherds of the whole ecosystem, but they rely on the core team in ways the core team doesn't always know about and can't always support. People want ways to be involved more broadly with the *whole ecosystem* without necessarily contributing to the core tools—we just need to build the right infrastructure.

## What we're building, together

The working group has converged on three interconnected priorities, with the community review system emerging as the most immediate focus.

### 1. Automated and community review systems

This is where we're starting. The working group has consistently prioritized the review system as the highest-impact effort, and we're building it with both automated and human components.

**Automated review tooling** is being developed to evaluate napari plugins against best practices. Inspired by [SciPy's repo review](https://repo-review.readthedocs.io/en/latest/) and the former [napari-hub-cli](https://github.com/chanzuckerberg/napari-hub-cli), this tooling will check plugin repositories for common issues—packaging quality, test coverage, dependency health, CI configuration—and provide actionable feedback. We're also working on using [npe2api](https://github.com/napari/npe2api) to run compatibility checks against napari itself, so we can detect when plugins break and surface that information to developers and users. A key design goal is to use CI to continuously check whether plugins install and function correctly, so that sustainability information stays current rather than becoming stale metadata.

**A tiered recognition system** has taken shape through working group discussions. Rather than a binary "reviewed/not-reviewed" label, we're moving toward a system with levels like "essentials" (curated, actively maintained, broadly useful), "community-reviewed" (peer-reviewed by experienced developers), and "dependency-verified" (automated checks pass). This addresses a real need: very specific but powerful plugins like microSAM serve smaller audiences, and a flat ranking wouldn't serve them well. The tiered approach lets different kinds of quality be recognized, especially when plugins target particular niches in a domain-specific manner.

**Human peer review**, inspired by [PyOpenSci's model](https://www.pyopensci.org/about-peer-review/), will pair experienced community members with plugin developers for constructive feedback on maintainability, discoverability, and best practices. Community members have already volunteered to serve as reviewers, and we're exploring formats including live video review sessions. We hope to build a partnership with the [Journal of Open Source Software (JOSS)](https://joss.theoj.org/) [similar to PyOpenSci's](https://www.pyopensci.org/software-peer-review/partners/joss.html), giving reviewed plugins a fast track to publication.

Together, automated tooling provides continuous, scalable feedback while human review offers the nuanced, domain-aware guidance that no tool can replace. Both feed into the tiered recognition system to give users meaningful signals about plugin quality.

### 2. Modernize plugin development infrastructure

We're actively updating the [napari-plugin-template](http://github.com/napari/napari-plugin-template) and [plugin documentation](https://napari.org/stable/plugins/index.html) to follow current best practices from [PyOpenSci](https://www.pyopensci.org/), [Scientific Python](https://scientific-python.org/), and the [Python Packaging User Guide](https://packaging.python.org/en/latest/). Working group members have contributed firsthand accounts of upgrading their own plugins, and those real-world experiences are directly informing the template and documentation updates. This includes:

- Clearer guidance for people new to Python packaging, Git, GitHub, testing, and continuous integration
- Better documentation of sustainable design patterns, especially separating computational code from UI code—a point the working group has emphasized repeatedly
- Real-world-tested upgrade paths for existing plugins, informed by members who have gone through the process themselves
- Guidance for reproducible environments using lock files with Pixi and uv
- Reorganized documentation with distinct beginner and advanced tracks, including a "your first plugin" guide prior to the template

### 3. Better discoverability and ecosystem communication

The automated tooling and review system provide the foundation for improving how users find and trust plugins. We're working on:

- Surfacing sustainability information (maintenance status, compatibility, last update) on the [napari hub](https://napari-hub.org/)
- Distinguishing composable tool plugins from standalone toolbox plugins in search and metadata
- Enabling plugin donation programs where maintainers can hand off plugins to new stewards
- Exploring a napari-plugins GitHub organization for community-maintained plugins
- Improving communication about napari API changes that may impact plugins, potentially through automated notifications

## Why it matters beyond napari

These challenges—sustaining domain-specific extensions, coordinating between foundational and downstream projects, supporting novice contributors while maintaining quality—aren't unique to napari. They show up across scientific software.

What might be transferable from this work is the approach of:

1. **Treating extensions as collaborative partners**, not external add-ons
2. **Creating shared ownership** through working groups that include core and extension developers
3. **Building infrastructure for collaboration**, review systems, donation programs, and maintainer partnerships
4. **Combining automated and human review** to provide scalable feedback without losing the nuance that domain expertise brings
5. **Enabling cross-domain learning** where advances in one field benefit others through upstream contributions.
6. **Recognizing all kinds of contributions** to the ecosystem, from code to documentation to review and mentorship, and providing pathways for people to get involved in different ways.

Everything we create—templates, review tools, documentation—is open source and documented for other communities to adapt.

## Thank you

This project is supported by the URSSI Early Career Fellowship, with funding from the Sloan Foundation. Thank you to URSSI and the Sloan Foundation for making this work possible, and to the napari community for showing up and building this together.

The most important outcome isn't any particular tool or program—it's that the collaborative relationship between napari and its plugin ecosystem is healthier than it has been in a while. When foundational tools and their extensions work together, everyone benefits: developers don't duplicate effort, users get more reliable tools, and research moves forward on steadier ground.

## Contact and follow along

If you're working on scientific software with an extension ecosystem, or if you're curious about sustainability practices for open source communities, we would love to hear from you.

You can follow our progress and join the conversations on [Zulip](https://napari.zulipchat.com/). Keep an eye on [the napari blog](https://napari.org/island-dispatch/), where we'll share updates on the review system rollout, infrastructure releases, and working group insights over the coming months.
