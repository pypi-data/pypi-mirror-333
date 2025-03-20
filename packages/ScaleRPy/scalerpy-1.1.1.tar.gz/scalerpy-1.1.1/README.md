# ScaleRPy

A Python package for obtaining scaling relationships between two parameters using the 'ridge line' technique. 
Designed for use with global (i.e., integrated) and spatially-resolved astrophysical data. 
This software is compatable with observed and simulated data, facilitating strong quantitative comparisons between studies.

This project and README file are in development.

## Table of Contents


- [ScaleRPy](#scalerpy)
  - [Table of Contents](#table-of-contents)
  - [Introduction and Scientific Motivation](#introduction-and-scientific-motivation)
  - [Features](#features)
  - [Installation](#installation)
  - [Examples](#examples)
  - [Contributing](#contributing)
  - [License](#license)
  - [Citation](#citation)
  - [References](#references)
  - [Acknowledgements](#acknowledgements)

## Introduction and Scientific Motivation
Scaling relationships are correlations between two (or more) parameters. There are numerous such scaling relationships between properties of galaxies, as well as properties of spatially-resolved elements of galaxies. While software for fitting relationships to data are widely available (e.g., scipy.optimize.curve_fit), relationships obtained with these methods are not necessarily broadly comparable. Variations in the source data can result in significant differences between relationships obtained in different studies.

This package obtains scaling relationships using the ridge line technique proposed by Renzini & Peng (2015) for the global star formation main sequence ($M_* -$SFR relation). The find_ridge() function identifies the 'ridge' of any 2D distribution. To do so, a kernel density estimate (KDE) is made on the y-axis data in bins of the x-axis paramater. The peaks of the KDEs define the ridge. Users can then specify whether a single or double linear function is fit to the ridge data. This software is modifiable so that ridges can be fit to functions with other shapes.

In order to obtain objective measurements of scaling relationships, it is desirable to limit the number of subjective choices that must be made when fitting the data. These choices include the range over which data is fit and sample selection criteria. Additionally, measurements that are robust against differences in source data (such as spatial resolution) are desirable. As implemented in ScalaRPy, the ridge line technique makes significant strides toward these goals. In particular, as compared to fitting a full data set with ordinary least squares, the ridge line technique is much less likely to be biased by outliers and distributions that are assymetrical about the ridge line. However, as currently implemented it is still necessary to manually limit the range over which the ridge line is fit in order to avoid over-fitting where data is sparse. Additionally, users have options regarding the type of function the ridge line should be fit to. This is to enable improvements to this package over time, as the shape of scaling relationships are better constrained.

These limitations being noted, this package is being offered to the community for use and improvement, in the hopes that we can move toward more objective and comparable measurements of scaling relationships.

## Features

- Data Handling

    The man_dat.py module features two classes for managing data and identifying scaling relationships, serving as wrappers for the fit_funcs module. The GalDat class is designed for use with global (i.e., integrated) galaxy parameters. SpatGalDat is designed for use with spatially resolved elements. 

- Ridge Line Identification and Fitting

    These features are included in the fit_funcs.py module. 
  - find_ridge(x, y, **kwarg) identifies the ridge (i.e., mode) in two-dimensional distributions of data. This function returns a figure for validation, parameters relating to that figure, and the ridge points. The returned figure contains a 2D histogram with the ridge points overplotted. This figure allows for a manual check of the ridge points identified. By default, ridges are identified by performing kernel density estimates of the y-distribution of the data in user-specified bins of the x-data. There is also an option to identify ridges by finding the modes in 2D histograms, although these will be less precise and dependent on the number of bins specified.
  - fit_double(ridgepts) and fit_single(ridgepts) fit, respectively, a discontinuous double linear function and a single linear function to ridge points.

## Installation
This software can be installed via pip, or the modules can be accessed directly from the src/ScaleRPy folder.

## Examples
Examples of use can be found in scalerfit_example.ipynb (in development).

## Contributing
Contributions are very welcome! Please submit pull requests or open an issue if you have any suggestions or improvements.

## License
Copyright 2025 Bryanne McDonough

This software is licensed under the Apache 2.0 License. See the LICENSE file for details.

## Citation

The methodology and motivation behind this software is to be introduced in "Measuring the Resolved Star Formation Main Sequence in TNG100: Fitting Technique Matters" by McDonough, Curtis, and Brainerd (in prep). We plan to publish a preprint on ArXiv early February 2025. If you use this software or the ridge line technique as implemented in this software for your research, we request citation to that work.

Depending on the relevency to your work, you may also want to cite the original paper that introduced ridge line technique for measuring scaling relationships: "An Objective Definition for the Main Sequence of Star-forming Galaxies" by Renzini & Peng (2015). [ADS link](https://ui.adsabs.harvard.edu/abs/2015ApJ...801L..29R/abstract). DOIs: (ApJL) 10.1088/2041-8205/801/2/L29   (ArXiv) 10.48550/arXiv.1502.01027. 

## References

Renzini, Alvio, and Ying-jie Peng. “AN OBJECTIVE DEFINITION FOR THE MAIN SEQUENCE OF STAR-FORMING GALAXIES.” The Astrophysical Journal 801, no. 2 (March 12, 2015): L29. https://doi.org/10.1088/2041-8205/801/2/L29.


## Acknowledgements
This software benefits greatly from SciPy (for the kernel density estimates and ridge fitting functions).
