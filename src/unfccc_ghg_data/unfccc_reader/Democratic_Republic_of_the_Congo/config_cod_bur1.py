"""Config for Democratic Republic of the Congo's BUR1

Full configuration including PRIMAP2 conversion config and metadata

"""

# ###
# for reading
# ###

# general
gwp_to_use = "SARGWP100"
terminology_proc = "IPCC2006_PRIMAP"


page_defs = {
    "23": {
        "table_areas": ["56,516,766,185"],
        "columns": ["107,165,212,258,300,341,375,438,492,530,569,609,666,716"],
        "split_text": False,
        "flavor": "stream",
    },
    "25": {
        "table_areas": ["93,765,507,465"],
        "split_text": False,
        "flavor": "stream",
    },
    "47": {
        "table_areas": ["71,392,531,75"],
        "split_text": False,
        "flavor": "stream",
    },
    # 71: AFOLU by subsectors and gas
    "71": {
        "table_areas": ["34,517,803,78"],
        "columns": ["85,129,170,219,261,307,347,391,435,484,521,557,625,688,743"],
        "split_text": False,
        "flavor": "stream",
    },
    # 72, 73: AFOLU by main sectors but without biomass burning and 3.B.3, 3.B.6
    # the tables are broken after reading. so ignore for now
    "72": {
        "table_areas": ["56,239,530,71"],
        "split_text": False,
        "flavor": "stream",
    },
    "73": {
        "table_areas": ["56,777,530,520"],
        "split_text": False,
        "flavor": "stream",
    },
    # page 74: AFOLU again, but with different contents
    # second table livestock
    "74": {
        "table_areas": ["56,746,517,448", "123,339,476,73"],
        "split_text": False,
        "flavor": "stream",
    },
    # page 75/77: tables on livestock, but with different values. the latter tables seem to be consistent
    # maybe other emissions are included in the first tables, the text (translation) is a bit unclear
    "75": {
        "table_areas": ["123,779,477,702", "139,669,461,384", "87,282,513,67"],
        "columns": ["166,236,289,357,411", "199,293,381", "139,203,265,327,389,451"],
        "split_text": False,
        "flavor": "stream",
    },
    "76": {
        "table_areas": ["123,779,509,702", "61,561,541,233", "56,201,557,67"],
        "columns": [
            "139,203,265,327,389,451",
            "105,168,230,291,354,417,478",
            "121,182,245,309,370,433,494",
        ],
        "split_text": False,
        "flavor": "stream",
    },
    "77": {
        "table_areas": ["56,777,556,549"],
        "split_text": False,
        "flavor": "stream",
    },
    # page 82: land use emissions (CO2 only, also included on page 71 )
    # page 83: 3.C per gas (also included in other tables)
    # page 84: subsectors for 3.C.1
    "84": {
        "table_areas": ["129,517,716,185"],
        "split_text": False,
        "flavor": "stream",
    },
    # page 85: details for 3.C.2,3,4+5,6,7
    "85": {
        "table_areas": ["81,517,764,180"],
        "columns": ["124,180,240,291,353,400,438,497,550,583,645,685"],
        "split_text": False,
        "flavor": "stream",
    },
}

