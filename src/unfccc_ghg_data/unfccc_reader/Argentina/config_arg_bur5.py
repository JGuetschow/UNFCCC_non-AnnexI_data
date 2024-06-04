"""Config for Argentina BUR5

Configuration for reading the inventory files underlying Argentina's BUR 5.
Full configuration is contained here including configuraton for  conversions to
primap2 data format.
"""

### config for reading and conversion to primap2 format
time_format = "%Y"

coords_cols = {
    "category": "id_ipcc",
    "entity": "tipo_de_gas",
    "time": "año",
    "data": "valor_en_toneladas_de_gas",
}

add_coords_cols = {}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "ARG-GHG-Inventory",
    "provenance": "measured",
    "area": "ARG",
    "scenario": "BUR5",
    # "unit": "tonnes" # this might not work as he entity has to be specified
}

unit = "t"

coords_value_mapping = {
    "category": "PRIMAP1",
    "unit": "PRIMAP1",
    "entity": {
        "HFC_23": "HFC23",
        "HFC_32": "HFC32",
        "HFC_125": "HFC125",
        "HFC_134a": "HFC134a",
        "HFC_152a": "HFC152a",
        "HFC_143a": "HFC143a",
        "HFC_227ea": "HFC227ea",
        "HFC_236fa": "HFC236fa",
        "HFC_365mfc": "HFC365mfc",
        "HFC_245fa": "HFC245fa",
        "PFC_143_CF4": "CF4",
        "PFC_116_C2F6": "C2F6",
    },
}

coords_value_filling = {}

filter_remove = {}

filter_keep = {}

