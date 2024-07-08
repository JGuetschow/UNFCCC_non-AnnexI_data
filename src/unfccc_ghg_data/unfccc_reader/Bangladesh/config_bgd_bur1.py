"""
Configuration file to read Bangladesh's BUR 1.
"""
coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

inv_conf_per_year = {
    "2013": {
        "page_defs": {
            "207": {
                "area": ["60,630,534,79"],
                "cols": ["387,444,495"],
                "skip_rows": 0,
            },
            "208": {
                "area": ["65,687,527,120"],
                "cols": ["380,437,491"],
                "skip_rows": 5,
            },
        },
    },
}
