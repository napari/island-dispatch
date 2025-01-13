---
blogpost: true
date: Jun 18, 2025
author: Grzegorz Bokota
category: Advertisement
language: English
---

# Summary of speedup of Shapes layer

With a big pleasure to SpatialData community whose decided to sponsor this work in last half year one of Core-Developer of napari, Grzegorz Bokota, has been working on speedup of Shapes layer. The work has been done in the context of the napari project, and the results are already available in the latest release of napari.

This post is a summary and retrospection of this work.

## List of PR and changes. 

### Napari:

* [#7162](https://github.com/napari/napari/pull/7162) – reduce number of highlight events in shapes layer by emitting only when selection changed
* [#7146](https://github.com/napari/napari/pull/7146) – calculate state of layer in separate thread
* [#7214](https://github.com/napari/napari/pull/7214) – use fan triangulation for convex shapes
* [#7228](https://github.com/napari/napari/pull/7228) – fix for bug introduced in [#7214](https://github.com/napari/napari/pull/7214)
* [#7256](https://github.com/napari/napari/pull/7256) – speed up checking if shape is convex 
* [#7144](https://github.com/napari/napari/pull/7144) – speed up of calculation which shape is under mouse in shapes layer
* [#7332](https://github.com/napari/napari/pull/7332) þ fix for bug introduced in [#7144](https://github.com/napari/napari/pull/7144) by increase bounding box of shape for checking if shape is under mouse
* [#7386](https://github.com/napari/napari/pull/7386) – Reduce number of highlight events in shapes layer
* [#7268](https://github.com/napari/napari/pull/7268) - speedup of triangulation of edges in shapes layer. Using numba.
* [#7223](https://github.com/napari/napari/pull/7223) - fix performance issue of highlight shape in shapes layer
* [#7457](https://github.com/napari/napari/pull/7457) - fix for bug introduced in [#7223](https://github.com/napari/napari/pull/7223)
* [#7470](https://github.com/napari/napari/pull/7470) – refactor of the shapes layer to reduce changes in [#7346](https://github.com/napari/napari/pull/7346)
* [#7346](https://github.com/napari/napari/pull/7346) – Add c++ compiled backend for triangulation 
* [#7512](https://github.com/napari/napari/pull/7512) – fix for bug introduced in [#7346](https://github.com/napari/napari/pull/7346)


### `PartSegCore-compiled-backend`:

I have used my package for testing if the speedup will be significant. 

* [#36](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/36) – Implement sweep line algorithm for triangulation in C++. Implement edge triangulation in C++.
* [#58](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/58) – Minor performance improvements in triangulation in C++.


### `bermuda`:

After getting promising result we have decided to create a new package for compiled backend for napari.

* [#1](https://github.com/napari/bermuda/pull/1) – Implementation of edge triangulation in Rust in our new package for compiled backend
