# Land Surface - Processing Tools

## Description

In these modules, we provide tools to generate land surface products from satellite data (Sentinel-2). The products are composites and categories (woody, herbaceous, bare soil, water, and snow).  
The composites and categories are generated using the available data for a whole year.  
Apart from the composites and categories, we also provide tools to generate some statistics for the land surface categories products. These statistics serve as a tool to help visualize the data for quality control purposes and they include the following:
- FRAC: Fraction of the class pressence in the year
- PROBMEAN: Mean probabilities of each class in the year
- PROBSTD: Standard deviation of the probabilities of each class in the year
- NUNIQUE: Number of unique classes in the year 
* For the first three statistics, there is a NOSNOW variant that excludes the snow class from the calculations.
