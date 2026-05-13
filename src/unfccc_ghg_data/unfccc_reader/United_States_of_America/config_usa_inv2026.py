"""Config for USA 2024 Inventroy

General configuration for reading the inventory files for USA's official draft 2025
inventory from csv

The EPA has never released the final inventory but was forced to publish the
draft inventory under the Freedom of Information Act

https://www.edf.org/freedom-information-act-documents-epas-greenhouse-gas-inventory

"""

gwp_to_use = "AR5GWP100"

# table definitions
inventory_files = {
    ## Chapter 3: energy
    # * 3-1, (detail not sufficient for all gases, stationary and mobile summed for CH4, N2O)
    "Chapter 3 - Energy": {
        "Table 3-1.csv": {
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "1",
                        "Fossil Fuel Combustion": "1.A",
                        "Transportation": "1.A.3",
                        "Electricity Generation": "1.A.1",
                        "Industrial": "1.A.2",
                        "Residential": "1.A.4.b",
                        "Commercial": "1.A.4.a",
                        "U.S. Territories": "1.A.5.a.v",
                        "Non-Energy Use of Fuels": "",
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Incineration of Waste": "1.A.5.a.iv",
                        "Coal Mining": "M1.B.1.a",  # abandoned underground mines are missing
                        "CO2 Transport, Injection, and Geological Storage": "",
                        "Abandoned Oil and Gas Wells": "M.1.B.2.ab.6",
                        "Biomass-Wooda": "M.BIO.Wood",
                        "International Bunker Fuelsb": "M.BK",
                        "Biofuels-Ethanola": "M.BIO.Ethanol",
                        "Biofuels-Biodiesela": "M.BIO.Biodiesel",
                        "Biomass-MSWa": "M.BIO.MSW",
                    },
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "1",
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Coal Mining": "M1.B.1.a",  # abandoned underground mines are missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Abandoned Oil and Gas Wells": "M.1.B.2.ab.6",
                        "Stationary Combustion": "M.1.stationary",
                        "Abandoned Underground Coal Mines": "1.B.1.a.i.3",
                        "Mobile Combustion": "M.1.mobile",
                        "Incineration of Waste": "1.A.5.a.iv",
                        "International Bunker Fuelsb": "M.BK",
                    },
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "1",
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Stationary Combustion": "M.1.stationary",
                        "Mobile Combustion": "M.1.mobile",
                        "Incineration of Waste": "1.A.5.a.iv",
                        "International Bunker Fuelsb": "M.BK",
                        "Total": "1",
                    },
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "1",
                    },
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq": None,
        },
    },
    # * 3-3, 1.A subsectors for CO2, CH4, N2O
    #     * 3-8: CO2 details per fuel and sector. probably not necessary
    # * 3-9: CH4 details per fuel and sector. probably not necessary
    # * 3-10: N2O details per fuel and sector. probably not necessary
    # * 3-21, 3-22: coal mines (1.B.1)
    # * 3-23 CH4 from abandoned coal mines
    # * 3-25, 3-26, 3-27 Petroleum systems
    # * 3-28, 3-29, 3-30 Natural gas systems
    # * 3-21, 3-32, abandoned oil and gas wells
    # * 3-33 1.C
    # * 3-36: bunkers
    # * 3-39 Biomass CO2 (not necessary, included in 3-1)
    #
    # ##  chapter 4: IPPU
    # * 4-1: overview table covering all sectors and gases (no F-gas per gas data)
    # * 4-31: Details petrochemical production (optional)
    # * 4-33: HFC-22 production
    # * 4-35: f-gas production other than HFC-22
    # * 4-38: CO2 from non-EOR Utilization (probably optional)
    # * 4-45: Iron and steel details (optional)
    # * 4-50: Aluminum production gas details (needed for f-gases)
    # * 4-52: Magnesium production gas details (needed for f-gases)
    # * 4-57: electronics industry gas details (needed for f-gases)
    # * 4-49: ODS substitutes (needed for f-gases)
    # * 4-61: Electrical equipment (needed for f-gases)
    # * 4-62: Other product use (needed for f-gases)
    #
    # ## chapter 5: Agriculture
    # * 5-1: overview. not enough details to map to IPCC categories, but sufficient for
    #     PRIMAP-hist
    # * 5-3: CH4 enteric fermentation
    # * 5-6: Manure management
    # * 5-10: Agricultural soils direct and indirect
    # * 5-11: liming details (optional, detail not needed)
    # * 5-15: field burning (optional, detail not needed)
    #
    # ## chapter 6: LULUCF
    # * 6-1: overview (suffices for LULUCF without details)
    # * 6-7: forest fires. needed to split CH4 and N2O
    # * 6-14: grassland fires: needed to split CH4 and N2O
    # * 6-16: peatland remaining peatland: needed for non-CO2
    #
    # ## chapter 7: waste
    # 7-1: overview: not much detail, but enough for PRIMAP-hist
}


coords_terminologies = {
    "area": "ISO3",
    "category": "CRF2013_2023",
    "scenario": "PRIMAP",
}

coords_defaults_template = {
    "source": "USA-GHGAI",
    "provenance": "measured",
    "area": "USA",
    "scenario": "2026INV",
}

meta_data = {
    "references": "https://ghgi.cgs.umd.edu/index.html",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Greenhouse Gas Inventory and Analysis for the United States",
    "comment": "Read fom csv files by Johannes Gütschow",
    "institution": "University of Maryland - Center for Global Sustainability",
}