meta_data = {
    "ref": "https://unfccc.int/documents/634953",
    "ref2": "https://ciam.ambiente.gob.ar/repositorio.php?tid=9&stid=36&did=394#",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "",
    "comment": "Read fom pcsv file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}


### config for processing

# many custom categories which are not in climate categories, so automatic
# aggregation would be a lot of coding work
cats_to_agg = {
    "1.A.1.c": {
        "sources": ["1.A.1.c.ii"],
        # "orig_cat_name": "Manufacture of Solid Fuels and Other Energy Industries",
    },
    "1.A.1": {
        "sources": ["1.A.1.a", "1.A.1.b", "1.A.1.c"],
        # "orig_cat_name": "Energy Industries",
    },
    "1.A.2": {
        "sources": [
            "1.A.2.a",
            "1.A.2.b",
            "1.A.2.c",
            "1.A.2.d",
            "1.A.2.e",
            "1.A.2.f",
            "1.A.2.g",
            "1.A.2.j",
            "1.A.2.l",
            "1.A.2.m",
        ],
        # "orig_cat_name": "Manufacturing Industries and Construction",
    },
    "1.A.3.a": {
        "sources": ["1.A.3.a.ii"],
        # "orig_cat_name": "Civil Aviation"
    },
    "1.A.3.b": {
        "sources": ["1.A.3.b.iii", "1.A.3.b.vii"],
        # "orig_cat_name": "Road Transportation",
    },
    "1.A.3.d": {
        "sources": ["1.A.3.d.ii"],
        # "orig_cat_name": "Water-Borne Navigation"
    },
    "1.A.3.e": {
        "sources": ["1.A.3.e.i"],
        # "orig_cat_name": "Other Transportation"
    },
    "1.A.3": {
        "sources": ["1.A.3.a", "1.A.3.b", "1.A.3.c", "1.A.3.d", "1.A.3.e"],
        # "orig_cat_name": "Transport",
    },
    "1.A.4.a": {
        "sources": ["1.A.4.a.i", "1.A.4.a.ii", "1.A.4.a.iii"],
        # "orig_cat_name": "Commercial/Institutional",
    },
    "1.A.4": {
        "sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"],
        # "orig_cat_name": "Other Sectors"
    },
    "1.A": {
        "sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4"],
        # "orig_cat_name": "Fuel Combustion Activities",
    },
    "1.B.1.a.i": {
        "sources": ["1.B.1.a.i.1", "1.B.1.a.i.2"],
        # "orig_cat_name": "Underground mines",
    },
    "1.B.1.a": {
        "sources": ["1.B.1.a.i"],
        # "orig_cat_name": "Coal Mining and Handling"
    },
    "1.B.1.c": {
        "sources": ["1.B.1.c.i"],
        # "orig_cat_name": "Solid Fuel Transformation"
    },
    "1.B.1": {
        "sources": ["1.B.1.a", "1.B.1.c"],
        # "orig_cat_name": "Solid Fuels"
    },
    "1.B.2.a": {
        "sources": ["1.B.2.a.i", "1.B.2.a.ii", "1.B.2.a.iii", "1.B.2.a.iv"],
        # "orig_cat_name": "Oil",
    },
    "1.B.2.b": {
        "sources": [
            "1.B.2.b.i",
            "1.B.2.b.ii",
            "1.B.2.b.iii",
            "1.B.2.b.iv",
            "1.B.2.b.v",
            "1.B.2.b.vi",
        ],
        # "orig_cat_name": "Natural Gas",
    },
    "1.B.2": {
        "sources": ["1.B.2.a", "1.B.2.b"],
        # "orig_cat_name": "Oil and Natural Gas"
    },
    "1.B": {
        "sources": ["1.B.1", "1.B.2"],
        # "orig_cat_name": "Fugitive Emissions from Fuels"
    },
    "1": {
        "sources": ["1.A", "1.B"],
        # "orig_cat_name": "Energy"
    },
    "2.A.4": {
        "sources": ["2.A.4.a", "2.A.4.b", "2.A.4.d"],
        # "orig_cat_name": "Other Process Uses of Carbonates",
    },
    "2.A": {
        "sources": ["2.A.1", "2.A.2", "2.A.4"],
        # "orig_cat_name": "Mineral Industry"
    },
    "2.B.8": {
        "sources": ["2.B.8.a", "2.B.8.b", "2.B.8.c", "2.B.8.f"],
        # "orig_cat_name": "Petrochemical and Carbon Black Production",
    },
    "2.B.9": {
        "sources": ["2.B.9.a"],
        # "orig_cat_name": "Fluorochemical Production"
    },
    "2.B": {
        "sources": ["2.B.1", "2.B.2", "2.B.5", "2.B.7", "2.B.8", "2.B.9"],
        # "orig_cat_name": "Chemical Industry",
    },
    "2.C": {
        "sources": ["2.C.1", "2.C.2", "2.C.3", "2.C.6"],
        # "orig_cat_name": "Metal Industry"
    },
    "2.D": {
        "sources": ["2.D.1", "2.D.2"],
        # "orig_cat_name": "Non-Energy Products from Fuels and Solvent Use",
    },
    "2.F.1": {
        "sources": ["2.F.1.a", "2.F.1.b"],
        # "orig_cat_name": "Refrigeration and Air Conditioning",
    },
    "2.F": {
        "sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4"],
        # "orig_cat_name": "Product Uses as Substitutes for Ozone Depleting Substances",
    },
    "2": {
        "sources": ["2.A", "2.B", "2.C", "2.D", "2.F"],
        # "orig_cat_name": "IPPU"
    },
    # AFOLU
    # 3.A - Livestock
    "3.A.1.a": {
        "sources": ["3.A.1.a.i", "3.A.1.a.ii"],
        # "orig_cat_name": "Cattle"
    },
    "3.A.1": {
        "sources": [
            "3.A.1.a",
            "3.A.1.b",
            "3.A.1.c",
            "3.A.1.d",
            "3.A.1.e",
            "3.A.1.f",
            "3.A.1.g",
            "3.A.1.h",
        ],
        # "orig_cat_name": "Enteric Fermentation",
    },
    "3.A.2.a": {
        "sources": ["3.A.2.a.i", "3.A.2.a.ii"],
        # "orig_cat_name": "Cattle"
    },
    "3.A.2": {
        "sources": [
            "3.A.2.a",
            "3.A.2.b",
            "3.A.2.c",
            "3.A.2.d",
            "3.A.2.e",
            "3.A.2.f",
            "3.A.2.g",
            "3.A.2.h",
            "3.A.2.i",
        ],
        # "orig_cat_name": "Enteric Fermentation",
    },
    "3.A": {
        "sources": ["3.A.1", "3.A.2"],
        # "orig_cat_name": "Livestock"
    },
    # 3.B - Land
    "3.B.1.a.i": {
        "sources": ["3.B.1.a.i.1", "3.B.1.a.i.2"],
        # "orig_cat_name": "",
    },  # no name, not the normal IPCC category
    "3.B.1.a.ii": {
        "sources": ["3.B.1.a.ii.1", "3.B.1.a.ii.2"],
        # "orig_cat_name": "",
    },  # no name, not the normal IPCC category
    "3.B.1.a": {
        "sources": ["3.B.1.a.i", "3.B.1.a.ii"],
        # "orig_cat_name": "Forest Land Remaining Forest Land",
    },
    # '3.B.1.b': {'sources': ['3.B.1.b.i', '3.B.1.b.ii'],
    #             'name': 'Land Converted to Forest Land'},
    "3.B.1": {
        "sources": ["3.B.1.a"],
        # "orig_cat_name": "Forest Land"
    },  # , '3.B.1.b'],
    "3.B.2.b": {
        "sources": ["3.B.2.b.i", "3.B.2.b.ii"],
        # "orig_cat_name": "Land Converted to Cropland",
    },
    "3.B.2": {
        "sources": ["3.B.2.b"],
        # "orig_cat_name": "Cropland"
    },
    "3.B.3.b": {
        "sources": ["3.B.3.b.i", "3.B.3.b.ii"],
        # "orig_cat_name": "Land Converted to Grassland",
    },
    "3.B.3": {
        "sources": ["3.B.3.b"],
        # "orig_cat_name": "Grassland"
    },
    "3.B": {
        "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.7"],
        # "orig_cat_name": "Land"
    },
    # 3.C - Aggregate Sources and Non-CO2 Emissions Sources on Land
    "3.C.1.a": {
        "sources": ["3.C.1.a.i", "3.C.1.a.ii"],
        # "orig_cat_name": "Biomass Burning in Forest Lands",
    },
    "3.C.1.b": {
        "sources": ["3.C.1.b.i", "3.C.1.b.ii"],
        # "orig_cat_name": "Biomass Burning in Croplands",
    },
    "M.3.C.1.b.AG": {
        "sources": ["3.C.1.b.i"],
        # "orig_cat_name": "Biomass Burning in Croplands - Agriculture",
    },
    "M.3.C.1.b.LU": {
        "sources": ["3.C.1.b.ii"],
        # "orig_cat_name": "Biomass Burning in Croplands - LULUCF",
    },
    "3.C.1.c": {
        "sources": ["3.C.1.c.i", "3.C.1.c.ii"],
        # "orig_cat_name": "Biomass Burning in Grasslands",
    },
    "M.3.C.1.c.AG": {
        "sources": ["3.C.1.c.i"],
        # "orig_cat_name": "Biomass Burning in Grasslands - Agriculture",
    },
    "M.3.C.1.c.LU": {
        "sources": ["3.C.1.c.ii"],
        # "orig_cat_name": "Biomass Burning in Grasslands - LULUCF",
    },
    "3.C.1": {
        "sources": ["3.C.1.a", "3.C.1.b", "3.C.1.c"],
        # "orig_cat_name": "Biomass Burning"
    },
    "M.3.C.1.AG": {
        "sources": ["M.3.C.1.b.AG", "M.3.C.1.c.AG"],
        # "orig_cat_name": "Biomass Burning - Agriculture",
    },
    "M.3.C.1.LU": {
        "sources": ["3.C.1.a", "M.3.C.1.b.LU", "M.3.C.1.c.LU"],
        # "orig_cat_name": "Biomass Burning",
    },
    "3.C.4.d": {
        "sources": [
            "3.C.4.d.i",
            "3.C.4.d.ii",
            "3.C.4.d.iii",
            "3.C.4.d.iv",
            "3.C.4.d.v",
            "3.C.4.d.vi",
            "3.C.4.d.vii",
        ],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.4.g": {
        "sources": ["3.C.4.g.i", "3.C.4.g.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.4": {
        "sources": [
            "3.C.4.a",
            "3.C.4.b",
            "3.C.4.c",
            "3.C.4.d",
            "3.C.4.e",
            "3.C.4.f",
            "3.C.4.g",
            "3.C.4.n",
            "3.C.4.o",
        ],
        # "orig_cat_name": "Direct N2O Emissions from Managed Soils",
    },
    "3.C.5.a": {
        "sources": ["3.C.5.a.i", "3.C.5.a.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.b": {
        "sources": ["3.C.5.b.i", "3.C.5.b.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.c": {
        "sources": ["3.C.5.c.i", "3.C.5.c.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.i": {
        "sources": ["3.C.5.d.i.1", "3.C.5.d.i.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.ii": {
        "sources": ["3.C.5.d.ii.1", "3.C.5.d.ii.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.iii": {
        "sources": ["3.C.5.d.iii.1", "3.C.5.d.iii.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.iv": {
        "sources": ["3.C.5.d.iv.1", "3.C.5.d.iv.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.v": {
        "sources": ["3.C.5.d.v.1", "3.C.5.d.v.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.vi": {
        "sources": ["3.C.5.d.vi.1", "3.C.5.d.vi.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d.vii": {
        "sources": ["3.C.5.d.vii.1", "3.C.5.d.vii.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.d": {
        "sources": [
            "3.C.5.d.i",
            "3.C.5.d.ii",
            "3.C.5.d.iii",
            "3.C.5.d.iv",
            "3.C.5.d.v",
            "3.C.5.d.vi",
            "3.C.5.d.vii",
        ],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.f": {
        "sources": ["3.C.5.f.ii"],
        # "orig_cat_name": ""
    },  # not standard IPCC2006
    "3.C.5.g.i": {
        "sources": ["3.C.5.g.i.1", "3.C.5.g.i.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.g.ii": {
        "sources": ["3.C.5.g.ii.1", "3.C.5.g.ii.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.g": {
        "sources": ["3.C.5.g.i", "3.C.5.g.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.n": {
        "sources": ["3.C.5.n.i", "3.C.5.n.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5.o": {
        "sources": ["3.C.5.o.i", "3.C.5.o.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.5": {
        "sources": [
            "3.C.5.a",
            "3.C.5.b",
            "3.C.5.c",
            "3.C.5.d",
            "3.C.5.e",
            "3.C.5.f",
            "3.C.5.g",
            "3.C.5.n",
            "3.C.5.o",
        ],
        # "orig_cat_name": "Indirect N2O Emissions from Managed Soils",
    },
    "3.C.6.a.i": {
        "sources": ["3.C.6.a.i.1"],
        # "orig_cat_name": ""
    },  # not standard IPCC2006
    "3.C.6.a.ii": {
        "sources": ["3.C.6.a.ii.1", "3.C.6.a.ii.2"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.6.a": {
        "sources": ["3.C.6.a.i", "3.C.6.a.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.6.h": {
        "sources": ["3.C.6.h.i", "3.C.6.h.ii"],
        # "orig_cat_name": "",
    },  # not standard IPCC2006
    "3.C.6.i": {
        "sources": ["3.C.6.i.i"],
        # "orig_cat_name": ""
    },  # not standard IPCC2006
    "3.C.6": {
        "sources": ["3.C.6.a", "3.C.6.h", "3.C.6.i"],
        # "orig_cat_name": "Indirect N2O Emissions from Manure Management",
    },
    "3.C": {
        "sources": ["3.C.1", "3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
        # "orig_cat_name": "Emissions from Biomass Burning",
    },
    "M.3.C.AG": {
        "sources": ["M.3.C.1.AG", "3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
        # "orig_cat_name": "Emissions from Biomass Burning - Agriculture",
    },
    "M.AG.ELV": {
        "sources": ["M.3.C.AG"],
        # "orig_cat_name": "Agriculture Excluding Livestock"
    },
    "M.3.C.LU": {
        "sources": ["M.3.C.1.LU"],
        # "orig_cat_name": "Emissions from Biomass Burning - LULUCF",
    },
    "3.D": {
        "sources": ["3.D.1"],
        # "orig_cat_name": "Other"
    },
    "M.3.D.LU": {
        "sources": ["3.D.1"],
        # "orig_cat_name": "Other - LULUCF"
    },
    "3": {
        "sources": ["3.A", "3.B", "3.C", "3.D"],
        # "orig_cat_name": "AFOLU"
    },
    "M.AG": {
        "sources": ["3.A", "M.3.C.AG"],
        # "orig_cat_name": "Agriculture"
    },
    "M.LULUCF": {
        "sources": ["3.B", "M.3.C.LU", "3.D"],
        # "orig_cat_name": "LULUCF"
    },
    # waste
    "4.A": {
        "sources": ["4.A.1", "4.A.3"],
        # "orig_cat_name": "Solid Waste Disposal"
    },
    "4.C": {
        "sources": ["4.C.1"],
        # "orig_cat_name": "Incineration and Open Burning of Waste"
    },
    "4.D.2": {
        "sources": ["4.D.2.a", "4.D.2.b", "4.D.2.c", "4.D.2.d", "4.D.2.e"],
        # "orig_cat_name": "Industrial Wastewater Treatment and Discharge",
    },
    "4.D": {
        "sources": ["4.D.1", "4.D.2"],
        # "orig_cat_name": "Wastewater Treatment and Discharge",
    },
    "4": {
        "sources": ["4.A", "4.B", "4.C", "4.D"],
        # "orig_cat_name": "Waste"
    },
    # national totals
    "0": {
        "sources": ["1", "2", "3", "4"],
        # "orig_cat_name": "National Total"
    },
    "M.0.EL": {
        "sources": ["1", "2", "M.AG", "4"],
        # "orig_cat_name": "National Total Excluding LULUCF",
    },
}
