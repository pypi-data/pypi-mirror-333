BANDS_L2A = {
    10: ["B02", "B03", "B04", "B08"],
    20: ["B05", "B06", "B07", "B8A", "B11", "B12"],
    60: ["B01", "B09"],
}

BANDS_L2A_ALL = BANDS_L2A[10] + BANDS_L2A[20] + BANDS_L2A[60]

BANDS_L2A_RESOLUTION = {band: res for res, bands in BANDS_L2A.items() for band in bands}
