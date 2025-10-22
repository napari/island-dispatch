---
blogpost: true
date: Jul 3, 2025
author: Draga Doncila Pop
location: World
category: news
language: English
---

# napari roadmap blog post

We're excited to share what's coming next for napari! After months of listening
to our community and carefully planning our path forward, we're ready to pull
back the curtain on our new [development roadmap](https://napari.org/stable/roadmaps/active_roadmap.html). 
Whether you're a longtime napari user or just discovering what we're all about,
this roadmap is our way of showing you where we're headed and why we
think you'll love what's coming.

Earlier this year, we were awarded the CZI scaffolding grant, for USD$1.7M over 
four years. For the first time since napari's inception, we can fund dedicated 
development, community-management and project operations roles. This is an important 
milestone that has allowed us to step back, assess our goals, and chart a clear 
path toward long-term sustainability of the project, beyond the grant duration.

This roadmap reflects our commitment to transparency, predictable releases, better 
documentation, and a thriving contributor community. With renewed energy and focus, 
we’re laying the foundation to ensure napari and its community can thrive for years 
to come. Read on to learn more about the roadmap process, our key focus areas, our 
2025 priorities (and progress towards them!) and how you can get involved in 
bringing the goals of the roadmap to life.

## Why roadmap?

Thanks to a thriving community of contributors and core developers, an increasing
user-base, and our ever-growing plugin ecosystem, napari has grown rapidly over the years.
Yet, we aspire to raise the bar to ensure the project is reliable and
sustainable in the long-term. New features are critical to enable the evolving analysis
workflows of our users. Over the past six years, the project has also accrued technical debt,
as a natural evolution of technology. This makes it more difficult to build these new features,
and is an obstacle for new contributors to join the project. As the project has grown, the
complexity of our maintenance and development processes have as well. We've got a lot to do,
and we want to make sure we're doing it efficiently, effectively, and transparently.

The roadmap lays out all the wonderful things we want to get done in the near term,
and allows us to think strategically about where we're dedicating our effort.
Regularly updating the roadmap also gives us an opportunity to track our progress,
prioritize our time, and celebrate our successes!

But it's not all about us! Having an up-to-date roadmap makes it easier for the broader
community to know where we're going. We invite you to join us for the journey, by
expressing interest in particular items, providing feedback on implementation, financially
supporting a certain feature, or even implementing it with us.

## How roadmap?

We view the roadmap as napari's north star to guide future work.
Is work limited to what's on the roadmap? Absolutely not. We welcome ideas
for additional project features from our napari users. We'll be reviewing the
roadmap several times a year, and as science and technology changes, we
expect to evolve to meet your needs.

To put together the roadmap, we collected a whole bunch of information from community
discussions, core developer meetings, the original roadmap GitHub project, grant applications
and open issues. We then synthesised this information into focus areas, and individual
deliverables within each focus area.

Speaking of the original roadmap GitHub board -- we found that while it was a useful exercise
for organizing our thoughts and keeping some of our big features together in one place, there were
a couple of issues with the format that kept it from being as useful as it could be. For starters,
we found it difficult to think about items at a high-level, keeping discussion strategic rather
than getting stuck in the weeds about technical implementation issues. We also found it difficult
to keep updated -- the scattering of issues and feature requests was hard to reason about. Finally,
it just wasn't discoverable! It felt tucked away somewhere in a dark corner of the GitHub org
(in fact, most of our community probably don't know it ever existed), and was annoying to share and refer to.

To address this, we've also developed a process for reviewing and updating the roadmap on a
quarterly basis, so that it is always reflecting the current state of the project, our current
priorities, and our vision for the future. "The roadmap is a living document" is by far the
most important aspect of this new approach, and as a team, we are 100% committed to this process.

The roadmap does not list items in priority order -- we like to think of it as a menu to choose
from. Every 3-6 months (or longer, depending on much effort is involved in a particular feature),
we will pick items from the menu that the core team will focus on. During the review process,
we'll also take the learnings from planning and implementing previous items, and use them to
enhance, tweak or even remove existing deliverables on the roadmap to better reflect our desired vision for napari.

If you're interested in reading more about the process, the roadmap itself describes the
[approach and philosophy](https://napari.org/stable/roadmaps/active_roadmap.html#roadmap-strategy)
we took in shaping the document.  

## Roadmap

[The roadmap](https://napari.org/stable/roadmaps/active_roadmap.html) lists strategic deliverables
we are targeting across three focus areas:

- **Core Technology:** this is the biggest area and includes the code API, the API's implementation
(what frameworks and design patterns do we use, how do we use them), performance improvements and
all the "backend" refactors necessary to unlock exciting new opportunities - maybe even a Web viewer?
- **User Experience:** all the current interfaces to our `Viewer` (the bundled application,
'headless' mode, integration with Jupyter notebooks) and our plugin ecosystem.
- **Project Sustainability & Community:** our focus has always been on making `napari` a pleasant
and rewarding project to engage with. This area contains key items for ensuring we're up to par
on that front: high-priority bug fixes, improving our usage documentation and the napari website,
and fostering our incredible community.

We've already made a lot of progress on our priorities for 2025 (good thing too,
since we're more than halfway through the year now)! The 2025 prorities include:

- **Shape triangulation performance:** [Grzegorz Bokota](https://github.com/czaki) has
overhauled our triangulation machinery using a more performant triangulation algorithm.
It's written in Rust and lightning fast - we're talking more than ten times faster!
Read the [blog post](https://napari.org/island-dispatch/blog/triangles_speedup_beta.html) for more details.
- **Community-run napari hub:** Starting from a prototype built by [Yunha Lee](https://github.com/yunhal),
we've developed a lighter-weight, more maintainable version of the napari hub for sharing & discovering
plugins, managed by the napari community. It's due to launch any day now, and it's *also* faster -
though maybe not ten times faster. Check it out at [https://napari.org/hub-lite]()!
-  **Modular canvas:**  [Lorenzo Gaifas](https://github.com/brisvag) has revamped our grid mode
to use individual view-boxes for each layer (rather than smoosh all the layers together into
a single coordinate space). This not only makes grid-mode more powerful and more useful,
but is also a huge step towards true multicanvas capabilities. Lorenzo is now working to
get NAP-9 (the implementation design for multicanvas) updated and approved. Learn more about
the new grid mode in the [release notes](https://napari.org/stable/release/release_0_6_2.html),
or [weigh in on NAP-9](https://napari.org/stable/naps/9-multiple-canvases.html) to help push this work along!
-  **Decoupling library from application design:** This work has been in progress for a while now,
and we've finally got the time to finish the transition for good. Grzegorz Bokota is working
on an implementation plan that will see the old action manager deprecated, giving us a
unified system for registering and executing all viewer actions. This may not sound particularly exciting,
but it will pave the way for full viewer serializability, and richer ways for plugins to
contribute to the viewer, besides just widgets!
-  **Sustaining the project:** This roadmap is just one piece of the puzzle in our work to
ensure the long-term sustainability of napari. [Tim Monko](https://github.com/timmonko),
our new community manager, is looking at better ways to engage with our community, like
themed meetings, demo days and better support for plugin developers. We're also working
on a predictable and consistent release cadence, with monthly releases and dedicated release managers.
Thanks to [Carol Willing](https://github.com/willingc)'s proven open-source leadership
experience, as a 3-term Python steering council member, we have a clear process for
sustaining our roadmap.  With [Tracy Teal](https://github.com/tracykteal)'s expertise
in leading large open source organizations, like the Carpentries, we're investigating
potential avenues for generating revenue, so that we can maintain our operations beyond
the horizon of the scaffolding grant. To that end, we'll soon be trialing two pilot
programs: bookable office hours with our team, and hosting training workshops for
the broader community. We'll share more about these in the coming weeks.

## Get Involved!

We’d love to hear from you! If you have thoughts on [the roadmap](https://napari.org/stable/roadmaps/active_roadmap.html),
are excited about particular items, or have ideas for implementation, we welcome your feedback.
Community engagement is key to the project’s success -- whether you're interested in
contributing code, improving documentation, or helping shape priorities.
Check out our [GitHub organisation](https://github.com/napari) to explore open issues and ongoing work,
and consider joining our [regular community meetings](https://napari.org/stable/community/meeting_schedule.html)
to connect with other contributors.

If you or your organization is interested in supporting or funding specific
areas of development, holding a training workshop, or learning more about office
hours please don’t hesitate to reach out to our Steering Council member and napari
Operations Manager, Draga Doncila Pop, at draga@napari.org. We're on the road to tackling
this roadmap, and we're excited for you to join us on the journey!
