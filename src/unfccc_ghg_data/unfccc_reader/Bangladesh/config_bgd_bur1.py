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
                "skip_rows_start": 0,
                "skip_rows_end": 0,
            },
            "208": {
                "area": ["63,720,527,120"],
                "cols": ["380,437,491"],
                "skip_rows_start": 8,
                "skip_rows_end": 6,
            },
        },
        "rows_to_fix": {
            -2: [
                "ch4 emission from rice field",
                "indirect nitrous oxide (n2o) from n based fertilizer",
                "Direct nitrous oxide (n2o) emissions from fertilizer application",
                "Total enteric ch4 emissions",
                "Total Manure ch4 emissions",
                "Total Direct n2o emissions from manure system",
                "Total indirect n2o emissions - Volatilization",
                "Total indirect n2o emissions - leaching/Runoff",
            ],
            3: [
                "3 - GHG Emissions Agriculture, Livestock & Forest and Other Land -Use"
            ],
            -3: [
                "Greenhouse gas source and sink categories",
            ],
        },
    },
}
