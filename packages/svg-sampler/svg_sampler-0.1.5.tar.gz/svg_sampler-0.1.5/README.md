# SVGSampler
This is a small project to quickly create 2D multiclass-datasets for machine learning applications.

You can install it using pip:

```
pip install svg_sampler
```

Then you can use the function `sample_from_svg` to sample datapoints from the filled in paths/objects of the svg.

# Examples:

```python
from svg_sampler import sample_from_svg
from matplotlib import pyplot as plt

X, y = sample_from_svg(path_to_file, 5000, normalize=True,
                       sample_setting="based_on_area", overlap_mode="upper_only")
plt.scatter(X[:, 0], X[:, 1], c=y)
plt.show()
```

<div style="display: flex;">
  <img src="examples/test.svg" alt="SVG" style="width: 30%;"/>
  <img src="examples/sampled.svg" alt="Sampled Datapoints" style="width: 40%;"/>
</div>

<div style="display: flex;">
  <img src="examples/yin_yang.svg" alt="SVG" style="width: 30%;"/>
  <img src="examples/sampled2.svg" alt="Sampled Datapoints" style="width: 40%;"/>
</div>

<div style="display: flex;">
  <img src="examples/github.svg" alt="SVG" style="width: 30%;"/>
  <img src="examples/sampled3.svg" alt="Sampled Datapoints" style="width: 40%;"/>
</div>

# Documentation

## `sample_from_svg`

```python
sample_from_svg(path, total_samples, sample_setting="equal_over_classes", overlap_mode="all", normalize=False, *, seed)
```

### Parameters

- **`path`** *(str)*: Path to the SVG file.
- **`total_samples`** *(int)*: Total number of points to sample.
- **`sample_setting`** *(str)*: Sampling mode. Options:
  - `"equal_over_classes"` – Union shapes by fill and sample equally.
  - `"equal_over_shapes"` – Sample equally from each shape.
  - `"based_on_area"` – Allocate samples proportional to the shape's area.
- **`overlap_mode`** *(str)*: Overlap handling mode. Options:
  - `"all"` – Sample from all overlapping shapes.
  - `"upper_only"` – Only sample from the top (upper) shape in overlapping regions.
- **`normalize`** *(bool)*: If True, normalize the sampled coordinates per axis to [0, 1].
- **`seed`** *(int)*: Seed for random number generation.

### Returns

- **`X`** *(ndarray)*: Array of shape (N, 2) with (x, y) coordinates.
- **`y`** *(ndarray)*: Numeric class labels for each sample point.

# Dependencies

    numpy
    shapely
    svgpathtools
    matplotlib
