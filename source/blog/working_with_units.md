---
blogpost: true
date: Feb 26, 2026
author: Grzegorz Bokota
location: World
category: tutorials
language: English
---

# How to read/write units and other spatial information using TIFF files

## Motivation 

In `napari` 0.7.0 we've started using information about units to render data more accurately. 
In `napari-tiff` 0.1.6 we enhanced readers and added writers to work with units in TIFF files.  

However, we know that not all data processing will be done through napari, and it is common to create custom scripts/notebooks. 
This blog post therefore explains how to read and write this metadata for TIFF files. Once we decide formats for Layers other than Image and Labels, we will post similar guides.

## Assumptions 

We'll use Python for all the code in this guide, and the [`tifffile`](https://pypi.org/project/tifffile/) library for file processing. The information about parsing/creating OME metadata might be useful for other file formats. For a higher level interface you might want to look at the [`bioio`](https://github.com/bioio-devs/bioio) library.

## Reading/Writing data from tiff files 

The `tifffile` library provides a low level of abstraction over the internal TIFF structure. 
So, while it allows for better control, it might require familiarity about different ways of doing things.

### Reading 

Reading only the image data from TIFF files is simple:

```python
import tifffile

data = tifffile.imread("path_to_file.tiff")
```

This will return a NumPy array with data in the same axis order as in the file.

To also read metadata, we need to use the `tifffile.TiffFile` class. It will give us access to metadata stored in TIFF file, such as scale, transforms and units.

```python
import tifffile

with tifffile.TiffFile("path_to_file.tiff") as tif:
    data = tif.asarray()
    # here we can access all tags and their value
```

To get information about axis order we could use information stored in the first series of the TIFF file. It is stored in `axes` property. Accessing this property will return a string with axis labels in the same order as data. For example, `TZCYX` means the first axis is Time, second is Z, third is Channel, fourth is Y and fifth is X.

```python
import tifffile

with tifffile.TiffFile("path_to_file.tiff") as tif:
    data = tif.asarray()
    series = tif.series[0]
    axes = series.axes
```

### Writing

Writing just data to TIFF files is also simple:

```python
import tifffile

tifffile.imwrite("path_to_file.tiff", data)
```

The `imwrite` function has parameter `compression` that allows specifying a compression method. 
For many types of data, using compression allows us to significantly reduce the image file size on disk. In `napari-tiff`, we use `ADOBE_DEFLATE` compression, but there are many others available. However, not all software can read all compression methods, so it is good to check if your software can read files compressed with a given method before using it.

This function can also accept metadata -- this is described later.

## OME-TIFF 

