"""Config for Bosnia and Herzegovina's BTR1

Full configuration including PRIMAP2 conversion config and metadata

Data have been read manually from pdf and completed in xlsx

"""

# ###
# for reading
# ###

# general
gwp_to_use = "AR5GWP100"
tolerance = 0.01

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
    "provenance": "provenance",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "BIH-GHG-Inventory",
    "area": "BIH",
    "scenario": "BTR1",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
}

filter_remove = {}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/660085",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Bosnia and Herzegovina. 2024 Biennial Transparency Report (BTR). BTR1. "
    "National Communications (NC). NC5",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}


# ###
# for processing
# ###
# aggregate categories
country_processing_step1 = {
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["PFCS", "HFCS"],
        "source_GWP": gwp_to_use,
    }
}


gas_baskets = {
    "FGASES (SARGWP100)": ["PFCS (SARGWP100)", "HFCS (SARGWP100)", "NF3", "SF6"],
    "FGASES (AR4GWP100)": ["PFCS (AR4GWP100)", "HFCS (AR4GWP100)", "NF3", "SF6"],
    "FGASES (AR5GWP100)": ["PFCS (AR5GWP100)", "HFCS (AR5GWP100)", "NF3", "SF6"],
    "FGASES (AR6GWP100)": ["PFCS (AR6GWP100)", "HFCS (AR6GWP100)", "NF3", "SF6"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "PFCS (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "PFCS (AR6GWP100)"],
}
