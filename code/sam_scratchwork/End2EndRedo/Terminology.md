We've been converging on a standardized association of words and meaning,
but usage is still inconsistent throughout our code. I propose these usages:

SYSTEM

- **evaluation metric** --- a program that compares two given segmentations, producing a numerical similarity score (and potentially more data). May be shortened to `metric`. Preferred over `algorithm`.
- **segmentation algorithm** --- a program that produces from two . May be shortened to `algorithm`. Preferred over `method`.
- **guess segmentation** --- output of one of our segmentation algorithms. May be shortened to `guess`.
- **groundtruth segmentation** --- hand-labeled data to which we compare the `guess segmentations`. May be shortened to `groundtruth`.
- **newspage** --- a single input datapoint in PQ's database, to be fed into `segmentation algorithm`s. Associated with one physical page of news. Contains both an `image` and `metadata`.
- **image** --- the visual component of a `newspage`, containing an array of pixel values and no more. Preferred over `jpg` or `jp2`.
- **metadata** --- the non-visual information of a `newspage`, for instance publication date and textblock coordinates. Preferred over `xml` or `ocr`.
- **report** --- the human-readable document produced by our end-to-end system to describe the performance of specified `segmentation algorithm`s on specified `newspage`s with respect to specified `metric`s. Will have format .pdf or .html.

GEOMETRY

- **region** --- a subset of the plane.
- **segmentation** --- an un-ordered collection of `article`s, potentially overlapping.
- **article** --- a mapping from `label`s to `polygon`s. Polygons potentially overlap.
- **polygon** --- a region represented as a disjoint union of `box`es.
- **box** --- an axis-aligned rectangle. A special type of region.

LABELS

- **label** --- a category to which a `region` may belong.
- **title** --- the `label` for headlines and article titles
- **article** --- the `label` for body text
- **other** --- the `label` for non-textual items such as images and advertisements.