table_defs = {
    "Tableau_3": {  # Emissions et absorptions de la RDC en Gg
        "tables": [0],
        "unit": "Gg",
        "cat_codes_mapping": {
            "Energie": "1",
            "PIUP": "2",
            "Bétail": "3.A",  # not completely clear, maybe includes other things as well
            "Terres forestières": "3.B.1",  # for removals. for emissions 3.B.2
            "Sources agrégées": "M.3.C.NBB",  # no biomass burning included
            "Déchets": "4",
        },
        "drop_rows": [0, 1, 2, 3],
        "header": [
            [
                "category",
                "Energie",
                "Energie",
                "Energie",
                "PIUP",
                "Bétail",
                "Bétail",
                "Terres forestières",
                "Terres forestières",
                "Sources agrégées",
                "Sources agrégées",
                "Sources agrégées",
                "Déchets",
                "Déchets",
                "Déchets",
            ],
            [
                "entity",
                "CO2",
                "CH4",
                "N2O",
                "CO2",
                "CH4",
                "N2O",
                "CO2 (séquestré)",
                "CO2 (émis)",
                "CO2",
                "CH4",
                "N2O",
                "CO2",
                "CH4",
                "N2O",
            ],
        ],
    },
    "Tableau_5": {  # Emissions et absorptions de la RDC en Gg
        "tables": [1],
        "rows_to_fix": {},
        "category_cell": [0, 0],
        "unit": "GgCO2eq",
        "add_coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
        },
        "cat_codes_mapping": {
            "Energie": "1",
            "PIUP": "2",
            "Agriculture": "M.AG.NBB",  # no biomass burning inlcuded
            "FAT": "M.LULUCF",  # same data as Terres forestières from Tableau 3
            "Déchets": "4",
            "Total": "0",
        },
    },
    "Tableau_16": {  # contribution des émissions des principaux gaz
        "tables": [2],
        "rows_to_fix": {},
        "add_coords_defaults": {"category": "1.A"},
        "drop_rows": [0, 1],
        "header": [
            [
                "entity",
                "CO2",
                "CH4",
                "N2O",
                f"CO2 ({gwp_to_use})",
                f"CH4 ({gwp_to_use})",
                f"N2O ({gwp_to_use})",
                f"KYOTOGHG ({gwp_to_use})",
            ],
            [
                "unit",
                "Gg",
                "Gg",
                "Gg",
                "GgCO2eq",
                "GgCO2eq",
                "GgCO2eq",
                "GgCO2eq",
            ],
        ],
        "filter_remove": {
            "f_co2eq": {
                "entity": [
                    f"CO2 ({gwp_to_use})",
                    f"CH4 ({gwp_to_use})",
                    f"N2O ({gwp_to_use})",
                ],
            },
        },
    },
    "Tableau_27": {  # Emissions par catégorie et gaz (Gg) du secteur Agriculture, Foresterie et autres Affectations des Terres
        "tables": [3],
        "rows_to_fix": {},
        "unit": "Gg",
        "cat_codes_mapping": {
            "3A1-Fermentation Entérique": "3.A.1",
            "3A2-EmissionsCH4dues àlaGestiondufumier": "3.A.2",
            "3C1-BrûlageBiomasse CH4": "3.C.1",
            "3C7-EmissionsCH4dues auxriziculture": "3.C.7",
            "3A2-Emissionsdirectes N2OduesàlaGestiondu fumier": "3.A.2",
            "3C1-BrûlageBiomasse": "3.C.1",
            "3C4-Emissionsdirectes N2Oduesauxsolsgérés N2O": "3.C.4",
            "3C5-Emissionsindirectes N2Oduesauxsolsgérés": "3.C.5",
            "3C6-Emissionsindirectes N2OduesàlaGestiondu fumier": "3.C.6",
            "3C2-Chaulage": "3.C.2",
            "3C3-Applicationd('Urée": "3.C.3",
            "3.B.1-Forêts": "3.B.1",
            "3.B.2-Terrescultivées CO2": "3.B.2",
            "3.B.3-Prairies": "3.B.3",
            "3.B.6-AutresTerres": "3.B.6",
        },
        "drop_rows": [0, 1],
        "header": [
            [
                "category",
                "3A1-Fermentation Entérique",
                "3A2-EmissionsCH4dues àlaGestiondufumier",
                "3C1-BrûlageBiomasse CH4",
                "3C7-EmissionsCH4dues auxriziculture",
                "3A2-Emissionsdirectes N2OduesàlaGestiondu fumier",
                "3C1-BrûlageBiomasse",
                "3C4-Emissionsdirectes N2Oduesauxsolsgérés N2O",
                "3C5-Emissionsindirectes N2Oduesauxsolsgérés",
                "3C6-Emissionsindirectes N2OduesàlaGestiondu fumier",
                "3C2-Chaulage",
                "3C3-Applicationd('Urée",
                "3.B.1-Forêts",
                "3.B.2-Terrescultivées CO2",
                "3.B.3-Prairies",
                "3.B.6-AutresTerres",
            ],
            [
                "entity",
                "CH4",
                "CH4",
                "CH4",
                "CH4",
                "N2O",
                "N2O",
                "N2O",
                "N2O",
                "N2O",
                "CO2",
                "CO2",
                "CO2",
                "CO2",
                "CO2",
                "CO2",
            ],
        ],
    },
    "Tableau_29": {  # Émissions agrégées dues au bétail, aux sources agrégées et émissions sans CO2 (Gg CO2-éq)
        "tables": [6],
        "rows_to_fix": {},
        "unit": "GgCO2eq",
        "cat_codes_mapping": {
            "Bétail": "M.3.A.T29",  # inconsistent with other tables
            "Sources agrégées et émissions sans CO2": "3.C",
            "Total": "M.AG",  # maybe LU bits of 3.C.1 included
        },
        "drop_rows": [0, 1, 2],
        "header": [
            [
                "category",
                "Bétail",
                "Bétail",
                "Sources agrégées et émissions sans CO2",
                "Sources agrégées et émissions sans CO2",
                "Sources agrégées et émissions sans CO2",
                "Total",
            ],
            [
                "entity",
                f"CH4 ({gwp_to_use})",
                f"CO2 ({gwp_to_use})",
                f"CH4 ({gwp_to_use})",
                f"N2O ({gwp_to_use})",
                f"CO2 ({gwp_to_use})",
                f"KYOTOGHG ({gwp_to_use})",
            ],
        ],
    },
    "Tableau_30": {  # Synthèse de l'évolution des émission imputables au Bétail (Gg éq-CO2)
        "tables": [7, 8],
        "rows_to_fix": {},
        "add_coords_defaults": {
            "category": "M.3.A.T30"  # not consistent with other 3.A time-series
        },
        "drop_rows": [0, 1],
        "header": [
            [
                "unit",
                "Gg",
                "Gg",
                "GgCO2eq",
                "GgCO2eq",
                "GgCO2eq",
            ],
            [
                "entity",
                "CH4",
                "N2O",
                f"CH4 ({gwp_to_use})",
                f"N2O ({gwp_to_use})",
                f"KYOTOGHG ({gwp_to_use})",
            ],
        ],
        "filter_remove": {
            "f_co2eq": {
                "entity": [f"CH4 ({gwp_to_use})", f"N2O ({gwp_to_use})"],
            },
        },
    },
    "Tableau_31": {  # Émissions de CH4 (Gg) de 2000 à 2019
        "tables": [9],
        "rows_to_fix": {},
        "add_coords_defaults": {
            "entity": "CH4",
        },
        "unit": "Gg",
        "cat_codes_mapping": {
            "Fermentation entérique": "M.3.A.1.T31",
            "Gestion du fumier": "M.3.A.2.T31",
            "Total": "M.3.A.T31",  # not consisten with table 30
        },
        "drop_rows": [0, 1, 2],
        "header": [
            [
                "category",
                "Fermentation entérique",
                "Gestion du fumier",
                "Total",
            ],
        ],
    },
    "Tableau_32": {  # Emissions de CH4 (Gg) imputables à la fermentation entérique
        "tables": [10, 11],
        "rows_to_fix": {},
        "add_coords_defaults": {
            "entity": "CH4",
        },
        "unit": "Gg",
        "cat_codes_mapping": {
            "Vaches laitières": "M.3.A.1.a.i.T31",
            "Autres bovins": "M.3.A.1.a.ii.T31",
            "Moutons": "M.3.A.1.c.T31",
            "Chèvres": "M.3.A.1.d.T31",
            "Suidés": "M.3.A.1.h.T31",
            "Total": "M.3.A.1.T31",
        },
        "drop_rows": [0, 1, 2],
        "header": [
            [
                "category",
                "Vaches laitières",
                "Autres bovins",
                "Moutons",
                "Chèvres",
                "Suidés",
                "Total",
            ],
        ],
    },
    "Tableau_33": {  # Emissions de CH4 (Gg) imputables à la gestion du fumier
        "tables": [12],
        "rows_to_fix": {},
        "add_coords_defaults": {
            "entity": "CH4",
        },
        "unit": "Gg",
        "cat_codes_mapping": {
            "Vaches laitières": "M.3.A.2.a.i.T31",
            "Autres bovins": "M.3.A.2.a.ii.T31",
            "Moutons": "M.3.A.2.c.T31",
            "Chèvres": "M.3.A.2.d.T31",
            "Suidés": "M.3.A.2.h.T31",
            "Volaille": "M.3.A.2.i.T31",
            "Total": "M.3.A.2.T31",
        },
        "drop_rows": [0, 1, 2],
        "header": [
            [
                "category",
                "Vaches laitières",
                "Autres bovins",
                "Moutons",
                "Chèvres",
                "Suidés",
                "Volaille",
                "Total",
            ],
        ],
    },
    "Tableau_34": {  # Émissions directes de N20 dues à la gestion du fumier de 2000 à 2019
        "tables": [13, 14],
        "rows_to_fix": {},
        "add_coords_defaults": {
            "entity": "N2O",
        },
        "unit": "Gg",
        "cat_codes_mapping": {
            "Vaches laitières": "M.3.A.2.a.i.T31",
            "Autres bovins": "M.3.A.2.a.ii.T31",
            "Moutons": "M.3.A.2.c.T31",
            "Chèvres": "M.3.A.2.d.T31",
            "Suidés": "M.3.A.2.h.T31",
            "Volaille": "M.3.A.2.i.T31",
            "Total": "M.3.A.2.T31",
        },
        "drop_rows": [0, 1, 2],
        "header": [
            [
                "category",
                "Vaches laitières",
                "Autres bovins",
                "Moutons",
                "Chèvres",
                "Suidés",
                "Volaille",
                "Total",
            ],
        ],
    },
    "Tableau_39": {  # émissions de CH4 et N2O dues au Brûlage de biomasse
        "tables": [15],
        "rows_to_fix": {},
        "cat_codes_mapping": {
            "Brûlage de biomasse - Forêt": "M.3.C.1.a.T39",
            "Brûlage de biomasse - Savanes et prairies": "M.3.C.1.c.T39",
            "Brûlage de biomasse - Total": "M.3.C.1.T39",
        },
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "header": [
            [
                "entity",
                "CH4",
                "CH4",
                "CH4",
                f"CH4 ({gwp_to_use})",
                "N2O",
                "N2O",
                "N2O",
                f"N2O ({gwp_to_use})",
            ],
            [
                "category",
                "Brûlage de biomasse - Forêt",
                "Brûlage de biomasse - Savanes et prairies",
                "Brûlage de biomasse - Total",
                "Brûlage de biomasse - Total",
                "Brûlage de biomasse - Forêt",
                "Brûlage de biomasse - Savanes et prairies",
                "Brûlage de biomasse - Total",
                "Brûlage de biomasse - Total",
            ],
            [
                "unit",
                "Gg",
                "Gg",
                "Gg",
                "GgCO2eq",
                "Gg",
                "Gg",
                "Gg",
                "GgCO2eq",
            ],
        ],
        "filter_remove": {
            "f_co2eq": {
                "entity": [f"CH4 ({gwp_to_use})", f"N2O ({gwp_to_use})"],
            },
        },
    },
    "Tableau_40": {  # Émissions de CH4, N2O et CO2 de sources d'émissions autres que le CO2 de Terres
        "tables": [16],
        "rows_to_fix": {},
        "cat_codes_mapping": {
            "Riziculture": "3.C.7",
            "Terres cultivées (Drainage des sols)": "M.3.C.4.DOS",
            "Total": "3.C",
            "Chaulage": "3.C.2",
            "Urée": "3.C.3",
            "Gestion des sols - Directe": "M.3.C.4.LM",  # land management
            "Gestion des sols - Inirectes": "3.C.5",
            "Gestion du fumier - Inirectes": "3.C.6",
        },
        "drop_rows": [0, 1, 2, 3, 4, 5, 6, 7, 8],
        "header": [
            [
                "entity",
                "CH4",
                "CH4",
                "CH4",
                f"CH4 ({gwp_to_use})",
                "CO2",
                "CO2",
                "CO2",
                "N2O",
                "N2O",
                "N2O",
                "N2O",
                f"N2O ({gwp_to_use})",
            ],
            [
                "category",
                "Riziculture",
                "Terres cultivées (Drainage des sols)",
                "Total",
                "Total",
                "Chaulage",
                "Urée",
                "Total",
                "Gestion des sols - Directe",
                "Gestion des sols - Inirectes",
                "Gestion du fumier - Inirectes",
                "Total",
                "Total",
            ],
            [
                "unit",
                "Gg",
                "Gg",
                "Gg",
                "GgCO2eq",
                "Gg",
                "Gg",
                "GgCO2eq",
                "Gg",
                "Gg",
                "Gg",
                "Gg",
                "GgCO2eq",
            ],
        ],
        "filter_remove": {
            "f_co2eq": {
                "entity": [f"CH4 ({gwp_to_use})", f"N2O ({gwp_to_use})"],
            },
        },
    },
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "COD-GHG-Inventory",
    "provenance": "measured",
    "area": "COD",
    "scenario": "BUR1",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    # "category": "PRIMAP1",
    "entity": {
        "CO2 (séquestré)": "CO2 removals",
        "CO2 (émis)": "CO2 emissions",
    },
}

