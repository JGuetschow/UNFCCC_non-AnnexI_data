"""Config for United Arab Emirates BUR1

Full configuration including PRIMAP2 conversion config and metadata

"""

#### configuration for PM2 format
gwp_to_use = "AR4GWP100"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_2006_ARE_Inv",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "ARE-GHG-Inventory",
    "provenance": "measured",
    "area": "ARE",
    "scenario": "BUR1",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": {
        "Total": "0",
        "Energy": "1",
        "Fuel Combustion Activities": "1.A",
        "Fugitive Emissions": "1.B",
        "Venting": "1.B.2.c.1",
        "Flaring": "1.B.2.c.2",
        "Other Fugitives": "M.1.B.2.OF",
        "IPPU": "2",
        "Mineral Industry": "2.A",
        "Cement": "2.A.1",
        "Chemical Industry": "2.B",
        "Ammonia": "2.B.1",
        "Metal Industry": "2.C",
        "Iron & Steel": "2.C.1",
        "Aluminum": "2.C.3",
        "Agriculture": "3",
        "Enteric Fermentation": "3.A",
        "Manure Management": "3.B",
        "Managed Soils": "3.D",
        "LUCF": "4",
        "Waste": "5",  # waste is more or less in 2006 categories
        "Solid Waste Disposal": "5.A",
        "Landfill": "M.5.A.LF",
        "Biological treatment": "5.B",
        "Composting": "M.5.B.COMP",
        "Incineration": "5.C.1",
        "Wastewater": "5.D",
        "Memo Items": "IGNORE",
        "Aviation": "M.1.A",
        "Marine bunker": "M.1.B",
    },
    "entity": {
        "CO2": "CO2",
        "CH4": "CH4",
        "N2O": "N2O",
        "CH4.1": f"CH4 ({gwp_to_use})",
        "N2O.1": f"N2O ({gwp_to_use})",
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "Total GHG": f"KYOTOGHG ({gwp_to_use})",
    },
}

filter_remove = {
    "rem_cat": {"category": ["Memo Items"]},
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/635318",
    "rights": "",
    "contact": "mail@johannes-guestchow.de",
    "title": "United Arab Emirates. National Communication (NC). NC 5. Biennial Update Report (BUR). BUR 1.",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

## processing iconfig
terminology_proc = "IPCC2006_PRIMAP"

category_conversion = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.B": "1.B",
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",
        "2.B": "2.B",
        "2.B.1": "2.B.1",
        "2.C": "2.C",
        "2.C.1": "2.C.1",
        "2.C.3": "2.C.3",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.D": "M.3.C.45.AG",
        "4": "M.LULUCF",
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.B",
        "5.C.1": "4.C.1",
        "5.D": "4.D",
        "M.1.A": "M.BK.A",
        "M.1.B": "M.BK.M",
        "1.B.2.c.1": "M.1.B.2.VEN",
        "1.B.2.c.2": "M.1.B.2.FL",
        "M.1.B.2.OF": "M.1.B.2.OF",
        # "M.5.A.LF": "",
        # "M.5.B.COMP": "",
    },
    "aggregate": {
        "1.B.2": {
            "sources": ["M.1.B.2.VEN", "M.1.B.2.FL", "M.1.B.2.OF"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "2": {
            "sources": ["2.G"],
            "filter": {
                "entity": ["HFCS"],
            },
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            "filter": {
                "entity": ["CH4", "N2O"],
            },
        },
        "3.C": {
            "sources": ["M.3.C.45.AG"],
            "filter": {
                "entity": ["N2O"],
            },
        },
        "M.AG.ELV": {
            "sources": ["3.C"],
            "filter": {
                "entity": ["N2O"],
            },
        },
        "M.AG": {  # consitency check
            "sources": ["3.A", "M.AG.ELV"],
            "filter": {
                "entity": ["N2O", "CH4"],
            },
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "4.C": {
            "sources": ["4.C.1"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "M.BK": {
            "sources": ["M.BK.A", "M.BK.M"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O"],
            },
        },
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O", "HFCS", "PFCS"],
            },
        },
        "0": {  # consistency check
            "sources": ["1", "2", "3", "4"],
            "filter": {
                "entity": ["CO2", "CH4", "N2O", "HFCS", "PFCS"],
            },
        },
    },
}

processing_info_country = {
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["PFCS", "HFCS"],
        "source_GWP": gwp_to_use,
    },
}
