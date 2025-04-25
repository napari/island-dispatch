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

## List of PR with short summaries. 

### Napari:

* [#7162](https://github.com/napari/napari/pull/7162) – reduce number of highlight events in shapes layer by emitting only when selection changed
* [#7146](https://github.com/napari/napari/pull/7146) – calculate state of layer in separate thread
* [#7214](https://github.com/napari/napari/pull/7214) – use fan triangulation for convex shapes
* [#7228](https://github.com/napari/napari/pull/7228) – fix for bug introduced in [#7214](https://github.com/napari/napari/pull/7214)
* [#7256](https://github.com/napari/napari/pull/7256) – speed up checking if shape is convex 
* [#7144](https://github.com/napari/napari/pull/7144) – speed up of calculation which shape is under mouse in shapes layer
* [#7332](https://github.com/napari/napari/pull/7332) – fix for bug introduced in [#7144](https://github.com/napari/napari/pull/7144) by increase bounding box of shape for checking if shape is under mouse
* [#7386](https://github.com/napari/napari/pull/7386) – Reduce number of highlight events in shapes layer
* [#7268](https://github.com/napari/napari/pull/7268) - speedup of triangulation of edges in shapes layer. Using numba.
* [#7223](https://github.com/napari/napari/pull/7223) - fix performance issue of highlight shape in shapes layer
* [#7457](https://github.com/napari/napari/pull/7457) - fix for bug introduced in [#7223](https://github.com/napari/napari/pull/7223)
* [#7470](https://github.com/napari/napari/pull/7470) – refactor of the shapes layer to reduce changes in [#7346](https://github.com/napari/napari/pull/7346)
* [#7346](https://github.com/napari/napari/pull/7346) – Add c++ compiled backend for triangulation 
* [#7512](https://github.com/napari/napari/pull/7512) – fix for bug introduced in [#7346](https://github.com/napari/napari/pull/7346)
* [#7537](https://github.com/napari/napari/pull/7537) – fix for bug introduced in [#7346](https://github.com/napari/napari/pull/7346)
* [#7688](https://github.com/napari/napari/pull/7688) – fix of checking if shape is convex, when shape has self intersections
* [#7739](https://github.com/napari/napari/pull/7739) – improve benchmarking for shapes layer
* [#6654](https://github.com/napari/napari/pull/6654) - Fix multiple problems with rendering polygons with holes
* [#7747](https://github.com/napari/napari/pull/7747) - Add bermuda as backend for triangulation

### `PartSegCore-compiled-backend`:

I have used my package for testing if the speedup will be significant. 

* [#36](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/36) – Implement sweep line algorithm for triangulation in C++. Implement edge triangulation in C++.
* [#58](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/58) – Minor performance improvements in triangulation in C++.
* [#68](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/68) – Fix checking if shape is convex in C++ (self intersection case).


### `bermuda`:

After getting promising result we have decided to create a new package for compiled backend for napari.
Initial test shows that Rust version is slightly faster, and more memory safety.

* [#1](https://github.com/napari/bermuda/pull/1) – Implementation of edge triangulation in Rust in our new package for compiled backend
* [#3](https://github.com/napari/bermuda/pull/3) – Add support for optional arguments for `triangulate_path_edge`
* [#4](https://github.com/napari/bermuda/pull/4) - implement intersection detection utils in Rust
* [#6](https://github.com/napari/bermuda/pull/6) - Improve test setup for faster implementing
* [#10](https://github.com/napari/bermuda/pull/10) - Implement monotone polygon triangulation in Rust
* [#14](https://github.com/napari/bermuda/pull/14) - Deduplicate of edges for edge and face triangulation
* [#17](https://github.com/napari/bermuda/pull/17) - Sweeping line algorithm for triangulation in Rust, Python API for face and edge triangulation in one call
* [#27](https://github.com/napari/bermuda/pull/27) - Python API for face triangulation without edges
* [#30](https://github.com/napari/bermuda/pull/30) - Checking if polygon is convex 
* [#32](https://github.com/napari/bermuda/pull/32) - Add handling 3D data for face triangulation and polygon on single plane orthogonal to axis
* [#39](https://github.com/napari/bermuda/pull/39) - Remove consecutive repeated points in polygon
* [conda-forge#29805](https://github.com/conda-forge/staged-recipes/pull/29805) - Add Bermuda to conda-forge

## Retrospection 

When we start talking with SpatialData community about sponsoring 
work on speedup of Shapes layer the initial idea was to have single PR. 
But after fast review of work range we have decided that it will be 
much better to work on sequence of PRs. One of the benefits of this
approach wast that users will get some speedup since napari in version 0.5.2. 

Also total amount of changes was so big that it was hard to review. 

Current work contain improvements in three areas:

1. Speedup Checking layer state (move task to separate thread and speedup the code),
2. Speedup highlight of shape under mouse,
3. Speedup triangulation of edges and shapes,

Two first made usage of napari with loaded shapes layer much more pleasant.
The last one significantly speedup load of shapes layer.

When support from SpatialData allow to spend multiple days to understand the source 
of performance issues and fix them. However sometimes PRs stuck in review process.
One of the reasons is that only one core-dev is funded to work on this task. 

In this situation it not was a big problem, as there were multiple subtasks. 
Also, there was assumption, that if some problem was not spotted in review,
the author will fix it fast in next PR.

Such assumptions may be not correct if external contributor will work on the task.
In such situation project may require more time to review the PRs. 
Also hiring core-dev gives better knowledge retention in the project, 
that is important for core functionality of the project.

## Results

Based on benchmarks we have got speedup of loading shapes layer by 10-20 times.
Also the triangulation of shapes is around 215 times faster when using bermuda backend and 100 times faster when using PartSegCore backend.

```
| Change   | Before [5535c71a] <v0.5.1^0>   | After [2d27070a] <switch_bermuda>   |   Ratio | Benchmark (Parameter)                                                                 |
|----------|--------------------------------|-------------------------------------|---------|---------------------------------------------------------------------------------------|
| -        | 563±7ms                        | 354±7ms                             |    0.63 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('polygon', numba)       |
| -        | 30.2±0.6ms                     | 12.2±1ms                            |    0.41 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('polygon', triangle)    |
| -        | 19.1±0.5ms                     | 3.97±0.4ms                          |    0.21 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('path', triangle)       |
| -        | 18.4±0.5ms                     | 3.67±0.1ms                          |    0.2  | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('path', numba)          |
| -        | 18.8±0.9ms                     | 582±20μs                            |    0.03 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('path', partsegcore)    |
| -        | 19.0±0.6ms                     | 360±20μs                            |    0.02 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('path', bermuda)        |
| -        | 556±9ms                        | 5.47±0.4ms                          |    0.01 | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('polygon', partsegcore) |
| -        | 564±20ms                       | 2.60±0.1ms                          |    0    | benchmark_shapes_layer.MeshTriangulationSuite.time_set_meshes('polygon', bermuda)     |
```

And time of creation layer was reduced 20-30 times.

```
| Change   | Before [5535c71a] <v0.5.1^0>   | After [2d27070a] <switch_bermuda>   |   Ratio | Benchmark (Parameter)                                                                          |
|----------|--------------------------------|-------------------------------------|---------|------------------------------------------------------------------------------------------------|
| -        | 48.7±5ms                       | 26.9±0.8ms                          |    0.55 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'path', triangle)        |
| -        | 51.4±0.9ms                     | 26.7±2ms                            |    0.52 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'polygon', triangle)     |
| -        | 52.5±5ms                       | 26.9±0.5ms                          |    0.51 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'path', numba)           |
| -        | 50.3±3ms                       | 24.7±0.6ms                          |    0.49 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'path', bermuda)         |
| -        | 52.0±4ms                       | 24.7±0.6ms                          |    0.48 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'path', partsegcore)     |
| -        | 358±20ms                       | 172±3ms                             |    0.48 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'polygon', numba)        |
| -        | 1.27±0.02s                     | 541±10ms                            |    0.42 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'polygon', triangle)    |
| -        | 1.00±0.03s                     | 416±30ms                            |    0.41 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'path', numba)          |
| -        | 1.01±0.05s                     | 404±10ms                            |    0.4  | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'path', triangle)       |
| -        | 999±50ms                       | 326±20ms                            |    0.33 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'path', partsegcore)    |
| -        | 1.00±0.08s                     | 309±5ms                             |    0.31 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'path', bermuda)        |
| -        | 381±20ms                       | 21.7±0.4ms                          |    0.06 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'polygon', partsegcore)  |
| -        | 382±20ms                       | 19.6±0.9ms                          |    0.05 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(100, 'polygon', bermuda)      |
| -        | 10.6±0.06s                     | 395±10ms                            |    0.04 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'polygon', partsegcore) |
| -        | 10.6±0.07s                     | 336±8ms                             |    0.03 | benchmark_shapes_layer.ShapeTriangulationMixed.time_create_layer(3000, 'polygon', bermuda)     |
```

For convex shapes it is 10-100x faster depending on number of vertices in the shape.

```
| Change   | Before [5535c71a] <v0.5.1^0>   | After [45a7ca24] <main>   |   Ratio | Benchmark (Parameter)                                                                                 |
|----------|--------------------------------|---------------------------|---------|-------------------------------------------------------------------------------------------------------|
| -        | 206±8ms                        | 17.1±0.9ms                |    0.08 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 8, 'polygon', bermuda)    |
| -        | 647±60ms                       | 20.3±0.2ms                |    0.03 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 32, 'polygon', bermuda)   |
| -        | 2.76±0.4s                      | 36.2±2ms                  |    0.01 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 128, 'polygon', bermuda)  |
| -        | 2.17±0.02m                     | 1.06±0.04s                |    0.01 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(5000, 128, 'polygon', bermuda) |
```


Both values are get from benchmark of shapes layer.

For real data (the `xenium_2.0.0_io` from `spatialdata-sandbox`) the time to create Shapes layer drop from 224s (v0.5.1) to 17s (v0.6.0).
When run code under profiler the steep of mesh calculation drop from 255s to 2.4s.

The real data used for benchmarking contains much more shapes without intersections than our synthetic benchmark data. 
Also the majority of shapes in current data are below 20 vertices. 

These changes will allow to use much more complex shapes for better representing details in data.

Next to the speedup of creation of shapes layer we have also improved interactivity of the layer, and general improvements in the code.
That will allow to work on Shapes layer interactivity in the future.

## Conclusions 

When part of speedup is done by changing algorithm to more efficient one, 
the other require to use compiled language, as available algorithms cannot be vectorized, so cannot 
be implemented fast using numpy.

Also `numpy.unique(data, axis=x)` is not efficient. I situation when we know size of axis (2 or 3) 
using python `set` is much faster for now. 

### Numba 

As numba compiles code written in pure python,
then it is easier for napari core-devs to review the code.
So it reduce maintenance cost of the code. 
Sometimes numba code is more readable than pure python code, that is 
using some numpy functions.

However numba is JIT compiler that introduces some delay at first trigger in given session, even when use
cache between runs.

It shows tha try to implement sweeping line algorithm in numba was not successful because of compilation time.

### C++ and Cython 

For gluing C++ code with python we have used Cython. It provides 
Python like code for writing Python API for C++ code.

For example:

```cython
def is_convex(polygon: Sequence[Sequence[float]]) -> bool:
    """ Check if polygon is convex"""
    cdef vector[Point] polygon_vector
    cdef pair[bool, vector[int]] result

    polygon_vector.reserve(len(polygon))
    for point in polygon:
        polygon_vector.push_back(Point(point[0], point[1]))

    return _is_convex(polygon_vector)
```

However for creating numpy array it call numpy API, that introduced performance overhead.
Maybe the better solution could be use [pybind11](https://github.com/pybind/pybind11) 
that offer c++ API for creating numpy array.

The C++ code was much faster than numba one and allow to use Red - Black, that are required for triangulation of shapes. 

### Rust

During discussion with core-devs we found that we need to increase proficiency with 
any compiled language to have maintenance capacity. 

Based on successful stories from different projects we have decided to try Rust.
When try it on edge triangulation it shows that Rust version is slightly faster than C++ one having memory safety.
This change may be connected with mentioned above problem with array creation in Cython.
But even same performance with memory safety is a big win.
Especially when we meet memory problems in C++ code because of floating point errors. Current error 
is much more readable than segmentation fault.

For me, the debugging tools for rust are still slightly worse than C++ one.

## Future notes

* Start from writing benchmark, instead of custom scripts, it will speedup the process of writing code and testing it.
* It will be best to have a core-dev funded for reviewing PRs, as early review allow to save time. 
* Works with multiple PR is muche better than one big PR. It speedup the review process. But require better planning to avoid bottleneck.
* LLM are better and better in initial review of code. Not all its comments are correct, but it is good starting point. LLM works bad with huge PRs, so it is the next argument to work on smaller PRs.

