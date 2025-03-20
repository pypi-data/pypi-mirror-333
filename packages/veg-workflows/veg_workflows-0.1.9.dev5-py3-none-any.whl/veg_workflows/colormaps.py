import numpy as np
from matplotlib.colors import ListedColormap

# from web image of legend
SCL_COLORMAP_WEB = (
    np.array(
        [
            [0, 0, 0],  # 0: No data - Black
            [255, 34, 30],  # 1: Saturated or defective - Red
            [66, 66, 66],  # 2: Dark feature/shadow - Dark Gray
            [133, 65, 29],  # 3: Cloud shadow - Dark brown
            [0, 255, 73],  # 4: Vegetation - Green
            [250, 255, 78],  # 5: Not vegetated - Yellow
            [46, 0, 196],  # 6: Water - Blue
            [117, 113, 113],  # 7: Unclassified or No Data - Black (Repeated)
            [173, 169, 169],  # 8: Cloud medium probability - Gray
            [207, 205, 205],  # 9: Cloud high probability - Light Gray
            [0, 199, 251],  # 10: Thin cirrus - Cyan
            [255, 93, 248],  # 11: Snow or ice - Magenta
        ]
    )
    / 255.0
)  # Normalize to [0, 1] for Matplotlib

# from sinergise
SCL_COLORMAP = (
    np.array(
        [
            [0, 0, 0],  # 0: No data - Black (#000000)
            [255, 0, 0],  # 1: Saturated or defective - Red (#ff0000)
            [47, 47, 47],  # 2: Dark feature/shadow - Dark Gray (#2f2f2f)
            [100, 50, 0],  # 3: Cloud shadow - Dark brown (#643200)
            [0, 160, 0],  # 4: Vegetation - Green (#00a000)
            [255, 230, 90],  # 5: Not vegetated - Yellow (#ffe65a)
            [0, 0, 255],  # 6: Water - Blue (#0000ff)
            [128, 128, 128],  # 7: Unclassified - Gray (#808080)
            [192, 192, 192],  # 8: Cloud medium probability - Gray (#c0c0c0)
            [255, 255, 255],  # 9: Cloud high probability - White (#ffffff)
            [100, 200, 255],  # 10: Thin cirrus - Cyan (#64c8ff)
            [255, 150, 255],  # 11: Snow or ice - Magenta (#ff96ff)
        ]
    )
    / 255.0  # Normalize to [0, 1] for Matplotlib
)

# Create a ListedColormap
scl_colormap_matplotlib = ListedColormap(SCL_COLORMAP, name="SCL")
