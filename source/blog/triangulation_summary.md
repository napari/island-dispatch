---
blogpost: true
date: Jun 18, 2025
author: Grzegorz Bokota
category: Advertisement
language: English
---

# Summary of speedup of Shapes layer

With a big thank you to the SpatialData team, who decided to sponsor this work over the past last half year, Grzegorz Bokota, one of the Core-Developers of napari, has been working on speedup of the Shapes layer. The work has been done in the context of the napari project, and the results are already available in the latest release of napari.

This post is a summary and retrospection of this work.

## List of PR with short summaries. 

### Project pull requests in Napari:

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

`PartSegCore-compiled-backend`, developed by Grzegorz Bokota, was initially used for testing if the speedup of the Shapes layer was significant. 

* [#36](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/36) – Implement sweep line algorithm for triangulation in C++. Implement edge triangulation in C++.
* [#58](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/58) – Minor performance improvements in triangulation in C++.
* [#68](https://github.com/4DNucleome/PartSegCore-compiled-backend/pull/68) – Fix checking if shape is convex in C++ (self intersection case).


### `bermuda`:

After getting promising results using `PartSegCore-compiled-backend`, core developers decided to create a new package for a compiled backend in napari to speed up the Shapes layer.
Initial test showed that the Rust version is slightly faster, and adds more memory safety.

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

When I started talking with the SpatialData team about sponsoring of
work on speedup the Shapes layer, the initial idea was to have a single PR. 
However, after a fast estimation of work required, we agree that it would be 
much better to work on a sequence of PRs. One of the benefits of this
approach was that napari users already could make use of some speedup since napari version 0.5.2. 

It also made the total amount of changes easier to review as the work was spread over multiple relatively small pull requests. 

The work contains improvements in three areas:

1. Speedup Checking layer state (move task to separate thread and speedup the code),
2. Speedup highlight of shape under mouse,
3. Speedup triangulation of edges and shapes,

The first two points made usage of napari with a loaded shapes layer much more pleasant.
The last point significantly speeds up the loading of shapes layer.

The financial support of SpatialData allowed me to spend multiple days to understand the source 
of performance issues and fix them. However, sometimes PRs were stuck in the review process.
One of the reasons is that only one core-dev is funded to work on this task. 

For this project, it was not a big problem, as there were multiple subtasks. 
Also, the assumption was that if some problem was not spotted in review,
I, as a core developer, could fix it fast in followup PR. 

These assumptions may be not correct if an external contributor will work on the task.
In such situations, a project may require more time to review the PRs. Hence, direct financial support 
of a napari core developer was crucial for this project.
Furthermore, hiring a core-dev gives better knowledge retention in the project, 
that is important for sustainability of the napari project.

## Results

Based on benchmarks, we achieved a 10–20× speedup in loading the Shapes layer.
Also, the triangulation of shapes is around 215 times faster when using `bermuda` backend and 100 times faster when using `PartSegCore` backend.

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

The time of creation of a Shapes layer was reduced 20-30x.

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

For convex shapes, it is 10-100x faster depending on the number of vertices in the shape.

```
| Change   | Before [5535c71a] <v0.5.1^0>   | After [45a7ca24] <main>   |   Ratio | Benchmark (Parameter)                                                                                 |
|----------|--------------------------------|---------------------------|---------|-------------------------------------------------------------------------------------------------------|
| -        | 206±8ms                        | 17.1±0.9ms                |    0.08 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 8, 'polygon', bermuda)    |
| -        | 647±60ms                       | 20.3±0.2ms                |    0.03 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 32, 'polygon', bermuda)   |
| -        | 2.76±0.4s                      | 36.2±2ms                  |    0.01 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(100, 128, 'polygon', bermuda)  |
| -        | 2.17±0.02m                     | 1.06±0.04s                |    0.01 | benchmark_shapes_layer.ShapeTriangulationConvexSuite.time_create_layer(5000, 128, 'polygon', bermuda) |
```


These values were generated by a benchmark of the napari Shapes layer.

For real data (the `xenium_2.0.0_io` from `spatialdata-sandbox`, test data used within the SpatialData project), the time to create the Shapes layer dropped from 224s (v0.5.1) to 17s (v0.6.0).
When running the code under a profiler, the step of mesh calculation dropped from 255s to 2.4s.

The real data used for benchmarking contains much more shapes without intersections than our synthetic benchmark data. The majority of shapes in our current test data contain less than 20 vertices. 

These changes will allow napari users to use much more complex shapes for better representing details in data.

Besides the speedup of the creation of the shapes layer we have also improved the interactivity of the layer, and general improvements in the code.
This will allow further work on Shapes layer interactivity in the future.

## Interesting findings 

While part of the speedup was initially done by changing the use of more efficient algorithms, 
the full speedup cannot be achieved without using compiled language. This because available algorithms cannot be vectorized, and thus not be implemented in fast vectorized fashion in numpy.

Also, `numpy.unique(data, axis=x)` is [not efficient](https://github.com/numpy/numpy/issues/11136). In a situation where we know the number of dimensions (2 or 3) 
using python `set` is much faster. 

### Considerations for using numba 

As numba compiles code written in pure python,
it is easier for napari core-devs to review the code.
With that, it reduces maintenance cost of the code. 
Sometimes numba code is more readable than pure python code using some numpy 
functions.

However, the downside is that numba is a JIT compiler that introduces some delay at first trigger in a given session, even when using a cache between runs.

Because of that, trying to implement the sweeping line algorithm using numba was not successful.

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

However, for creating a numpy array it calls the numpy API, which introduces a performance overhead.
The better solution could be to use [pybind11](https://github.com/pybind/pybind11), which offers a c++ API for creating a numpy array.

The C++ code turned out to be much faster than the numba-version and made it possible to use a Red-Black tree, a binary search tree. Red-Black trees are essential for efficiently managing edges during the triangulation of shapes. They help quickly inserting, deleting and finding edges when breaking down complex shapes into simpler triangles.

### Rust

During discussion with core-developers, we found that we had to increase our proficiency with 
any compiled language to have maintenance capacity. 

Based on successful stories from different projects we decided to try Rust.
When trying it on edge triangulation, the Rust version was slightly faster than the C++ implementation and adds memory safety.
This result may be connected with the problem mentioned earlier with array creation in Cython.
However, even same performance with memory safety is a big win.
Also, because when we meet memory problems in C++ code because of floating point errors, we get a cryptic segmentation fault that is hard to trace. The error in Rust is much more readable than this.

For me, the debugging tools for rust are still slightly worse than C++ one.

## Lessons learned

* Start with writing a benchmark, instead of custom scripts, it will speed up the process of writing code and testing it.
* It will be best to have a core-dev funded for reviewing PRs, as early review allows saving time. 
* Working with multiple PRs is much better than one big PR. It speeds up the review process. However, it requires better planning to avoid bottlenecks.
* LLMs are better and better in initial review of code. Not all its comments are correct, but it is a good starting point. LLM works bad with huge PRs, so it is an additional argument to work with smaller PRs.

