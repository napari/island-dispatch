---
blogpost: true
date: Sep 1, 2026
author: Aniket Singh Yadav
location: World
category: Manual
language: English
---

# From `Any` to Certainty: A Typechecking Journey

## How I Got Into Typing

This is my first blog post. It’s all about how I started my open source journey and how I ended up spending most of my time working on typing in open source.

I’ll also talk about how and why we decided to replace our old type checker with a new one. If you’re trying to decide which type checker might be the best choice for your project, I hope this blog helps.

## Where It Started

I started contributing to open source about a year ago, and I joined napari in April. More specifically, my first pull request was on April 2nd. I still remember Tim welcoming me on my first issue. I don’t know about others, but for me, that small gesture meant a lot ❤️. I can say it’s one of the reasons I felt so motivated to keep contributing and wanted to be part of such a welcoming and supportive community.

Typing wasn’t really part of the plan. I became interested in it while working on SciPy-stubs with **Joren** (@jorenham). I still remember my late-night PRs, and Joren used to review them so quickly and merge them at light speed 😸. That’s where I started getting more interested in typing and decided to dive deeper into it.

*A special thanks to Joren — I learned so many things along the way ❤️.*

After that, I came back to napari and started fixing mypy errors and adding type hints across the codebase.

## Typing Across Scientific Python

My experience with typing has been a little different across napari and other Scientific Python projects.

In napari, I sometimes came across confusing annotations that weren’t properly typed. At times, the easiest way to fix them was to add something just to make mypy happy, even though it didn’t feel like the right solution.

I faced some similar issues while working on SciPy-stubs. Things like overlapping overloads and other mypy errors were confusing at first, but slowly I started to understand them. In some cases, we even had to disable mypy for an entire module. 😆

These experiences made me curious about better options. That’s when I came across newer type checkers like `ty` and `Pyrefly`. When I first tried `Pyrefly`, I was surprised by how much faster it was than `mypy`. After some time, I saw a PR in SciPy dropping `mypy` in favor of `Pyrefly`. That made me even more interested in this topic, and I wanted to open a thread for similar decision in napari.

But unfortunately, I was already late. 😭 Lorenzo (@brisvag) had already opened a PR to migrate from mypy.

More recently, I’ve also started doing some typing work in NumPy and Matplotlib. It’s been really interesting to see how different projects in the Scientific Python ecosystem handle typing.

## Can an LLM Do a Type Checker Migration for You?

This came up while working on napari#9375, where Lorenzo migrated the project from mypy to ty. So, can an LLM do the migration for you?

**Partly, yes.**

LLMs are pretty good at the repetitive part. If you have hundreds of similar errors across a codebase, they can help make bulk changes, add ignore comments, update suppressions, and take care of a lot of the boring work. That can save a lot of time. But here is the interesting part.

When a new type checker reports an error, someone still needs to understand **why**. Is there a real bug? Is the type checker missing something? Or does the code just need a better annotation? 

An LLM can make the error disappear by adding an `ignore` comment, but that doesn’t mean the problem is actually fixed. For me, the takeaway is simple:

> **LLMs can help with the boring part of a migration, but the important decisions still need you to understand and fix.**

## Choosing a New Type Checker

### Tim: How to Wrongly Implement a New Type Checker 😆

*(Just a joke — Tim actually did a great job!)*

After some discussion, we decided to give Pyrefly a try. Tim took the first shot at migrating the codebase from mypy to Pyrefly, and that started a bigger discussion about which type checker we should use: **ty or Pyrefly**.

We spent some time comparing both options and looking at the results from our codebase. After a few discussions, we decided to go with **Pyrefly**.

In this blog post, I’ll share the things we looked at and the factors that helped us make that decision. Hopefully, it can also help other projects that are trying to choose a type checker for their own codebase.

## Pyrefly: Nice Features for Legacy Codebases and Speed

Adding a type checker to a new project is easier than migrating from an old one, where you may have hundreds of modules and type checking that may have been quietly ignored and turned off years ago.

That’s napari. And maybe that’s your project too. 😆

Both tools have good support for migrating existing codebases, but Pyrefly's particular workflow and commands worked better for us. It has some built-in commands that make the complex parts smoother, and I consider them strong practical arguments in the decision:

