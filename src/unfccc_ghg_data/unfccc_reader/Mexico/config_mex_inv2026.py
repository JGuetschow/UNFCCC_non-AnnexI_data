"""Config for Mexico's 2023 inventory

Full configuration including PRIMAP2 conversion config and metadata

"""

gwp_to_use = "AR5GWP100"


# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

# manual category codes
cat_codes_manual = {
    # "EMISIONES BRUTAS (con UTCUTS1)2": "",
    "EMISIONES Sin UTCUTS3": "M.0.EL",
    "EMISIONES NETAS (Emisiones + Absorciones)4": "0",
    "1A1ci Fabricación de combustibles sólidos (coque de carbón)": "1A1ci",
    "1A1cii Otras Industrias de la energía": "1A1cii",
    "1A2ci Petroquímica": "1A2ci",
    "1A2cii Industria química": "1A2cii",
    "1A2ciii Fertilizantes": "1A2ciii",
    "1A2ei Elaboración de azúcares": "1A2ei",
    "1A2eii Elaboración de bebidas": "1A2eii",
    "1A2eiii Elaboración de productos de tabaco": "1A2eiii",
    "1A2eiiii Elaboración de cerveza": "1A2eiv",
    "1A2eiiiii Elaboración de alimentos": "1A2ev",
    "1A2mi Fabricación de vidrio y productos de vidrio": "1A2mi",
    "1A2mii Fabricación de productos de hule": "1A2mii",
    "1A2miii Otras ramas": "1A2miii",
    "1B2ai Venteo petróleo": "1B2ai",
    "1B2aii Quemado petróleo": "1B2aii",
    "1B2aiii Otras fugitivas petróleo": "1B2aiii",
    "1B2bi Venteo gas natural": "1B2bi",
    "1B2bii Quemado gas natural": "1B2bii",
    "1B2biii Otras fugitivas gas natural": "1B2biii",
    "Bunkers5": "MBK",
    "Aviación internacional": "MBKA",
    "Marítimo internacional": "MBKM",
    "Emisiones de CO2 por quema de biomasa": "MBIO",
    "[3A1i] Otros (especificar)": "3A1j",
    "[3A2g] Otros (especificar)": "3A2j",
    "[4(IV)] Emisiones de GEI por quemado de biomasa": "4",
    "[4(IV)A] Emisiones de quemado de biomasa en tierras forestales": "4A",
    "[4(IV)C] Emisiones de quemado de biomasa en tierras praderas": "4C",
    "[4(IV)H] Emisiones de quemado de biomasa en otras tierras": "4F",
    # "Nota:": "\\IGNORE",
}

cat_code_regexp = r"^\[(?P<code>[a-zA-Z0-9]{1,6})\].*"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "CRT1_MEX",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "MEX-GHG-Inventory",
    "provenance": "measured",
    "area": "MEX",
    "scenario": "INV2026",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "CO2": "CO2",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
        "HFC-23": f"HFC23 ({gwp_to_use})",
        "HFC-410A": f"HFC410a ({gwp_to_use})",
        "HFC-43-10mee": f"HFC4310mee ({gwp_to_use})",
        "HFC-125": f"HFC125 ({gwp_to_use})",
        "HFC-134": f"HFC134 ({gwp_to_use})",
        "HFC-134a": f"HFC134a ({gwp_to_use})",
        "HFC-404A": f"HFC404a ({gwp_to_use})",
        "HFC-407C": f"HFC407c ({gwp_to_use})",
        "HFC-245fa": f"HFC245fa ({gwp_to_use})",
        "HFC-152a": f"HFC152a ({gwp_to_use})",
        "HFC-227ea": f"HFC227ea ({gwp_to_use})",
        "HFC-236fa": f"HFC236fa ({gwp_to_use})",
        # "HFC-365mfc/227ea": f"HFC365mfc ({gwp_to_use})",
        # TODO: include in openscm units as mixture
        "HFC-365mfc": f"HFC365mfc ({gwp_to_use})",
        "HFC-507a": f"HFC507a ({gwp_to_use})",
        "HFC-32": f"HFC32 ({gwp_to_use})",
        "CF4": f"CF4 ({gwp_to_use})",
        "C2F6": f"C2F6 ({gwp_to_use})",
        "C3F8": f"C3F8 ({gwp_to_use})",
        "C4F6": f"C4F6 ({gwp_to_use})",  # not in openscm_units
        "c-C4F8": f"cC4F8 ({gwp_to_use})",
        "C5F8": f"C5F8 ({gwp_to_use})",  # not in openscm_units
        "NF3": f"NF3 ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "EMISIONES t de CO2e": f"KYOTOGHG ({gwp_to_use})",
        "Emisión neta de Carbono Negro (t)": "BC",
    },
}