OME-TIFF is a modern standard for storing data and its metadata in a TIFF container. Its detailed description can be found [here](https://docs.openmicroscopy.org/ome-model/5.6.3/ome-tiff/)

### Reading OME-TIFF

The `TiffFile` class has a property `is_ome` that allows checking if the file is OME-TIFF. If it is, we can access OME metadata through the `ome_metadata` property. It will return [xml](https://en.wikipedia.org/wiki/XML) with all metadata stored in OME format.
To parse this xml into a Python `dict`, we can use the `tifffile.xml2dict` function.

The units and scale information are stored in the `Pixels` element of the `Image` element. The metadata could contain multiple `Image` elements, but usually there is only one. 
 The `Pixels` element has attributes `PhysicalSizeX`, `PhysicalSizeY`, `PhysicalSizeZ`  
 and `TimeIncrement` that store the scale for each axis. The units are stored in `PhysicalSizeXUnit`, `PhysicalSizeYUnit`, `PhysicalSizeZUnit` and `TimeIncrementUnit` attributes.

Here is some example code reading this information:

```python
import tifffile
from typing import Any


def ensure_list(x: Any) -> list[Any]:
    """Ensure that x is a list or tuple. If it is not, convert it to a list."""
    if not isinstance(x, (list, tuple)):
        x = [x]
    return x

def get_scale_and_units_from_ome(pixels: dict[str, Any], axes: str) -> tuple[list[float], list[str]]:
    pixel_size = []
    units = []

    for i, ax in enumerate(axes):
        if ax == "C":
            continue
        if ax == 'C':
            time_increment = float(pixels.get("TimeIncrement", 1.0))
            time_unit = pixels.get("TimeIncrementUnit", "pixel")
            pixel_size.append(time_increment)
            units.append(time_unit)
        else:
            physical_size = float(pixels.get(f"PhysicalSize{ax}", 1.0))
            spatial_unit = pixels.get(f"PhysicalSize{ax}Unit", "pixel")
            pixel_size.append(physical_size)
            units.append(spatial_unit)
    return pixel_size, units


with tifffile.TiffFile("path_to_file.tiff") as tif:
    if tif.is_ome:
        data = tif.asarray()
        ome_metadata = tifffile.xml2dict(tif.ome_metadata)["OME"]
        axes = tif.series[0].axes.upper()

        image_metadata = ensure_list(ome_metadata.get("Image", {}))[0]
        pixels = image_metadata.get("Pixels", {})

        scale, units = get_scale_and_units_from_ome(pixels, axes)
        print(f"Data shape {data.shape}, Axes order {axes}, Scale: {scale}, Units: {units}")
```

### Writing OME-TIFF

To write OME-TIFF we can use the `tifffile.imwrite` function. It has a parameter, `metadata`, that allows us to pass metadata. Here is an example `dict` that could be passed to the `metadata` parameter:

```python
pixels = {
    "PhysicalSizeX": scale_for_x_axis,
    "PhysicalSizeY": scale_for_y_axis,
    "PhysicalSizeXUnit": unit_for_x_axis,
    "PhysicalSizeYUnit": unit_for_y_axis,
    ... # for other axes
}

plane_li = [
    {"TheC": 0, "TheZ": 0, "TheT": 0},
    {"TheC": 0, "TheZ": 1, "TheT": 0},
    ...  # for each plane in the data
]

metadata = {
    "Pixels": pixels,
    "Plane": plane_li,
    "Creator": "napari-tiff",  
    "Channel": {
        "Name": channel_names, # for example ["DAPI", "GFP", "RFP"]
    },
    "axes": axes_order,  # for example "TZCYX"
}
```

Then we can pass this metadata to the `imwrite` function:

```python
import tifffile

tifffile.imwrite(
    "path_to_file.tiff",
    data,
    ome=True,
    metadata=metadata,
    software="napari-tiff",
    compression="ADOBE_DEFLATE"
)
```

## ImageJ TIFF

ImageJ TIFF is the native format for ImageJ. It allows storing much less metadata 
but if your workflow is based on ImageJ it might be good idea to use this format.

We have not found a formal specification for this format, but it is widely used and supported by much software.

### Reading ImageJ TIFF

Similar to OME-TIFF, the `TiffFile` class has a property, `is_imagej`, that allows checking if the file is an ImageJ TIFF. If it is, we can access metadata through the `imagej_metadata` property. It will return a `dict` with all metadata stored in the ImageJ format.

The information about scale and units for X and Y axes are stored in TIFF tags `XResolution`, `YResolution`, and `ResolutionUnit`. The scale for Z is stored in `imagej_metadata` under the `spacing` key, and its unit is stored under the `unit` key. The scale for Time is stored in `imagej_metadata` under the `finterval` key and is in seconds.

Here is some example code for reading this information:

```python
import tifffile

def read_resolution_from_tags(image_file: tifffile.TiffFile) -> tuple[float, float, str]:
    tags = image_file.pages[0].tags
    if image_file.is_imagej:
        unit = image_file.imagej_metadata["unit"]
    else:
        unit_tag = tags["ResolutionUnit"].value
        if unit_tag == 3:
            unit = 'cm'
        elif unit_tag == 2:
            unit = 'inch'
        else:
            raise KeyError(f"wrong scalar {tags['ResolutionUnit']}, {tags['ResolutionUnit'].value}")

    x_spacing = tags["XResolution"].value[1] / tags["XResolution"].value[0]
    y_spacing = tags["YResolution"].value[1] / tags["YResolution"].value[0]
    
    return x_spacing, y_spacing, unit


with tifffile.TiffFile("path_to_file.tiff") as tif:
    if tif.is_imagej:
        data = tif.asarray()
        axes = tif.series[0].axes
        x_spacing, y_spacing, unit = read_resolution_from_tags(tif)


        imagej_metadata = tif.imagej_metadata
        if "spacing" in imagej_metadata:
            z_spacing = imagej_metadata["spacing"]
        else:
            z_spacing = 1.0
        if "finterval" in imagej_metadata:        
            time_interval = imagej_metadata.get("finterval", 1.0)
        else:
            time_interval = 1.0
            

        print(f"Data shape {data.shape}, Axes order {axes}, X/Y Scale: {(x_spacing, y_spacing)}, Unit: {unit}, Z Scale: {z_spacing} {unit}, Time Scale: {time_interval} s")
```

### Writing ImageJ TIFF

ImageJ metadata can also be passed to the `imwrite` function, but it should be in a different format. The `resolution` is required to store scale information for X and Y. For example:

```python
import tifffile

metadata = {
    "spacing": z_spacing,  # scale for Z axis
    "finterval": time_interval,  # scale for Time axis
    "fpx": 1/time_interval,  # frequency for Time axis
    "unit": unit,  # unit for all axes
    "Labels": channel_names,  # for example ["DAPI", "GFP", "RFP"]
}

resolution = (1/x_spacing, 1/y_spacing)

tifffile.imwrite(
    "path_to_file.tiff",
    data,
    imagej=True,
    metadata=metadata,
    resolution=resolution,
    software="napari-tiff"
)
```

ImageJ has issues with loading compressed TIFF files, for the compression methods that we've checked. We've therefore omitted it in these examples.


## Using napari_tiff

If you are happy with napari's data model, you can use `napari_tiff` to read/write TIFF files. 
Doing so does not require a full napari installation (with a Qt frontend), as it is using `napari.types.LayerDataTuple` as the input and output of its functions.

The `napari.types.FullLayerData` is a tuple of three elements: data, metadata, and layer type. The data is a NumPy array, the metadata is a `dict` with all metadata, and the layer type is a string with the napari layer type.

The functions that you might use are `napari_tiff.napari_tiff_reader.reader_function` and 
`napari_tiff.napari_tiff_writer.images_layer_writer`. 