* **`pyrefly init`** — It reads your old configuration and helps initialize Pyrefly.

* **`pyrefly suppress`** — It can silence everything at once.

* **`pyrefly suppress --remove-unused=all`** — You can remove unused suppressions later. This is an important part because Pyrefly tells you when you don’t need an ignore comment anymore. After fixing real problems, the comments can be cleaned up automatically.

* **`pyrefly infer`** — It can write annotations for you.

* **`pyrefly coverage`** — It can measure progress. The `pyrefly coverage` report tells you how much of your code is actually typed. You can also use coverage checks in CI. For example, `pyrefly coverage check --fail-under 80` can fail CI if your typing coverage drops below 80%.

* **Existing `# type: ignore` comments** — Your old comments still work. Pyrefly respects `# type: ignore` by default, so existing mypy suppressions can continue to do their job; however, Pyrefly cannot self-prune bare ignores, and require an error type like `# type: ignore [<error type>]`.

### Speed

Speed was another important factor for us.

Pyrefly checks over **1.85 million lines per second** and runs about **15 times faster than mypy and Pyright on PyTorch**.

The napari numbers are more concrete:

* **Mypy:** 15–25 seconds cold
* **Pyrefly:** 0.9 seconds cold, 0.7 seconds warm

## Ty vs Pyrefly: How We Decided

Our key deciding factors were these three, as we thought they played an important role:

1. **Speed**
2. **Configuration and maintenance**
3. **Error messages**

**Speed with tox:**

* **mypy:** ~15–25 s cold (warm cache ~0.5 s, but it invalidates on near-any edit)
* **ty:** ~1.9–2 s
* **Pyrefly:** ~0.7 s warm / 0.9 s cold

**Configuration and maintenance:**

The Pyrefly and ty configurations are quite different. The ty configuration is about **450 lines** because of complexity with ignore types managed in the configuration rather than inline with the code. In comparison, napari's Pyrefly config is about **140 lines**, although is mostly a long list of ignores that we hope to eventually be zero! I personally think Pyrefly is significantly better here, especially with its CLI commands.

**Error messages:**

The other user-facing part is the error message. We found ty to be more verbose and helpful, but compared with mypy, we found both to be clearer.

### Other Details

There are some other differences that I don’t think affected our decision as much:

* **Conformance:** Both are above 90% conformance with the typing specification, with Pyrefly being higher.

* **Maturity:** Pyrefly is 1.0+, while ty is not.

* **Pydantic support:** Pydantic is supported by both natively as of ty adding support in July 2026. Most information online is outdated on this.

* **Cross-platform consistency:** Our Linux developers may be surprised by this, but both `ty` and `mypy` are not reproducible on Windows, even with the `tox` configuration, because they type-check against Linux only. This means there is often noise locally or false positives/negatives that then have to be dealt with between local development and CI.

  Pyrefly allows setting the check to all platforms, resulting in better local/CI consistency for me.

  This means that:

  ```bash
  uv run pyrefly ...
  ```

  is consistent with tox as well.

* **Philosophy:** Pyrefly aggressively infers types in unannotated code, whereas ty does not report errors when you remove an annotation, so it is quieter.

## Resources

Here are some resources that can be helpful for a more in-depth analysis:

* [Typing Specification Conformance Results](https://htmlpreview.github.io/?https://github.com/python/typing/blob/main/conformance/results/results.html)
* [Python Type Checker Benchmark](https://python-type-checking.com/typecheck_benchmark/)

## Wrapping Up

It has been a really great experience getting into typing and working on it across different projects. I’ve learned a lot along the way, and I’m definitely going to keep working on it.

My next goal is to help make napari fully typed over the next few months, while continuing to contribute to other projects in the Scientific Python ecosystem. If you want to dive into the nitty-gritty details, you can find my work on GitHub: **@Aniketsy**. If you’re also interested in typing or open source, feel free to reach out. I’m always happy to learn from others and collaborate.

Finally, a big thank you to everyone on the napari team who helped with this decision and the discussions around it. And a special thanks to **Tim** (@TimMonko), who spent a lot of time researching the decision-making points and also helped me throughout the writing of this blog ❤️.

I’m excited to see where this typing journey takes me next!

**Thank you for reading this — type-safe!**
