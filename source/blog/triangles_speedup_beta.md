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

Thanks to SpatialData community, that decided to sponsor this work, we were able to implement faster algorithm for rendering triangles. 

Before this change we are using Constrained Delaunay Triangulation ([1](https://doi.org/10.1007/BF01553881),[2](https://www.cs.jhu.edu/~misha/Spring16/Chew87.pdf)) to render triangles from [vispy](https://vispy.org/).

This algorithm is iterative. As vispy implement it in Python, it is not as fast as it could be. 


Te have tested the new implementation on a few datasets, and we see significant speedup. For example, on `cell_boundaries` from `xenium2.0.0_io` that constains 162k polygons,
we observed that creation of the shapes layer drop from 3:52 (napari 0.4.19) to 0:20 on Ubuntu 20.04 with Intel Core i7-8700 CPU @ 3.20GHz.
Where most of the time was spent on triangulation, and now it takes around 2.5s.

We decided that we need to implement algorithm in compiled language. For create prototype we choose C++.
We have decided to implement sweeping line triangulation algorithm ([3](https://doi.org/10.1007/978-3-540-77974-2)).
This algorithm will allow us in future to implement support of holes in polygons.

The prototype is implemented in `PartSegCore-compiled-backend`, the package maintained by one of core developer of napari.
During testing we observed, that sometimes algorithm crash because of floating point precision. 
So we need to fix part of code choosing equivalent, but more floating point precision resistant solutions.

Current plan is to create `bermuda` package, that will contain compiled backend for napari shapes layer.
Based on some tests, the usage of rust may produce even faster code ([4](https://github.com/napari/bermuda/pull/1))


It may happen that we do not found all bugs and problems with floating point calculations, so we are looking for beta testers.
When we are working to make it stable, you could test if it works for you. If not we will be happy to get feedback from you. If you could provide us with dataset that cause problems, it will be even better, as we could add problematic cases to tests.


## How to test it

If napari 0.4.6 is not released yet, you can install it from source:

```bash
pip install git+https://github.com/napari/napari.git
pip install PartSegCore-compiled-backend
``` 
otherwise you can install it from pypi:

```bash
pip install napari PartSegCore-compiled-backend
```

Then open napari, then open File → Preferences → Experimental and enable "Use compiled backend to speedup create/update of Shapes layer"

![Experimental settings](images/speedup_triangulate_shapes.png)

If you spot any issues you may report them on [napari zulip](https://napari.zulipchat.com/), or create issue on [bermuda github](https:/github.com/bermuda/napari/issues).


Once we release the `bermuda` we will add proper installation instruction to this post.