filter_remove = {
    "fcat": {
        "category": [
            "",
            "EMISIONES BRUTAS (con UTCUTS1)2",
            "EMISIONES NETAS (t de CO2e)",  # already present as EMISIONES NETAS (Emisiones + Absorciones)4
        ]
    },
    "fent": {"entity": ["EMISIONES kt de CO2e", ""]},
}

filter_keep = {}

meta_data = {
    "references": "https://www.gob.mx/cms/uploads/attachment/file/1031246/INEGyCEI_1990-2024_Dif_221025.xlsx",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Mexico INVENTARIO NACIONAL DE EMISIONES DE GASES Y COMPUESTOS DE EFECTO INVERNADERO (INEGYCEI)",
    "comment": "Read fom xlsx by Johannes Gütschow",
    "institution": "UNFCCC",
}

# processing
cat_terminology_proc = "IPCC2006_PRIMAP"

CRT1_MEX_to_IPCC2006_mapping = {
    "mapping": {
        "0": "0",  # Total National Emissions and Removals
        "M.0.EL": "M.0.EL",  # National total excluding LULUCF
        "1": "1",  # Energy
        "1.A": "1.A",  # Fuel Combustion Activities
        "1.A.1": "1.A.1",  # Energy Industries
        "1.A.1.a": "1.A.1.a",  # Public electricity and heat production
        "1.A.1.b": "1.A.1.b",  # Petroleum Refining
        "1.A.1.c": "1.A.1.c",  # Manufacture of Solid Fuels and Other Energy Industries
        "1.A.1.c.i": "1.A.1.c.i",  # Manufacture of Solid Fuels
        "1.A.1.c.ii": "1.A.1.c.ii",  # XXCCXX Other energy industries
        "1.A.2": "1.A.2",  # Manufacturing Industries and Construction
        "1.A.2.a": "1.A.2.a",  # Iron and Steel
        "1.A.2.b": "1.A.2.b",  # Non-Ferrous Metals
        "1.A.2.c": "1.A.2.c",  # Chemicals
        # 1A2ci Petroquímica
        #     1A2cii Industria química
        #     1A2ciii Fertilizantes
        "1.A.2.d": "1.A.2.d",  # Pulp, Paper and Print
        "1.A.2.e": "1.A.2.e",  # Food Processing, Beverages and Tobacco
        # 1A2ei Elaboración de azúcares
        #     1A2eii Elaboración de bebidas
        # 1A2eiii Elaboración de productos de tabaco
        #     1A2eiiii Elaboración de cerveza
        # 1A2eiiiii Elaboración de alimentos
        "1.A.2.f": "1.A.2.f",  # Non-Metallic Minerals
        "1.A.2.g": "1.A.2.g",  # Transport Equipment
        "1.A.2.h": "1.A.2.h",  # Manufacturing of Machinery
        "1.A.2.i": "1.A.2.i",  # Mining (Excluding Fuels) and Quarrying
        "1.A.2.j": "1.A.2.j",  # Wood and Wood Products
        "1.A.2.k": "1.A.2.k",  # Construction
        "1.A.2.l": "1.A.2.l",  # Textile and Leather
        "1.A.2.m": "1.A.2.m",  # Non-Specified Industry
        # '1.A.2.m.i': '1.A.2.m.i',  # Glass and glass products
        # '1.A.2.m.ii': '1.A.2.m.ii',  # Manufacture of rubber products
        # '1.A.2.m.iii': '1.A.2.m.iii',  # Other branches
        "1.A.3": "1.A.3",  # Transport
        "1.A.3.a": "1.A.3.a.ii",  # Domestic Aviation
        "1.A.3.b": "1.A.3.b",  # Road Transportation
        "1.A.3.c": "1.A.3.c",  # Railways
        "1.A.3.d": "1.A.3.d.ii",  # Domestic Navigation
        "1.A.3.e": "1.A.3.e",  # Other Transportation
        "1.A.4": "1.A.4",  # Other Sectors
        "1.A.4.a": "1.A.4.a",  # Commercial/Institutional
        "1.A.4.b": "1.A.4.b",  # Residential
        "1.A.4.c": "1.A.4.c",  # Agriculture/Forestry/Fishing/Fish Farms
        "1.B": "1.B",  # Fugitive Emissions from Fuels
        "1.B.1": "1.B.1",  # Solid Fuels
        "1.B.1.a": "1.B.1.a",  # Coal Mining and Handling
        "1.B.1.a.i": "1.B.1.a.i",  # Underground Mines
        "1.B.1.a.ii": "1.B.1.a.ii",  # Surface Mines
        "1.B.1.b": "1.B.1.b",  # Uncontrolled Combustion, and Burning Coal Dumps
        "1.B.2": "1.B.2",  # Oil and Natural Gas
        "1.B.2.a": "1.B.2.a",  # Oil
        "1.B.2.a.i": "1.B.2.a.i",  # Venting
        "1.B.2.a.ii": "1.B.2.a.ii",  # Flaring
        "1.B.2.a.iii": "1.B.2.a.iii",  # All Other
        "1.B.2.b": "1.B.2.b",  # Natural Gas
        "1.B.2.b.i": "1.B.2.b.i",  # Venting
        "1.B.2.b.ii": "1.B.2.b.ii",  # Flaring
        "1.B.2.b.iii": "1.B.2.b.iii",  # All Other
        "2": "2",  # Industrial Processes and Product Use
        "2.A": "2.A",  # Mineral Industry
        "2.A.1": "2.A.1",  # Cement Production
        "2.A.2": "2.A.2",  # Lime Production
        "2.A.3": "2.A.3",  # Glass Production
        "2.A.4": "2.A.4",  # Other Process Uses of Carbonates
        "2.A.5": "M.2.A.5",  # Other
        "2.B": "2.B",  # Chemical Industry
        "2.B.1": "2.B.1",  # Ammonia Production
        "2.B.10": "2.B.10",  # Other (Please Specify)
        "2.B.2": "2.B.2",  # Nitric Acid Production
        "2.B.3": "2.B.3",  # Adipic Acid Production
        "2.B.4": "2.B.4",  # Caprolactam, Glyoxal and Glyoxylic Acid Production
        "2.B.5": "2.B.5",  # Carbide Production
        "2.B.6": "2.B.6",  # Titanium Dioxide Production
        "2.B.7": "2.B.7",  # Soda Ash Production
        "2.B.8": "2.B.8",  # Petrochemical and Carbon Black Production
        "2.B.9": "2.B.9",  # Fluorochemical Production
        "2.C": "2.C",  # Metal Industry
        "2.C.1": "2.C.1",  # Iron and Steel Production
        "2.C.2": "2.C.2",  # Ferroalloys Production
        "2.C.3": "2.C.3",  # Aluminium Production
        "2.C.4": "2.C.4",  # Magnesium Production
        "2.C.5": "2.C.5",  # Lead Production
        "2.C.6": "2.C.6",  # Zinc Production
        "2.C.7": "2.C.7",  # Other (Please Specify)
        "2.D": "2.D",  # Non-Energy Products from Fuels and Solvent Use
        "2.D.1": "2.D.1",  # Lubricant Use
        "2.D.2": "2.D.2",  # Paraffin Wax Use
        "2.D.3": "2.D.3",  # Solvent use
        "2.D.4": "2.D.4",  # Other (please specify)
        "2.E": "2.E",  # Electronics Industry
        "2.E.1": "2.E.1",  # Integrated Circuit or Semiconductor
        "2.E.2": "2.E.2",  # TFT Flat Panel Display
        "2.E.3": "2.E.3",  # Photovoltaics
        "2.E.4": "2.E.4",  # Heat Transfer Fluid
        "2.E.5": "2.E.5",  # Other (Please Specify)
        "2.F": "2.F",  # Product Uses as Substitutes for Ozone Depleting Substances
        "2.F.1": "2.F.1",  # Refrigeration and Air Conditioning
        "2.F.2": "2.F.2",  # Foam Blowing Agents
        "2.F.3": "2.F.3",  # Fire Protection
        "2.F.4": "2.F.4",  # Aerosols
        "2.F.5": "2.F.5",  # Solvents
        "2.F.6": "2.F.6",  # Other Applications (Please Specify)
        "2.G": "2.G",  # Other Product Manufacture and Use
        "2.G.1": "2.G.1",  # Electrical Equipment
        "2.G.2": "2.G.2",  # SF6 and PFCs from Other Product Uses
        "2.G.3": "2.G.3",  # N2O from Product Uses
        "2.G.4": "2.G.4",  # Other (Please Specify)
        "2.H": "2.H",  # Other
        "2.H.1": "2.H.1",  # Pulp and Paper Industry
        "2.H.2": "2.H.2",  # Food and Beverages Industry
        "2.H.3": "2.H.3",  # Other (Please Specify)
        "3": "M.AG",  # Total Agriculture
        "3.A": "3.A.1",  # Enteric Fermentation
        "3.A.1": "3.A.1.a",  # Cattle
        "3.A.2": "3.A.1.c",  # Sheep
        "3.A.3": "3.A.1.h",  # Swine
        "3.A.4.a": "3.A.1.b",  # Buffalo
        "3.A.4.b": "3.A.1.e",  # Camels
        "3.A.4.d": "3.A.1.d",  # Goats
        "3.A.4.e": "3.A.1.f",  # Horses
        "3.A.4.f": "3.A.1.g",  # Mules and Asses
        "3.A.4.h": "3.A.1.j",  # Other (Please Specify)
        "3.B": "M.3.B.CRF",  # Manure Management NOTE: not mapped as indirect emissions have to be removed
        "3.B.1": "3.A.2.a",  # Cattle
        "3.B.2": "3.A.2.c",  # Sheep
        "3.B.3": "3.A.2.h",  # Swine
        "3.B.4.a": "3.A.2.b",  # Buffalo
        "3.B.4.b": "3.A.2.e",  # Camels
        "3.B.4.d": "3.A.2.d",  # Goats
        "3.B.4.e": "3.A.2.f",  # Horses
        "3.B.4.f": "3.A.2.g",  # Mules and Asses
        "3.B.4.g": "3.A.2.i",  # Poultry
        "3.B.4.h": "3.A.2.j",  # Other (Please Specify)
        "3.B.5": "3.C.6",  # Indirect N2O emissions from manure management
        "3.C": "3.C.7",  # Rice Cultivation
        "3.D": "M.3.C.45.AG",  # Agricultural Soils
        "3.D.1": "M.3.C.4.AG",  # Direct N2O emissions from managed soils
        "3.D.2": "M.3.C.5.AG",  # Indirect N2O Emissions from Managed Soils
        "3.F": "3.C.1.b",  # Field burning of Agricultural Residues
        "3.G": "M.3.C.2.AG",  # Liming
        "3.H": "M.3.C.3.AG",  # Urea Application
        "4": "M.LULUCF",  # Total LULUCF
        # ignore subsectors of land types as they are not complete in Table4
        "4.A": "3.B.1",  # Forest Land
        "4.A.1": "3.B.1.a",  # Forest Land Remaining Forest Land
        "4.A.2": "3.B.1.b",  # Land Converted to Forest Land
        "4.B": "3.B.2",  # Cropland
        "4.B.1": "3.B.2.a",  # Cropland Remaining Cropland
        "4.B.2": "3.B.2.b",  # Land Converted to Cropland
        "4.C": "3.B.3",  # Grassland
        "4.C.1": "3.B.3.a",  # Grassland Remaining Grassland
        "4.C.2": "3.B.3.b",  # Land Converted to Grassland
        "4.D": "3.B.4",  # Wetlands
        "4.D.1": "3.B.4.a",  # Wetlands Remaining Wetlands
        "4.D.2": "3.B.4.b",  # Land Converted to Wetlands
        "4.E": "3.B.5",  # Settlements
        "4.E.1": "3.B.5.a",  # Settlements Remaining Settlements
        "4.E.2": "3.B.5.b",  # Land Converted to Settlements
        "4.F": "3.B.6",  # Other Land
        "4.F.1": "3.B.6.a",  # Other Land Remaining Other Land
        "4.F.2": "3.B.6.b",  # Land Converted to Other Land
        "4.G": "3.D.1",  # Harvested Wood Products
        "4.H": "M.3.D.2.b.LU",  # Other ( Please Specify)
        "5": "4",  # Waste
        "5.A": "4.A",  # Solid Waste Disposal
        "5.A.1": "4.A.1",  # Managed Waste Disposal Sites
        "5.A.2": "4.A.2",  # Unmanaged Waste Disposal Sites
        "5.A.3": "4.A.3",  # Uncategorized Waste Disposal Sites (not exactly)
        "5.B": "4.B",  # Biological Treatment of Solid Waste
        "5.C": "4.C",  # Incineration and Open Burning of Waste
        "5.C.1": "4.C.1",  # Waste Incineration
        "5.C.2": "4.C.2",  # Open Burning of Waste
        "5.D": "4.D",  # Wastewater Treatment and Discharge
        "5.D.1": "4.D.1",  # Domestic Wastewater
        "5.D.2": "4.D.2",  # Industrial Wastewater
        "5.E": "4.E",  # Other (please specify)
        "M.BIO": "M.BIO",  # CO2 Emissions from Biomass
        "M.BK": "M.BK",  # International Bunkers
        "M.BK.A": "M.BK.A",  # International Aviation (Aviation Bunkers)
        "M.BK.M": "M.BK.M",  # International Navigation (Marine Bunkers)
    },
    "aggregate": {
        # for now just the operations necessary for PRIMAP-hist (+ a few).
        # full aggregation is complicated and needs overwriting which is not
        # implemented in the current category mapping code
        # 1
        ## 1.A
        # domestic aviation and shipping
        "1.A.3.a": {"sources": ["1.A.3.a.ii"]},
        "1.A.3.d": {"sources": ["1.A.3.d.ii"]},
        ## 1.B
        # no rebuilding of subsectors where we add items from "other" categories
        # has to be added for full tree consistency
        "1.B.2.a": {
            "sources": [
                "1.B.2.a.i",
                "1.B.2.a.ii",
                "1.B.2.a.iii",
                "M.1.B.3.b.v",
                "M.1.B.3.b.viii",
            ]
        },
        # consistency check
        "1.B": {"sources": ["1.B.1", "1.B.2"]},
        # 2
        # consistency check
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"],
        },
        # 3
        ## 3.A
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
                "3.A.2.j",
            ]
        },
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        ## 3.B
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"]},
        ## 3.C
        "3.C.1": {"sources": ["3.C.1.b"]},
        "M.3.C.1.AG": {"sources": ["3.C.1.b"]},
        "3.C.2": {"sources": ["M.3.C.2.AG"]},
        "3.C.3": {"sources": ["M.3.C.3.AG"]},
        "3.C.4": {"sources": ["M.3.C.4.AG"]},
        "3.C.5": {"sources": ["M.3.C.5.AG"]},
        "3.C": {
            "sources": ["3.C.1", "3.C.2", "3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"]
        },
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "M.3.C.2.AG",
                "M.3.C.3.AG",
                "M.3.C.4.AG",
                "M.3.C.5.AG",
                "3.C.6",
                "3.C.7",
            ]
        },
        # 3.D
        "M.3.D.2.LU": {"sources": ["M.3.D.2.b.LU"]},
        "3.D.2": {"sources": ["M.3.D.2.LU"]},
        "M.3.D.LU": {"sources": ["3.D.1", "M.3.D.2.LU"]},
        "3.D": {"sources": ["M.3.D.LU"]},
        "M.AG.ELV": {"sources": ["M.3.C.AG"]},
        # consistency check
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},
        "M.LULUCF": {"sources": ["3.B", "M.3.D.LU"]},
        "3": {"sources": ["M.AG", "M.LULUCF"]},
        # top level
        "0": {"sources": ["1", "2", "3", "4", "5"]},
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4", "5"]},
    },
    "unmapped": [
        # just for automatic checks of unmapped categories in new data,
        # so we don't have to go through all of them again
        # country specific cattle detail
        # FF combustion categories too specialized for mapping
        # (can be added if needed)
        "1.A.2.c.i",  # 1A2ci Petroquímica
        "1.A.2.c.ii",  # 1A2cii Industria química
        "1.A.2.c.iii",  # 1A2ciii Fertilizantes
        "1.A.2.e.i",  # 1A2ei Elaboración de azúcares
        "1.A.2.e.ii",  #     1A2eii Elaboración de bebidas
        "1.A.2.e.iii",  # 1A2eiii Elaboración de productos de tabaco
        "1.A.2.e.iiii",  #     1A2eiiii Elaboración de cerveza
        "1.A.2.e.iiiii",  # 1A2eiiiii Elaboración de alimentos
        "1.A.2.m.i",
        "1.A.2.m.ii",
        "1.A.2.m.ii",
    ],
}
