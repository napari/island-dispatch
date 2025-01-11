---
blogpost: true
date: December 22, 2024
author: Grzegorz Bokota
location: World
category: Advertisement
language: English
---

# Triangles Speedup – call for beta testers

We are excited to announce that significant performance improvements are coming to napari shapes layers. 

Thanks to the [SpatialData](https://spatialdata.scverse.org/) community, which decided to sponsor this work, we were able to implement a faster algorithm for rendering triangles used for rendering geometries in a napari shapes layer.

Before this change we were using Constrained Delaunay Triangulation ([1](https://doi.org/10.1007/BF01553881),[2](https://www.cs.jhu.edu/~misha/Spring16/Chew87.pdf)) to render triangles from [vispy](https://vispy.org/).

This algorithm is iterative. As vispy is implemented in Python, it is not as fast as it could be. 


We have tested the new implementation on a few example datasets of SpatialData, and we see a significant speedup. For example, for `cell_boundaries` from `xenium2.0.0_io` which contains 162k polygons,
we observed that creation of the shapes layer drops from 3:52 (napari 0.4.19) to 0:20 on Ubuntu 20.04 with Intel Core i7-8700 CPU @ 3.20GHz.
Most of the time of creating the shapes layer was spent on triangulation, which takes 2.5s with the latest changes.

The speedup was achieved by implementing the sweeping line triangulation algorithm ([3](https://doi.org/10.1007/978-3-540-77974-2)) in a compiled language. For the initial prototype we choose C++. The algorithm will allow us in future to implement support of holes in polygons.

The prototype is implemented in `PartSegCore-compiled-backend`, a package maintained by Grzegorz Bokota, a core developer of napari.
During testing we observed, that sometimes the algorithm crashes because of [floating point precision](https://learn.microsoft.com/en-us/cpp/build/why-floating-point-numbers-may-lose-precision?view=msvc-170). 
In order to address this we require equivalent, but more floating point precision resistant solutions.

In the future we plan to create the `bermuda` package (yes, because of the Bermuda triangle), that will contain the compiled backend for napari shapes layer.
Some testing showed that the usage of rust may produce even faster code ([4](https://github.com/napari/bermuda/pull/1))


It may happen that we did not find all bugs and problems with floating point calculations, so we are looking for beta testers.
To help make it stable, you could test if it works for you. If not, we would be happy to get your feedback by reporting any problems in a [github issue](https://github.com/napari/napari/issues) or at a [napari community meeting](https://napari.org/dev/community/meeting_schedule.html). If you could provide us with a dataset that causes problems, it will be even better, as it allows us to add problematic cases to tests.


## How to test it

This feature requires napari in version at least 0.4.6. At moment of publishin this annoucement the firt pre-release of napri is avialable. 

If napari 0.4.6 is not released yet, you can install pre-release:

```bash
pip install --pre napari
pip install PartSegCore-compiled-backend
``` 
otherwise you can install it from pypi:

```bash
pip install napari PartSegCore-compiled-backend
```


Then open napari, and open the menu File → Preferences → Experimental and enable "Use compiled backend to speedup create/update of Shapes layer"
(You don't need to restart napari, just create a new Shapes layer after toggling the setting.)
![Experimental settings](images/speedup_triangulate_shapes.png)

You can also toggle it using the `COMPILED_TRIANGULATION` environment variable, for example activating it and launching `napari` using `COMPILED_TRIANGULATION=1 napari`.
If you spot any issues you may report them on [napari zulip](https://napari.zulipchat.com/), or create issue on [bermuda github](https:/github.com/bermuda/napari/issues).


Once we release the `bermuda` we will add proper installation instruction to this post.