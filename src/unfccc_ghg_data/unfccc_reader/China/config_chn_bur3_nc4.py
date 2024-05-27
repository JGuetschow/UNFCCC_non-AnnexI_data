"""Config for China BUR3 and NC4

Configuration for reading the China's NC4 and BUR3 from pdf.
Full configuration is contained here including configuraton for conversions to
primap2 data format.

NOTE: GWPs are a mixture of AR4 and SAR values (SAR except for HFC-245fa and HFC-365mfc)
Thus the Kyoto GHG gas basket is not fully consistent with SAR GWPs and is
re-generated for the processed version of the data.
"""

## general config
gwp_to_use = "SARGWP100"  # see note above


## NC4 specific config
config_nc4 = {
    "scenario": "NC4",
    "year": 2017,
    "unit": "kt / year",
    "pages_overview": {
        "CHN": [30],
        "MAC": [218],
        "HKG": [190],
    },
    "pages_inventory": {
        "CHN": [31, 32],
        "MAC": [219],
        "HKG": [191],
    },
    "pages_fgases": {
        "CHN": [33],
        "MAC": [],
        "HKG": [192],
    },
}

## BUR3 specific config
config_bur3 = {
    "scenario": "BUR3",
    "year": 2018,
    "unit": "kt / year",
    "pages_overview": {
        "CHN": [11],
        "MAC": [63],
        "HKG": [43],
    },
    "pages_inventory": {
        "CHN": [13, 14],
        "MAC": [61],
        "HKG": [44],
    },
    "pages_fgases": {
        "CHN": [15],
        "MAC": [],
        "HKG": [45],
    },
    "pages_recalc": {
        "CHN": [18],
        "MAC": [67],
        "HKG": [50],
    },
}
