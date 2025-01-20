---
blogpost: true
date: Jan 20, 2025
author: Grzegorz Bokota
location: World
category: news, help-wanted
language: English
---

# Triangles Speedup – call for beta testers

We are excited to announce that significant performance improvements are coming to napari Shapes layers.

Shapes layers in napari represent 2D geometric objects, — rectangles, circles,
polygons, paths… — possibly embedded in a higher-dimensional space, for
example, 2D polygons of cell outlines within a 3D image stack.
[Vispy](https://vispy.org), which powers napari's graphics, uses OpenGL to draw
on the screen. The fundamental unit of OpenGL graphics is *triangles*, which
can be put together to draw more complex shapes such as polygons. This means
that we have a preproprocessing step in napari to break down input shapes into
triangles. This step is called *triangulation*.

Until now, we have been using an algorithm called Constrained Delaunay
Triangulation
([1](https://doi.org/10.1007/BF01553881),[2](https://www.cs.jhu.edu/~misha/Spring16/Chew87.pdf)),
implemented in pure Python in Vispy. This has been a performance bottleneck
when creating Shapes layers with thousands to hundreds of thousands of shapes.
(An optional dependency [`triangle`](http://www.cs.cmu.edu/~quake/triangle.html)
can be used to speed things up, but because it uses a proprietary license, we
cannot ship it by default and we cannot use it in the napari bundled app.)

Thanks to the [SpatialData](https://spatialdata.scverse.org/) community, which
decided to sponsor this work, we were able to implement a faster algorithm for
rendering triangles used for rendering geometries in a napari shapes layer.
(`SpatialData` is a framework for the representation of spatial multimodal
data and part of the single-cell omics analysis suite
[scverse](https://scverse.org/).)

We have tested the new implementation on a few example datasets of SpatialData,
and we see a significant speedup. For example, in this [Xenium Human Lung
Cancer dataset from 10x
Genomics](https://www.10xgenomics.com/datasets/preview-data-ffpe-human-lung-cancer-with-xenium-multimodal-cell-segmentation-1-standard)
(available in the SpatialData Zarr format using [these
scripts](https://github.com/giovp/spatialdata-sandbox/tree/main/xenium_2.0.0_io)),
the cell boundaries are stored as 162,000 polygons. When visualizing these
polygons in napari, creation of the shapes layer drops from almost 4 minutes
(napari 0.4.19) to just 20 seconds! (Ubuntu 20.04 with Intel Core i7-8700 CPU @
3.20GHz)
Most of the time creating a Shapes layer with so many shapes was spent on
triangulation, which takes just 2.5s with our changes.

We obtain this dramatic speedup through a combination of algorithmic changes
(using the sweeping line triangulation algorithm from
[3](https://doi.org/10.1007/978-3-540-77974-2)) and code changes —
implementing the algorithm in C++ instead of pure Python.

For now, our fast triangulation is implemented in
`PartSegCore-compiled-backend`, a compiled Python package I was already
distributing for [PartSeg](https://partseg.github.io), which is the main
software output of my PhD and the work that brought me to napari and eventually
the napari core team.
In the near future we plan to create the `bermuda` package (yes, because of the
Bermuda triangle — and with thanks to [Aperio's](https://aperiosoftware.com)
Thomas Robitaille a.k.a. astrofrog for the PyPI package name!), which will
contain fast spatial algorithms for the napari Shapes layer and beyond.
We plan to develop in Rust which [seems to give us even faster
performance](https://github.com/napari/bermuda/pull/1) on top of better memory
safety guarantees. Plus all those shipwrecks are probably pretty rusty!

To help make it stable, you could test if it works for you. If not, we would be happy to get your feedback by reporting any problems in a [github issue](https://github.com/napari/napari/issues) or at a [napari community meeting](https://napari.org/dev/community/meeting_schedule.html). If you could provide us with a dataset that causes problems, it will be even better, as it allows us to add problematic cases to tests.


## How to test it

This feature requires napari in version at least 0.5.6. At moment of publishing this announcement, the first pre-release of napari 0.5.6 is available on PyPI. 

If napari 0.5.6 is not released yet, you can install the pre-release using `pip`:

```bash
pip install --pre napari[optional,pyqt6]
pip install PartSegCore-compiled-backend
``` 
otherwise you can install it from pypi:

```bash
pip install napari[optional,pyqt6] PartSegCore-compiled-backend
```


Then open napari, and open the menu File → Preferences → Experimental and enable "Use compiled backend to speedup create/update of Shapes layer".
(You don't need to restart napari, just create a new Shapes layer after toggling the setting.)
![Experimental settings](images/speedup_triangulate_shapes.png)

You can also toggle it using the `COMPILED_TRIANGULATION` environment variable, for example activating it and launching `napari` using `COMPILED_TRIANGULATION=1 napari`.
If you spot any issues you may report them on [napari zulip](https://napari.zulipchat.com/), or create issue on [bermuda github](https:/github.com/bermuda/napari/issues).


Once we release the `bermuda` we will add proper installation instruction to this post.

## Editing layer

Ths job not (yet) improve code responsible for slownes of editing Shapes layer with a huge number of polygons.

## Acknoledgments

In addition to the SpatialData development team, we would like to express our gratitude to the Chan Zuckerberg Initiative for their generous support, as their funding enabled the SpatialData team to support the work presented here. We also acknowledge the [scverse team](https://scverse.org/), a consortium of open-source developers dedicated to single-cell omics.
