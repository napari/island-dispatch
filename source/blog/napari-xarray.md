---
blogpost: true
date: Sep 19, 2025
author: Ian Hunt-Isaak, Tim Monko
location: World
category: news, help-wanted
language: English
---

# Seamless Xarray Integration with napari - Plan from SciPy 2025

```{note}
This post is cross-posted on the [Xarray blog](https://xarray.dev/blog).
```

## What and Why

[napari](https://napari.org/stable/) is a high-performance, GPU-backed multidimensional array viewer with support for physical coordinates, data annotation, 2 and 3D visualization, and a plugin infrastructure, allowing users to customize it to their needs.

```{raw} html
<div style="text-align: center;">
  <video width="100%" controls autoplay muted loop
         aria-label="Video of napari in action showing multidimensional image visualization"
         title="napari GUI demonstration - Biological data">
    <source src="https://napari.org/stable/_static/images/tribolium.webm" type="video/webm">
    <p>Video of napari in action showing multidimensional image visualization with GPU-backed rendering and physical coordinate support. Your browser does not support the video tag.</p>
  </video>
</div>
```

However, there are still several key pain points around managing image metadata when using napari.

- Most users think in physical units (microns, lat/lon) rather than pixels
- Re-indexing dimensions (e.g. Fiji’s Stack to HyperStack) is difficult with unnamed dimensions  
- Dimensionality reductions can lead to incorrect dimension mappings in the viewer due to dropping of singleton dimensions.
  - For example, a max projected image stack will no longer respond to the correct sliders as the base image (`TCZYX` vs `TCYX`)
- Users expect that provided dimension names will be matched to viewer dimension names, but napari right-aligns axes, so if you add an image with axes `TYX` to a viewer with a `TCZYX` image, then the axes of the `TYX` image will be aligned with the 3 right-most axes, so `ZYX`, in the viewer.

```{raw} html
<div style="text-align: center; margin: 20px 0;">
  <iframe width="100%" style="max-width: 800px; aspect-ratio: 16/9;" src="https://www.youtube.com/embed/b3j4GkYKkW8" title="Napari Misaligned arrays" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
</div>
```

[Xarray](https://xarray.dev/) is a powerful multidimensional array library with deep support for labelled axes and managing metadata. If napari could utilize Xarray objects' metadata, then this integration would provide a solution to all of these pain points.

To get a sense of the benefits Xarray provides, read the [Accelerating Biological Analysis with Xarray](https://xarray.dev/blog/xarray-biology) blog post and look at the rich repr of an `Xarray.DataArray` for an image stack:

```{raw} html
<div style="text-align: center; margin: 20px 0;">
  <iframe src="../_static/xarray-dataarray-repr.html" width="100%" height="600" frameborder="0" style="border: 1px solid #ccc; border-radius: 5px;"></iframe>
</div>
```

Having napari leverage the Xarray metadata will not only improve the experience of napari users but also provide Xarray users with a polished interactive visualization tool.

```{raw} html
<div style="text-align: center;">
  <video width="100%" controls autoplay muted loop
         aria-label="Video of napari displaying geographic data with coordinate systems"
         title="napari GUI demonstration - Geographic data">
    <source src="../_static/geo-in-napari.mov" type="video/mp4">
    <p>Video of napari displaying geographic data with proper coordinate system handling. Your browser does not support the video tag.</p>
  </video>
</div>
```

This potential for napari and Xarray to bring out the best in each other is not a new insight.
In fact, the second oldest open issue on napari [`#14`](https://github.com/napari/napari/issues/14) is titled “Pass xarray to napari-gui for autolabeling sliders.”
That issue's age is a testament to the difficulty of the problems involved in this integration.

But something being hard is not a reason not to try to do it.
Indeed, some of the most successful plugins for napari are [napari-aicsimageio](https://github.com/AllenCellModeling/napari-aicsimageio) which is built on top of [aicsimageio](https://github.com/AllenCellModeling/aicsimageio) and its successor [bioio](https://bioio-devs.github.io/bioio/OVERVIEW.html), which use xarray to manage their data and metadata.

Yet, both napari and Xarray have recently implemented important changes that make this problem easier to solve.
With this in mind both a group of napari and Xarray developers are committed to improving the integration of napari and Xarray.

## How

### SciPy 2025

Thanks to support from the Chan Zuckerberg Institute the napari, Xarray, and [CellProfiler](https://cellprofiler.org/) team members were able to attend SciPy 2025. At the sprints members of these three teams—Ian Hunt-Isaak, Tim Monko, Nodar Gogoberidze, Beth Cimini, Peter Sobolewski and Carol Willing—collaborated to develop a plan for enhancing the integration of Xarray with napari. The rest of this blog post is the initial roadmap we came up with for better integration of Xarray and napari.

### Get Involved

This is a community effort, so your contributions and thoughts are very welcome! To get involved in shaping this vision of the future, please join the napari [Zulip](https://napari.zulipchat.com/) and introduce yourself on this [introductions issue](https://github.com/napari/napari-xarray/issues/8) in the napari Xarray repository.

### **🗺️ Roadmap**

To fully realize the potential of an integration between Xarray and napari, some deep changes in napari may be required. Therefore, we have developed a phased plan that progresses from simple to more complex enhancements, culminating in solutions that require more fundamental changes to how napari handles data.

#### 1: Basic Metadata Mapping (Proof of Concept)

This first step is the easiest, as it requires no changes to napari's core and can be implemented in a simple script or plugin.

**Goal:** Ingest Xarray data into napari's layer metadata to provide immediate context to the user.

**Key Functionality:**

- Auto-label sliders with Xarray dimension names (e.g., `'Z'`, `'Time'`)
- Assign layer names from Xarray's `.name` attribute
- Automatically transform:
  - [`DataArray`](https://docs.xarray.dev/en/latest/user-guide/data-structures.html#dataarray) -> Layer
  - [`Dataset`](https://docs.xarray.dev/en/latest/user-guide/data-structures.html#dataset) -> Multiple Layers
  - [`DataTree`](https://docs.xarray.dev/en/latest/user-guide/data-structures.html#datatree) -> Multiple Layers + Pyramidal Viewing (if applicable)

**Implementation:** Script or plugin level, no napari core changes required.

#### 2: Meaningful Physical Units (Enhancement)

The next step is to map array indices to Xarray coordinates. This is harder than the previous step as it involves napari's viewer dims model, which is more complex than the layer metadata.

**Goal:** Display physical values instead of array indices in napari sliders and use coordinate information for proper scaling.

**Key Functionality:**

- Show slider values as physical units (e.g., `20.5` microns) using Xarray [Coordinates](https://docs.xarray.dev/en/latest/user-guide/data-structures.html#coordinates)
- Use Xarray coordinates to map pixel sizes for accurate scale bars

**Implementation:** First at script/plugin level, with eventual integration into napari core.

#### 3: "Magic" Reordering (Complex)

Today, if you mix up the order of your axes in non-standard way (e.g. `lat, time, lon`, or `XCZSYT`) and pass it to napari it will display as is, from right to left. Thisis because napari treats all axes equally, and does not know about or distinguish spatial or temporal dimensions! With knowledge of metadata and the conventions of a field napari could magically re-order the array to display in the "correct" order, with spatial dimensionss on the right. This is a significant jump in complexity due to the "magic" involved - the system will need to correctly guess user intent, which can be challenging.

**Goal:** Handle a few clear cases of problematic dimension ordering, not solve the general case of arbitrary reordering.

**Key Functionality:**

- Focus on well-defined, common problematic orderings with clear solutions
- Recognize specific patterns
  - `lat, time, lon` -> `time, lat, lon`
  - `XTCZYS` -> `STCZYX`
- Start with a small set of clear examples rather than attempting to solve all possible cases
- Persist user-defined dimension mappings and schemas across sessions

**Implementation:** Plugin with access to napari internals, requires deep integration with viewer logic.

#### 4: User Personas (Plugin System)

The "magic" reordering naturally leads to issues where different fields of science have different conventions for what the "right" thing to do is. napari can't possibly know every convention across different scientific domains. napari now supports a [startup script](https://github.com/napari/napari/pull/8188) which can serve as an initial hook for this functionality.

**Goal:** Enable domain-specific configuration through pluggable personas with well-defined schemas for converting Xarray data into how napari should interpret it.

**Key Functionality:**

- Define pluggable persona system with well-established schemas (e.g., Microscopy, Geospatial, Astronomy)
- Each persona provides rules for dimension ordering, naming conventions, and visualization defaults
- For example, a Microscopy persona would define different defaults than a Geospatial persona
- Allow users to create and share custom personas for their specific domains
- Persistent user preferences and persona selection across sessions

**Implementation:** Plugin mechanism and API provided by napari for extensible persona definitions.

#### 5: Big Lift: New Dims Model (Major Architecture Change)

Taking the lessons and user feedback from the earlier steps into account, we work to update napari's internal data model to be name-aware in addition to its current index-aware state. This is a major architectural change that addresses long-standing issues.

**Goal:** Transform napari's core to natively understand and preserve named dimensions throughout all operations.

**Key Functionality:**

- Preserve named dimensions and their relationships through transformations like slicing or max projections
- Unify layer dimensions and viewer dimensions under a name-aware system
- Replace fragile index-based state (0, 1, 2...) with persistent named dimensions ('time', 'channel', 'z')
- Ensure viewer state persists correctly when layers are added or removed
- Make napari viewer respect and preserve Xarray's descriptive dimension model

**Implementation:** Deep changes to napari core architecture - significant development effort required. This addresses years-old open issues and fundamental limitations.
