---
blogpost: true
date: Sep 22, 2026
author: Aniket Singh Yadav
location: World
category: Manual
language: English
---

# From `Any` to Certainty: A Typechecking Journey

In my first ever blog post, I'm going to walk you through not only my journey through open source, but how
I've ended up spending much of my time working on improving typing. In this journey, I've worked with the
napari team to replace our old type checker, mypy, with [Pyrefly](https://github.com/facebook/pyrefly). If you're trying to decide which type
checker might be the best choice for your project, I hope this blog helps.

## Where It Started

I ([@Aniketsy](https://github.com/Aniketsy)) started contributing to open source about a year ago, and I joined napari in April. More specifically, my [first](https://github.com/napari/napari/pull/8848) pull request was on April 2nd. I still remember Tim welcoming me on my first issue. I don’t know about others, but for me, that small gesture meant a lot ❤️. I can say it’s one of the reasons I felt so motivated to keep contributing and wanted to be part of such a welcoming and supportive community.

Typing wasn’t really part of the plan. I became interested in it while working on SciPy-stubs with **Joren** ([@jorenham](https://github.com/jorenham)). I still remember my late-night PRs, and Joren used to review them so quickly and merge them at light speed 😸. That’s where I started getting more interested in typing and decided to dive deeper into it.

*A special thanks to Joren — I learned so many things along the way ❤️.*

After that, I came back to napari and looked for typing issues. I found [one high-level tracker issue](https://github.com/napari/napari/issues/8120) that needed a long-term effort.

My steps were simple:
1. Pick a module from the list of files that mypy was skipping.
2. Run mypy on it and read every error.
3. Fix the real problems and add type hints where they were missing.
4. Repeat with the next module.

Doing this over and over is how I slowly learned what the errors actually mean.

Since our napari discussion, I have also started helping other projects move from mypy to Pyrefly. I opened a [discussion in nilearn](https://github.com/nilearn/nilearn/issues/6580), the maintainers agreed, and I have [opened a PR](https://github.com/nilearn/nilearn/pull/6584) there too. All the more open source love.

## Typing Across Scientific Python

My experience with typing has been a little different across napari and other Scientific Python projects.

In napari, I sometimes came across confusing annotations that weren’t properly typed. At times, the easiest way to fix them was to add something just to make mypy happy, even though it didn’t feel like the right solution.

I faced some similar issues while working on SciPy-stubs. Things like overlapping overloads and other mypy errors were confusing at first, but slowly I started to understand them. In some cases, we even had to disable mypy for an entire module. 😆

These experiences made me curious about better options. That’s when I came across newer type checkers like `ty` and `Pyrefly`. When I first tried `Pyrefly`, I was surprised by how much faster it was than `mypy`. After some time, I saw a [PR in SciPy](https://github.com/scipy/scipy/pull/25582) dropping `mypy` in favor of `Pyrefly`. That made me even more interested in this topic, and I wanted to open a thread for a similar decision in napari.

But unfortunately, I was already late. 😭 Lorenzo ([@brisvag](https://github.com/brisvag)) had already opened a [PR to migrate from mypy](https://github.com/napari/napari/pull/9375).

More recently, I've also started doing some typing work in NumPy and Matplotlib. It's been really interesting to see how different projects in the Scientific Python ecosystem handle typing. NumPy runs both mypy and pyrefly in CI, along with `stubtest` and a pyrefly coverage check that requires 100% of the public API to be typed. Matplotlib runs mypy and `stubtest`.

## Can an LLM Do a Type Checker Migration for You?

This came up while working on [napari#9375](https://github.com/napari/napari/pull/9375), where Lorenzo migrated the project from mypy to ty. So, can an LLM do the migration for you?

**Partly, yes.**

LLMs are pretty good at the repetitive part. If you have hundreds of similar errors across a codebase, they can help make bulk changes, add ignore comments, update suppressions, and take care of a lot of the boring work. That can save a lot of time. But here is the interesting part.

When a new type checker reports an error, someone still needs to understand **why**. Is there a real bug? Is the type checker missing something? Or does the code just need a better annotation? 

An LLM can make the error disappear by adding an `ignore` comment, but that doesn’t mean the problem is actually fixed. For me, the takeaway is simple:

> **LLMs can help with the boring part of a migration, but the important decisions still need you to understand and fix.**

## Choosing a New Type Checker

### Tim: How to Wrongly Implement a New Type Checker 😆

*(Just a joke — Tim actually did a great job!)*

After some [discussion](https://github.com/napari/napari/issues/9466), we decided to give Pyrefly a try. Tim took the [first shot](https://github.com/napari/napari/pull/9395) at migrating the codebase from mypy to Pyrefly, and that started a bigger discussion about which type checker we should use: **ty or Pyrefly**.

We spent some time comparing both options and looking at the results from our codebase. After a few discussions, we decided to go with **Pyrefly**.

## Pyrefly: Nice Features for Legacy Codebases and Speed

Adding a type checker to a new project is easier than migrating from an old one, where you may have hundreds of modules and type checking that may have been quietly ignored and turned off years ago.

That’s napari. And maybe that’s your project too. 😆

Both tools have good support for migrating existing codebases, but Pyrefly's particular workflow and commands worked better for us. It has some built-in commands that make the complex parts smoother, and I consider them strong practical arguments in the decision:

* **`pyrefly init`** — It reads your old configuration and helps initialize Pyrefly.

* **`pyrefly suppress`** — It can silence everything at once.

* **`pyrefly suppress --remove-unused=all`** — You can remove unused suppressions later. This is an important part because Pyrefly tells you when you don’t need an ignore comment anymore. After fixing real problems, the comments can be cleaned up automatically.

* **`pyrefly infer`** — It can write annotations for you.

* **`pyrefly coverage`** — It can measure progress. The `pyrefly coverage` report tells you how much of your code is actually typed. You can also use coverage checks in CI. For example, `pyrefly coverage check --fail-under 80` can fail CI if your typing coverage drops below 80%.

* **Existing `# type: ignore` comments** — Your old comments still work. Pyrefly respects `# type: ignore` by default, so existing mypy suppressions can continue to do their job; however, Pyrefly cannot self-prune bare ignores; it requires an error type like `# type: ignore[<error type>]`.

### A Tip: Delete Your Bare Ignores First

This was very useful during our migration. Because Pyrefly cannot check whether a bare `# type: ignore` is still needed, we recommend this order:

1. Grep for all bare `# type: ignore` comments and delete them.
2. Run `pyrefly check`.
3. Run `pyrefly suppress` to add back only the ignores that are really needed.
4. Run `pyrefly suppress --remove-unused=all` to clean up.

We dropped at least 30 stale ignores this way. If we hadn't done the grep-and-delete step, they would have stayed stale forever, because Pyrefly had no way to check them.

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

The Pyrefly and ty configurations are quite different. The ty configuration is about **450 lines** because of complexity with ignore types managed in the configuration rather than inline with the code. In comparison, napari's Pyrefly config is about **140 lines**, although it is mostly a long list of ignores that we hope to eventually be zero! I personally think Pyrefly is significantly better here, especially with its CLI commands.

**Error messages:**

Both checkers give clearer errors than mypy did. Between the two, ty is more verbose. Lorenzo compared them on the same failure, a function that declares one return type but returns another:

ty:

```text
error[invalid-return-type]: Return type does not match returned value
   --> src/napari/components/camera.py:248:16
    |
248 |         return up_direction_nd
    |                ^^^^^^^^^^^^^^^ expected `ndarray[tuple[int, int], dtype[Any]] | None`, found `_Array1D[float64]`
    |
   ::: src/napari/components/camera.py:229:10
    |
229 |     ) -> np.ndarray[tuple[int, int]] | None:
    |          ---------------------------------- Expected `ndarray[tuple[int, int], dtype[Any]] | None` because of return type
info: type `ndarray[tuple[int], dtype[float64]]` is not assignable to any element of the union `ndarray[tuple[int, int], dtype[Any]] | None`
info: ├─ a tuple of length 1 is not assignable to a tuple of length 2
info: └─ ... omitted 1 union element without additional context
```

pyrefly:

```text
ERROR Returned type `ndarray[tuple[int], dtype[float64]]` is not assignable to declared return type `ndarray[tuple[int, int]] | None` [bad-return]
   --> src/napari/components/camera.py:248:16
    |
248 |         return up_direction_nd
    |                ^^^^^^^^^^^^^^^
    |
   ::: src/napari/components/camera.py:229:10
    |
229 |     ) -> np.ndarray[tuple[int, int]] | None:
    |          ---------------------------------- declared return type
    |
 INFO 1 error (324 suppressed, 53 warnings not shown)
```

> Ty is more verbose, in a good way! I often get cross-eyed trying to figure out *what* is wrong with the types, when they get very messy. This is actually giving me a helpful hint that the issue is the tuple length.
>
> — [brisvag](https://github.com/brisvag), [napari/napari#9395 (comment)](https://github.com/napari/napari/pull/9395#issuecomment-5439762500)

And [Jacopo](https://github.com/jacopoabramo) helped us at every point by sharing opinion and thoughts.

### Other Details

There are some other differences that I don’t think affected our decision as much:

* **Conformance:** Both are above 90% conformance with the [typing specification](https://htmlpreview.github.io/?https://github.com/python/typing/blob/main/conformance/results/results.html), with Pyrefly being higher.

* **Maturity:** Pyrefly is 1.0+, while ty is not, and a stable API is nice to build on.

* **Pydantic support:** Pydantic is supported by both natively as of ty adding support in July 2026. Most information online is outdated on this.

* **Cross-platform consistency:** This one surprised our Linux developers. *The problem:* `mypy` and `ty` only check the code paths for the platform they run on. With our old setup, that meant Linux only. On any other platform, `sys.platform` checks like this one send the checker down a different branch:

  ```python
  if sys.platform == "win32":
    ...  # never checked by CI, always checked on Windows
  ```

  So a Windows developer sees errors CI never reports, and misses errors CI does report. That's a lot of noise to sort through before you can trust a green (or red) check.

  *The fix:* Pyrefly can check every platform in one run, with one line in [pyproject.toml](https://github.com/napari/napari/pull/9395/changes#diff-50c86b7ed8ac2cf95bd48334961bf0530cdc77b5a56f852c5c61b89d735fd711R657-R667).

  ```toml
  [tool.pyrefly]
  python-platform = "all"
  ```

  *How to run it:* use the tox environment. It matches CI exactly, on every platform:

  ```bash
  tox -e pyrefly
  ```

  `uv run pyrefly check` is faster for quick iteration, but its results can differ a little from CI for now, because the dev environment installs extra dependencies that tox's slimmer typecheck environment does not ([napari/docs#1134](https://github.com/napari/docs/pull/1134)). When in doubt, trust `tox -e pyrefly`.

* **Philosophy:** Pyrefly aggressively infers types in unannotated code, whereas ty does not report errors when you remove an annotation, so it is quieter.

* **Contributing upstream:** Both projects are active and easy to contribute to. While working on the migration I hit a bug in Pyrefly, and I recently fixed it [upstream](https://github.com/facebook/pyrefly/pull/4992). It was a nice feeling to give something back to the tool we now depend on.

## Resources

Here are some resources that can be helpful for a more in-depth analysis:

* [Typing Specification Conformance Results](https://htmlpreview.github.io/?https://github.com/python/typing/blob/main/conformance/results/results.html)
* [Python Type Checker Benchmark](https://python-type-checking.com/typecheck_benchmark/)

## Wrapping Up

It has been a really great experience getting into typing and working on it across different projects. I’ve learned a lot along the way, and I’m definitely going to keep working on it.

My next goal is to help make napari fully typed over the next few months, while continuing to contribute to other projects in the Scientific Python ecosystem. If you want to dive into the nitty-gritty details, you can find my work on GitHub: [@Aniketsy](https://github.com/Aniketsy). If you’re also interested in typing or open source, feel free to reach out. I’m always happy to learn from others and collaborate.

Finally, a big thank you to everyone on the napari team who helped with this decision and the discussions around it. And a special thanks to **Tim** ([@TimMonko](https://github.com/TimMonko)), who spent a lot of time researching the decision-making points and also helped me throughout the writing of this blog ❤️.

I’m excited to see where this typing journey takes me next!

**Thank you for reading this — type-safe!**