filter_remove = {}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/629121",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Democratic Republic of the Congo. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}


# ###
# for processing
# ###
# aggregate categories
country_processing_step1 = {
    "basket_copy": {
        "GWPs_to_add": ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS", "UnspMixOfHFCsPFCs"],
        "source_GWP": gwp_to_use,
    },
    "aggregate_coords": {
        f"category ({coords_terminologies['category']})": {
            "1.B": {  # because we had to fix 1.B for year 2000
                "sources": ["1.B.1", "1.B.2", "1.C"],
                "sel": {
                    "entity": ["CO2", "CH4", "N2O", "NOx", "CO", "SO2", "NMVOC"],
                },
            },
            "1": {  # because we had to fix 1.B for year 2000
                "sources": ["1.A", "1.B", "1.C"],
                "sel": {
                    "entity": ["CO2", "CH4", "N2O", "NOx", "CO", "SO2", "NMVOC"],
                },
            },
            "M.3.C.1.AG": {
                "sources": ["3.C.1.b"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.3.C.1.LU": {
                "sources": ["3.C.1.a"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.3.C.AG": {
                "sources": [
                    "M.3.C.1.AG",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                ],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.AG": {
                "sources": ["M.AG.ELV", "3.A"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.LULUCF": {
                "sources": ["3.B", "3.D", "M.3.C.1.LU"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "3": {  # conmsistency check
                "sources": ["M.AG", "M.LULUCF"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "0": {  # consistency check
                "sources": ["1", "2", "3", "4"],
                "sel": {
                    "entity": [
                        "CH4",
                        "CO2",
                        "N2O",
                        "NOx",
                        "CO",
                        "SO2",
                        "NMVOC",
                        "SF6",
                        f"HFCS ({gwp_to_use})",
                        f"PFCS ({gwp_to_use})",
                        f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                    ],
                },
            },
            "M.0.EL": {
                "sources": ["1", "2", "M.AG", "4"],
                "sel": {
                    "entity": [
                        "CH4",
                        "CO2",
                        "N2O",
                        "NOx",
                        "CO",
                        "SO2",
                        "NMVOC",
                        "SF6",
                        f"HFCS ({gwp_to_use})",
                        f"PFCS ({gwp_to_use})",
                        f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                    ],
                },
            },
        }
    },
}

gas_baskets = {
    "FGASES (SARGWP100)": [
        "HFCS (SARGWP100)",
        "PFCS (SARGWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (SARGWP100)",
    ],
    "FGASES (AR4GWP100)": [
        "HFCS (AR4GWP100)",
        "PFCS (AR4GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR4GWP100)",
    ],
    "FGASES (AR5GWP100)": [
        "HFCS (AR5GWP100)",
        "PFCS (AR5GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR5GWP100)",
    ],
    "FGASES (AR6GWP100)": [
        "HFCS (AR6GWP100)",
        "PFCS (AR6GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR6GWP100)",
    ],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
