from urllib.parse import urlencode


def cdse_url(
    lat,
    lon,
    start_date,
    end_date=None,
    cloud_coverage=0,
    zoom=13,
    dataset="S2_L2A_CDAS",
):
    """
    Generate a URL to the Copernicus Data and Exploitation Platform (CDS&E) browser
    with the specified parameters.

    # Example usage
    url = generate_cdse_url(
        lat=33.65164,
        lon=118.03823,
        dataset="S2_L2A_CDAS",
        start_date="2020-06-15",
        end_date="2020-06-15"
    )
    """
    base_url = "https://browser.dataspace.copernicus.eu/"

    end_date = end_date or start_date
    params = {
        "zoom": zoom,
        "lat": lat,
        "lng": lon,
        "themeId": "DEFAULT-THEME",
        "visualizationUrl": "U2FsdGVkX181jftOkqo8Lr3KujPs84mBRzcOup22xZl2KFg9EXVV2i2h%2Bv%2FU%2BAV1ikmXAg426AnnOoxVxdb3bJJDMixb6na7C8z3g3uJcM5dMc3nSZrCfcQceFrVYxxy",
        "datasetId": dataset,
        "fromTime": f"{start_date}T00%3A00%3A00.000Z",
        "toTime": f"{end_date}T23%3A59%3A59.999Z",
        "layerId": "1_TRUE_COLOR",
        "demSource3D": '"MAPZEN"',
        "cloudCoverage": cloud_coverage,
        "dateMode": "SINGLE",
    }

    return base_url + "?" + urlencode(params)
