"""Config for UK 2024 Inventroy

General configuration for reading the inventory files for UK's official 2024
inventory from xlsx

"""

gwp_to_use = "AR5GWP100"
cols_to_drop = ["Regioncode", "NCFormat", "SourceName", "TESS1"]  # , 'TESS2']

entity_unit_filter = {
    # 'CO2': {
    #     'from': 'kilotonne',
    #     'to': 'kt',
    # },
    # 'CH4': {
    #     'from': 'kilotonne',
    #     'to': 'kt',
    # },
    # 'N2O': {
    #     'from': 'kilotonne',
    #     'to': 'kt',
    # },
    # 'SF6': {
    #     'from': 'kilotonne',
    #     'to': 'kt',
    # },
    # 'NF3': {
    #     'from': 'kilotonne',
    #     'to': 'kt',
    # },
    "CO2": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "CH4": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "N2O": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "SF6": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "NF3": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "HFC": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
    "PFC": {
        "from": "GWP CO2_AR5",
        "to": "ktCO2eq",
    },
}

time_format = "%Y"
coords_cols = {
    "category": "IPCC_code",
    # "category_name": "IPCC_name",
    # "subcategory": "Sourcename",
    # "area": "RegionName",
    "data": "Emission",
    "time": "EmissionYear",
    "entity": "Pollutant",
    "unit": "ConvertTo",
    # "type3": "TESS3",
    # "type2": "TESS2",
    # "type1": "TESS1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "CRF2013_2023",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "GBR-GHG-Inventory",
    "provenance": "measured",
    "area": "GBR",
    "scenario": "2024INV",
}

coords_value_mapping = {
    "entity": {
        "HFC": f"HFCS ({gwp_to_use})",
        "PFC": f"PFCS ({gwp_to_use})",
        "CO2": "CO2",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NF3": f"NF3 ({gwp_to_use})",
    },
    "unit": "PRIMAP1",
    # for a correct mapping we need to use IPCC_name not IPCC_code as some codes are
    # used twice so we have some aggregation (e.g. in animal species)
    "category": {
        "1A1ai": "1.A.1.a.i",  # 1A1ai_Public_Electricity&Heat_Production
        "1A1aiii": "1.A.1.a.iii",  # 1A1aiii_Public_Heat_Production
        "1A1b": "1.A.1.b",  # 1A1b_Petroleum_Refining
        "1A1ci": "1.A.1.c.i",  # 1A1ci_Manufacture_of_solid_fuels
        "1A1cii": "1.A.1.c.ii",  # 1A1cii_Oil_and_gas_extraction
        "1A1ciii": "1.A.1.c.iii",  # 1A1ciii_Other_energy_industries
        "1A2a": "1.A.2.a",  # 1A2a_Iron_and_steel
        "1A2b": "1.A.2.b",  # 1A2b_Non-Ferrous_Metals
        "1A2c": "1.A.2.c",  # 1A2c_Chemicals
        "1A2d": "1.A.2.d",  # 1A2d_Pulp_Paper_Print
        "1A2e": "1.A.2.e",  # 1A2e_food_processing_beverages_and_tobacco
        "1A2f": "1.A.2.f",  # 1A2f_Non-metallic_minerals
        "1A2giii": "1.A.2.g.iii",  # 1A2giii_Mining_and_quarrying
        "1A2gv": "1.A.2.g.v",  # 1A2gv_Construction
        "1A2gvii": "1.A.2.g.vii",  # 1A2gvii_Off-road_vehicles_and_other_machinery
        "1A2gviii": "1.A.2.g.v.iii",  # 1A2gviii_Other_manufacturing_industries_and_construction
        "1A3a": "1.A.3.a",  # 1A3a_Domestic_aviation
        "1A3bi": "1.A.3.b.i",  # 1A3bi_Cars
        "1A3bii": "1.A.3.b.ii",  # 1A3bii_Light_duty_trucks
        "1A3biii": "1.A.3.b.iii",  # 1A3biii_Heavy_duty_trucks_and_buses
        "1A3biv": "1.A.3.b.iv",  # 1A3biv_Motorcycles
        "1A3bv": "1.A.3.b.v",  # 1A3bv_Other_road_transport
        "1A3c": "1.A.3.c",  # 1A3c_Railways
        "1A3d": "1.A.3.d",  # 1A3d_Domestic_navigation
        "1A3eii": "1.A.3.e.ii",  # 1A3eii_Other_Transportation
        "1A4ai": "1.A.4.a.i",  # 1A4ai_Commercial/Institutional
        "1A4aii": "1.A.4.a.ii",  # 1A4aii_Commercial/Institutional_Mobile
        "1A4bi": "1.A.4.b.i",  # 1A4bi_Residential_stationary
        "1A4bii": "1.A.4.b.ii",  # 1A4bii_Residential:Off-road
        "1A4ci": "1.A.4.c.i",  # 1A4ci_Agriculture/Forestry/Fishing:Stationary
        "1A4cii": "1.A.4.c.ii",  # 1A4cii_Agriculture/Forestry/Fishing:Off-road
        "1A4ciii": "1.A.4.c.iii",  # 1A4ciii_Fishing
        "1A5b": "1.A.5.b",  # 1A5b_Other:Mobile
        "1B1a1i": "1.B.1.a.i.1",  # 1B1ai_Underground_mines:Mining_activities
        "1B1a1ii": "1.B.1.a.i.2",  # 1B1ai_Underground_mines:Post-mining_activities
        "1B1a1iii": "1.B.1.a.i.3",  # 1B1ai_Underground_mines:Abandoned
        "1B1a2i": "1.B.1.a.ii.1",  # 1B1aii_Surface_mines:Mining_activities
        "1B1b": "1.B.1.b",  # 1B1b_Solid_Fuel_Transformation
        "1B2a1": "1.B.2.a.1",  # 1B2a1_Oil_exploration
        "1B2a2": "1.B.2.a.2",  # 1B2a2_Oil_Production
        "1B2a3": "1.B.2.a.3",  # 1B2a3_Oil_transport
        "1B2a4": "1.B.2.a.4",  # 1B2a4_Oil_refining/storage
        "1B2a6": "1.B.2.a.6",  # 1B2a6_Oil_Production
        "1B2b1": "1.B.2.b.1",  # 1B2b1_Gas_exploration
        "1B2b2": "1.B.2.b.2",  # 1B2b2_Gas_production
        "1B2b3": "1.B.2.b.3",  # 1B2b3_Gas_processing
        "1B2b4": "1.B.2.b.4",  # 1B2b4_Gas_transmission_and_storage
        "1B2b5": "1.B.2.b.5",  # 1B2b5_Gas_distribution
        "1B2c1i": "1.B.2.c-ven.i",  # 1B2c_Venting_Oil
        "1B2c1ii": "1.B.2.c-ven.ii",  # 1B2c_Venting_Gas
        "1B2c2i": "1.B.2.c-fla.i",  # 1B2c_Flaring_Oil
        "1B2c2ii": "1.B.2.c-fla.ii",  # 1B2c_Flaring_Gas
        "1B2d": "1.B.2.d",  # 1B2d_Other_energy_industries
        "2A1": "2.A.1",  # 2A1_Cement_Production
        "2A2": "2.A.2",  # 2A2_Lime_Production
        "2A3": "2.A.3",  # 2A3_Glass_production
        "2A4a": "2.A.4.a",  # 2A4a_Other_process_uses_of_carbonates:ceramics
        "2A4b": "2.A.4.b",  # 2A4b_Other_uses_of_Soda_Ash
        "2A4d": "2.A.4.d",  # 2A4d_Other_process_uses_of_carbonates:other
        "2B1": "2.B.1",  # 2B1_Chemical_Industry:Ammonia_production
        "2B10": "2.B.10",  # 2B10_Chemical_Industry:Other
        "2B2": "2.B.2",  # 2B2_Nitric_Acid_Production
        "2B3": "2.B.3",  # 2B3_Adipic_Acid_Production
        "2B6": "2.B.6",  # 2B6_Titanium_dioxide_production
        "2B7": "2.B.7",  # 2B7_Soda_Ash_Production
        "2B8a": "2.B.8.a",  # 2B8a_Methanol_production
        "2B8b": "2.B.8.b",  # 2B8b_Ethylene_Production
        "2B8c": "2.B.8.c",  # 2B8c_Ethylene_Dichloride_and_Vinyl_Chloride_Monomer
        "2B8d": "2.B.8.d",  # 2B8d_Ethylene_Oxide
        "2B8e": "2.B.8.e",  # 2B8e_Acrylonitrile
        "2B8f": "2.B.8.f",  # 2B8f_Carbon_black_production
        "2B8g": "2.B.8.g",  # 2B8g_Petrochemical_and_carbon_black_production:Other
        "2B9a1": "2.B.9.a.i",  # 2B9a1_Fluorchemical_production:By-product_emissions
        "2B9b3": "2.B.9.b.iii",  # 2B9b3_Fluorchemical_production:Fugitive_emissions
        "2C1a": "2.C.1.a",  # 2C1a_Steel
        "2C1b": "2.C.1.b",  # 2C1b_Pig_iron
        "2C1d": "2.C.1.d",  # 2C1d_Sinter
        "2C3a": "2.C.3.a",  # 2C3_Aluminium_Production
        "2C3b": "2.C.3.b",  # 2C3_Aluminium_Production
        "2C4": "2.C.4",  # 2C4_Magnesium_production
        "2C6": "2.C.6",  # 2C6_Zinc_Production
        "2D1": "2.D.1",  # 2D1_Lubricant_Use
        "2D2": "2.D.2",  # 2D2 Non-energy_products_from_fuels_and_solvent_use:Paraffin_wax_use
        "2D3": "2.D.3",  # 2D3_Other_NEU
        "2E1": "2.E.1",  # 2E1_Integrated_circuit_or_semiconductor
        "2F1a": "2.F.1.a",  # 2F1a_Commercial_refrigeration
        "2F1b": "2.F.1.b",  # 2F1b_Domestic_refrigeration
        "2F1c": "2.F.1.c",  # 2F1c_Industrial_refrigeration
        "2F1d": "2.F.1.d",  # 2F1d_Transport_refrigeration
        "2F1e": "2.F.1.e",  # 2F1e_Mobile_air_conditioning
        "2F1f": "2.F.1.f",  # 2F1f_Stationary_air_conditioning
        "2F2a": "2.F.2.a",  # 2F2a_Closed_foam_blowing_agents (not in CRF2023_2023)
        "2F2b": "2.F.2.b",  # 2F2b_Open_foam_blowing_agents (not in CRF2023_2023)
        "2F3": "2.F.3",  # 2F3_Fire_Protection
        "2F4a": "2.F.4.a",  # 2F4a_Metered_dose_inhalers
        "2F4b": "2.F.4.b",  # 2F4b_Aerosols:Other
        "2F5": "2.F.5",  # 2F5_Solvents
        "2F6b": "2.F.6.b",  # 2F6b_Other_Applications:Contained-Refrigerant_containers
        "2G1": "2.G.1",  # 2G1_Electrical_equipment
        "2G2a": "2.G.2.a",  # 2G2_Military_applications
        "2G2b": "2.G.2.b",  # 2G2_Particle_accelerators
        "2G2e": "2.G.2.e",  # 2G2e_Electronics_and_shoes
        "2G3a": "2.G.3.a",  # 2G3a_Medical aplications
        "2G3b": "2.G.3.b",  # 2G3b_N2O_from_product_uses:_Other
        "2G4": "2.G.4",  # 2G4_Other_product_manufacture_and_use
        "3A1a": "3.A.1.Aa",  # 3A1a_Enteric_Fermentation_dairy_cattle
        "3A1b": "3.A.1.Ab",  # 3A1b_Enteric_Fermentation_non-dairy_cattle
        "3A2": "3.A.2",  # 3A2_Enteric_Fermentation_sheep
        "3A3": "3.A.3",  # 3A3_Enteric_Fermentation_swine
        "3A4": "3.A.4",  # 3A4_Enteric_Fermentation_other:deer
        "3B11a": "3.B.1.Aa",  # 3B11a_Manure_Management_Methane_dairy_cattle
        "3B11b": "3.B.1.Ab",  # 3B11b_Manure_Management_Methane_non-dairy_cattle
        "3B12": "3.B.2",  # 3B12_Manure_Management_Methane_sheep
        "3B13": "3.B.3",  # 3B13_Manure_Management_Methane_swine
        "3B14": "3.B.4",  # 3B14_Manure_Management_Methane_other:deer
        "3B21a": "3.B.1.Aa",  # 3B21a_Manure_Management_Non-methane_dairy_cattle
        "3B21b": "3.B.1.Ab",  # 3B21b_Manure_Management_Non-methane_non-dairy_cattle
        "3B22": "3.B.2",  # 3B22_Manure_Management_Non-methane_sheep
        "3B23": "3.B.3",  # 3B23_Manure_Management_Non-methane_swine
        "3B24": "3.B.4",  # 3B24_Manure_Management_Non-methane_other:poultry
        "3B25": "3.B.5",  # 3B25_Manure_Management_Indirect_Emissions_swine
        "3D11": "3.D.a.1",  # 3D11_Agriculural_Soils_Inorganic_N_Fertilisers
        "3D12a": "3.D.a.2.a",  # 3D12a_Agricultural_Soils_Manure_Applied_to_Soils
        "3D12b": "3.D.a.2.b",  # 3D12b_Agricultural_Soils_Sewage_Sludge_Applied_to_Soils
        "3D12c": "3.D.a.2.c",  # 3D12c_Agricultural_Soils_Other_Organic_Fertilisers_Applied_to_Soils
        "3D13": "3.D.a.3",  # 3D13_Agricultural_Soils_Manure_Deposited_by_Grazing_Animals
        "3D14": "3.D.a.4",  # 3D14_Agriculural_Soils_Residues
        "3D15": "3.D.a.5",  # 3D15_Agricultural_soils_Mineralization/Immobilization
        "3D16": "3.D.a.6",  # 3D16_Agricultural_soils_Cultivation_of_Organic_Soils
        "3D21": "3.D.b.1",  # 3D21_Agriculural_Soils_Indirect_Deposition
        "3D22": "3.D.b.2",  # 3D22_Agriculural_Soils_Indirect_Leaching_and_Run-off
        "3F11": "3.F.1.a",  # 3F11_Field_burning_wheat
        "3F12": "3.F.1.b",  # 3F12_Field_burning_barley
        "3F14": "3.F.1.d",  # 3F14_Field_burning_other_cereals
        "3F5": "3.F.5",  # 3F5_Field_burning_other_residues
        "3G1": "3.G.1",  # 3G1_Liming - limestone
        "3G2": "3.G.2",  # 3G2_Liming - dolomite
        "3H": "3.H",  # 3H_Urea application
        "4": "4",  # 4_Indirect_N2O_Emissions
        "4A": "4.A",  # 4A_Forest Land_Emissions_from_Drainage
        "4A1": "4.A.1",  # 4A1_ Forest Land remaining Forest Land
        "4A2": "4.A.2",  # 4A2_Cropland_converted_to_Forest_Land
        "4B1": "4.B.1",  # 4B1_Cropland Remaining Cropland
        "4B2": "4.B.2",  # 4B2_Forest_Land_converted_to_Cropland
        "4C": "4.C",  # 4C_Grassland_Emissions_from_Drainage
        "4C1": "4.C.1",  # 4C1_Grassland Remaining Grassland
        "4C2": "4.C.2",  # 4C2_Forest_Land_converted_to_Grassland
        "4D": "4.D",  # 4D_Wetlands_Emissions_from_Drainage
        "4D1": "4.D.1",  # 4D1_Wetlands remaining wetlands
        "4D2": "4.D.2",  # 4D2_Land_converted_to_Wetlands_Peat_Extraction
        "4E": "4.E",  # 4E_Settlements_Emissions_from_Drainage
        "4E1": "4.E.1",  # 4E1_Settlements remaining settlements
        "4E2": "4.E.2",  # 4E2_Forest_Land_converted_to_Settlements
        "4G": "4.G",  # 4G_Harvested Wood Products
        "5A1a": "5.A.1.a",  # 5A1a_Managed_Waste_Disposal_sites_anaerobic
        "5B1a": "5.B.1.a",  # 5B1a_composting_municipal_solid_waste
        "5B2a": "5.B.2.a",  # 5B2a_Anaerobic_digestion_municipal_solid_waste
        "5C1.1b": "5.C.1.a.ii.4",  # 5C1.1b_Biogenic:Sewage_sludge
        "5C1.2a": "5.C.1.b.i",  # 5C1.2a_Non-biogenic:municipal_solid_waste
        "5C1.2b": "5.C.1.b.ii.3",  # 5C1.2b_Non-biogenic:Clinical_waste
        "5C2.1b": "5.C.2.a.ii.5",  # 5C2.1b_Biogenic:Other
        "5C2.2b": "5.C.2.b.ii.5",  # 5C2.2b_Non-biogenic:Other
        "5D1": "5.D.1",  # 5D1_Domestic_wastewater_treatment
        "5D2": "5.D.2",  # 5D2_Industrial_wastewater_treatment
        "Aviation_Bunkers": "M.Memo.Int.Avi",  # Aviation_Bunkers
        "Marine_Bunkers": "M.Memo.Int.Mar",  # Marine_Bunkers
    },
}

meta_data = {
    "references": "https://naei.beis.gov.uk/reports/reports?report_id=1140",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Devolved Administration GHG Inventory 1990-2022",
    "comment": "Read fom xlsx file by Johannes Gütschow",
    "institution": "National Atmospheric Emissions Inventory (United Kingdom)",
}

##################################3333333333


filter_remove = {
    "f1": {
        "category": [
            "Total (excluding LULUCF, including indirect CO2)",
            "Total (including LULUCF, including indirect CO2)",
        ]
    }
}

# for processing
terminology_proc = "IPCC2006_PRIMAP"

cat_conversion = {
    "mapping": {
        "1.A.1.a.i": "1.A.1.a.i",  # 1A1ai_Public_Electricity&Heat_Production
        "1.A.1.a.iii": "1.A.1.a.iii",  # 1A1aiii_Public_Heat_Production
        "1.A.1.b": "1.A.1.b",  # 1A1b_Petroleum_Refining
        "1.A.1.c.i": "1.A.1.c.i",  # 1A1ci_Manufacture_of_solid_fuels
        "1.A.1.c.ii": "1.A.1.c.ii",  # 1A1cii_Oil_and_gas_extraction
        "1.A.1.c.iii": "1.A.1.c.iii",  # 1A1ciii_Other_energy_industries
        "1.A.2.a": "1.A.2.a",  # 1A2a_Iron_and_steel
        "1.A.2.b": "1.A.2.b",  # 1A2b_Non-Ferrous_Metals
        "1.A.2.c": "1.A.2.c",  # 1A2c_Chemicals
        "1.A.2.d": "1.A.2.d",  # 1A2d_Pulp_Paper_Print
        "1.A.2.e": "1.A.2.e",  # 1A2e_food_processing_beverages_and_tobacco
        "1.A.2.f": "1.A.2.f",  # 1A2f_Non-metallic_minerals
        "1.A.2.g.iii": "1.A.2.i",  # 1A2giii_Mining_and_quarrying
        "1.A.2.g.v": "1.A.2.k",  # 1A2gv_Construction
        "1.A.2.g.vii": "1.A.2.m.i",  # 1A2gvii_Off-road_vehicles_and_other_machinery
        "1.A.2.g.v.iii": "1.A.2.m.ii",  # 1A2gviii_Other_manufacturing_industries_and_construction
        "1.A.3.a": "1.A.3.a.ii",  # 1A3a_Domestic_aviation
        "1.A.3.b.i": "1.A.3.b.i",  # 1A3bi_Cars
        "1.A.3.b.ii": "1.A.3.b.ii",  # 1A3bii_Light_duty_trucks
        "1.A.3.b.iii": "1.A.3.b.iii",  # 1A3biii_Heavy_duty_trucks_and_buses
        "1.A.3.b.iv": "1.A.3.b.iv",  # 1A3biv_Motorcycles
        "1.A.3.b.v": "M.1.A.3.b.v",  # 1A3bv_Other_road_transport (no direct match in IPCC2006)
        "1.A.3.c": "1.A.3.c",  # 1A3c_Railways
        "1.A.3.d": "1.A.3.d.ii",  # 1A3d_Domestic_navigation
        "1.A.3.e.ii": "1.A.3.e.ii",  # 1A3eii_Other_Transportation (subsector consistent with CRF reporting)
        "1.A.4.a.i": "1.A.4.a.i",  # 1A4ai_Commercial/Institutional (stationary)
        "1.A.4.a.ii": "1.A.4.a.ii",  # 1A4aii_Commercial/Institutional_Mobile
        "1.A.4.b.i": "1.A.4.b.i",  # 1A4bi_Residential_stationary
        "1.A.4.b.ii": "1.A.4.b.ii",  # 1A4bii_Residential:Off-road
        "1.A.4.c.i": "1.A.4.c.i",  # 1A4ci_Agriculture/Forestry/Fishing:Stationary
        "1.A.4.c.ii": "1.A.4.c.ii",  # 1A4cii_Agriculture/Forestry/Fishing:Off-road
        "1.A.4.c.iii": "1.A.4.c.iii",  # 1A4ciii_Fishing
        "1.A.5.b": "1.A.5.b",  # 1A5b_Other:Mobile
        "1.B.1.a.i.1": "1.B.1.a.i.1",  # 1B1ai_Underground_mines:Mining_activities
        "1.B.1.a.i.2": "1.B.1.a.i.2",  # 1B1ai_Underground_mines:Post-mining_activities
        "1.B.1.a.i.3": "1.B.1.a.i.3",  # 1B1ai_Underground_mines:Abandoned
        "1.B.1.a.ii.1": "1.B.1.a.ii.1",  # 1B1aii_Surface_mines:Mining_activities
        "1.B.1.b": "1.B.1.c",  # 1B1b_Solid_Fuel_Transformation
        "1.B.2.a.1": "1.B.2.a.iii.1",  # 1B2a1_Oil_exploration
        "1.B.2.a.2": "1.B.2.a.iii.2",  # 1B2a2_Oil_Production
        "1.B.2.a.3": "1.B.2.a.iii.3",  # 1B2a3_Oil_transport
        "1.B.2.a.4": "1.B.2.a.iii.4",  # 1B2a4_Oil_refining/storage
        "1.B.2.a.6": "1.B.2.a.iii.6",  # 1B2a6_Oil_Production
        "1.B.2.b.1": "1.B.2.b.iii.1",  # 1B2b1_Gas_exploration
        "1.B.2.b.2": "1.B.2.b.iii.2",  # 1B2b2_Gas_production
        "1.B.2.b.3": "1.B.2.b.iii.3",  # 1B2b3_Gas_processing
        "1.B.2.b.4": "1.B.2.b.iii.4",  # 1B2b4_Gas_transmission_and_storage
        "1.B.2.b.5": "1.B.2.b.iii.5",  # 1B2b5_Gas_distribution
        "1.B.2.c-ven.i": "1.B.2.a.i",  # 1B2c_Venting_Oil
        "1.B.2.c-ven.ii": "1.B.2.b.i",  # 1B2c_Venting_Gas
        "1.B.2.c-fla.i": "1.B.2.a.ii",  # 1B2c_Flaring_Oil
        "1.B.2.c-fla.ii": "1.B.2.b.ii",  # 1B2c_Flaring_Gas
        "1.B.2.d": "1.B.3.b",  # 1B2d_Other_energy_industries
        "2.A.1": "2.A.1",  # 2A1_Cement_Production
        "2.A.2": "2.A.2",  # 2A2_Lime_Production
        "2.A.3": "2.A.3",  # 2A3_Glass_production
        "2.A.4.a": "2.A.4.a",  # 2A4a_Other_process_uses_of_carbonates:ceramics
        "2.A.4.b": "2.A.4.b",  # 2A4b_Other_uses_of_Soda_Ash
        "2.A.4.d": "2.A.4.d",  # 2A4d_Other_process_uses_of_carbonates:other
        "2.B.1": "2.B.1",  # 2B1_Chemical_Industry:Ammonia_production
        "2.B.10": "2.B.10",  # 2B10_Chemical_Industry:Other
        "2.B.2": "2.B.2",  # 2B2_Nitric_Acid_Production
        "2.B.3": "2.B.3",  # 2B3_Adipic_Acid_Production
        "2.B.6": "2.B.6",  # 2B6_Titanium_dioxide_production
        "2.B.7": "2.B.7",  # 2B7_Soda_Ash_Production
        "2.B.8.a": "2.B.8.a",  # 2B8a_Methanol_production
        "2.B.8.b": "2.B.8.b",  # 2B8b_Ethylene_Production
        "2.B.8.c": "2.B.8.c",  # 2B8c_Ethylene_Dichloride_and_Vinyl_Chloride_Monomer
        "2.B.8.d": "2.B.8.d",  # 2B8d_Ethylene_Oxide
        "2.B.8.e": "2.B.8.e",  # 2B8e_Acrylonitrile
        "2.B.8.f": "2.B.8.f",  # 2B8f_Carbon_black_production
        "2.B.8.g": "2.B.8.g",  # 2B8g_Petrochemical_and_carbon_black_production:Other
        "2.B.9.a.i": "2.B.9.a.i",  # 2B9a1_Fluorchemical_production:By-product_emissions
        "2.B.9.b.iii": "2.B.9.b.iii",  # 2B9b3_Fluorchemical_production:Fugitive_emissions
        "2.C.1.a": "2.C.1.a",  # 2C1a_Steel
        "2.C.1.b": "2.C.1.b",  # 2C1b_Pig_iron
        "2.C.1.d": "2.C.1.d",  # 2C1d_Sinter
        "2.C.3.a": "2.C.3.a",  # 2C3_Aluminium_Production
        "2.C.3.b": "2.C.3.b",  # 2C3_Aluminium_Production
        "2.C.4": "2.C.4",  # 2C4_Magnesium_production
        "2.C.6": "2.C.6",  # 2C6_Zinc_Production
        "2.D.1": "2.D.1",  # 2D1_Lubricant_Use
        "2.D.2": "2.D.2",  # 2D2 Non-energy_products_from_fuels_and_solvent_use:Paraffin_wax_use
        "2.D.3": "2.D.3",  # 2D3_Other_NEU
        "2.E.1": "2.E.1",  # 2E1_Integrated_circuit_or_semiconductor
        "2.F.1.a": "M.2.F.1.a.i",  # 2F1a_Commercial_refrigeration
        "2.F.1.b": "M.2.F.1.a.ii",  # 2F1b_Domestic_refrigeration
        "2.F.1.c": "M.2.F.1.a.iii",  # 2F1c_Industrial_refrigeration
        "2.F.1.d": "M.2.F.1.a.iv",  # 2F1d_Transport_refrigeration
        "2.F.1.e": "2.F.1.b",  # 2F1e_Mobile_air_conditioning
        "2.F.1.f": "M.2.F.1.a.v",  # 2F1f_Stationary_air_conditioning
        "2.F.2.a": "M.2.F.2.a",  # 2F2a_Closed_foam_blowing_agents (not in CRF2023_2023)
        "2.F.2.b": "M.2.F.2.b",  # 2F2b_Open_foam_blowing_agents (not in CRF2023_2023)
        "2.F.3": "2.F.3",  # 2F3_Fire_Protection
        "2.F.4.a": "M.2.F.4.a",  # 2F4a_Metered_dose_inhalers
        "2.F.4.b": "M.2.F.4.b",  # 2F4b_Aerosols:Other
        "2.F.5": "2.F.5",  # 2F5_Solvents
        "2.F.6.b": "2.F.6.b",  # 2F6b_Other_Applications:Contained-Refrigerant_containers
        "2.G.1": "2.G.1",  # 2G1_Electrical_equipment
        "2.G.2.a": "2.G.2.a",  # 2G2_Military_applications
        "2.G.2.b": "2.G.2.b",  # 2G2_Particle_accelerators
        "2.G.2.e": "M.2.G.2.c.i",  # 2G2e_Electronics_and_shoes
        "2.G.3.a": "2.G.3.a",  # 2G3a_Medical aplications
        "2.G.3.b": "2.G.3.c",  # 2G3b_N2O_from_product_uses:_Other
        "2.G.4": "2.G.4",  # 2G4_Other_product_manufacture_and_use
        "3.A.1.Aa": "3.A.1.a.i",  # 3A1a_Enteric_Fermentation_dairy_cattle
        "3.A.1.Ab": "3.A.1.a.ii",  # 3A1b_Enteric_Fermentation_non-dairy_cattle
        "3.A.2": "3.A.1.c",  # 3A2_Enteric_Fermentation_sheep
        "3.A.3": "3.A.1.h",  # 3A3_Enteric_Fermentation_swine
        "3.A.4": "3.A.1.j",  # 3A4_Enteric_Fermentation_other:deer
        "3.B.1.Aa": "3.A.2.a.i",  # 3B21a_Manure_Management_X_dairy_cattle
        "3.B.1.Ab": "3.A.2.a.ii",  # 3B21b_Manure_Management_X_non-dairy_cattle
        "3.B.2": "3.A.2.c",  # 3B22_Manure_Management_X_sheep
        "3.B.3": "3.A.2.h",  # 3B23_Manure_Management_X_swine
        "3.B.4": "3.A.2.i",  # 3B24_Manure_Management_X_other:poultry
        "3.B.5": "3.C.6",  # 3B25_Manure_Management_Indirect_Emissions_swine
        "3.D.a.1": "M.3.C.4.a.AG",  # 3D11_Agriculural_Soils_Inorganic_N_Fertilisers
        "3.D.a.2.a": "M.3.C.4.b.i.AG",  # 3D12a_Agricultural_Soils_Manure_Applied_to_Soils
        "3.D.a.2.b": "M.3.C.4.b.ii.AG",  # 3D12b_Agricultural_Soils_Sewage_Sludge_Applied_to_Soils
        "3.D.a.2.c": "M.3.C.4.b.iii.AG",  # 3D12c_Agricultural_Soils_Other_Organic_Fertilisers_Applied_to_Soils
        "3.D.a.3": "3.C.4.c",  # 3D13_Agricultural_Soils_Manure_Deposited_by_Grazing_Animals
        "3.D.a.4": "3.C.4.d",  # 3D14_Agriculural_Soils_Residues
        "3.D.a.5": "M.3.C.4.e.AG",  # 3D15_Agricultural_soils_Mineralization/Immobilization
        "3.D.a.6": "M.3.C.4.f.AG",  # 3D16_Agricultural_soils_Cultivation_of_Organic_Soils
        "3.D.b.1": "M.3.C.5.a.AG",  # 3D21_Agriculural_Soils_Indirect_Deposition
        "3.D.b.2": "M.3.C.5.b.AG",  # 3D22_Agriculural_Soils_Indirect_Leaching_and_Run-off
        "3.F.1.a": "M.3.C.1.b.i",  # 3F11_Field_burning_wheat
        "3.F.1.b": "M.3.C.1.b.ii",  # 3F12_Field_burning_barley
        "3.F.1.d": "M.3.C.1.b.iii",  # 3F14_Field_burning_other_cereals
        "3.F.5": "M.3.C.1.b.iv",  # 3F5_Field_burning_other_residues
        "3.G.1": "M.3.C.2.a",  # 3G1_Liming - limestone
        "3.G.2": "M.3.C.2.b",  # 3G2_Liming - dolomite
        "3.H": "M.3.C.3.AG",  # 3H_Urea application
        "4": "M.3.C.5.LU",  # 4_Indirect_N2O_Emissions (LULUCF)
        "4.A": "M.3.B.1.DR",  # 4A_Forest Land_Emissions_from_Drainage
        "4.A.1": "3.B.1.a",  # 4A1_ Forest Land remaining Forest Land
        "4.A.2": "3.B.1.b",  # 4A2_Cropland_converted_to_Forest_Land (and other land types)
        "4.B.1": "3.B.2.a",  # 4B1_Cropland Remaining Cropland
        "4.B.2": "3.B.2.b",  # 4B2_Forest_Land_converted_to_Cropland (and other land types)
        "4.C": "M.3.B.3.DR",  # 4C_Grassland_Emissions_from_Drainage
        "4.C.1": "3.B.3.a",  # 4C1_Grassland Remaining Grassland
        "4.C.2": "3.B.3.b",  # 4C2_Forest_Land_converted_to_Grassland (and other land types)
        "4.D": "M.3.B.4.DR",  # 4D_Wetlands_Emissions_from_Drainage
        "4.D.1": "3.B.4.a",  # 4D1_Wetlands remaining wetlands
        "4.D.2": "3.B.4.b",  # 4D2_Land_converted_to_Wetlands_Peat_Extraction
        "4.E": "M.3.B.5.DR",  # 4E_Settlements_Emissions_from_Drainage
        "4.E.1": "3.B.5.a",  # 4E1_Settlements remaining settlements
        "4.E.2": "3.B.5.b",  # 4E2_Forest_Land_converted_to_Settlements (and other land types)
        "4.G": "3.D.1",  # 4G_Harvested Wood Products
        "5.A.1.a": "M.4.A.1.a",  # 5A1a_Managed_Waste_Disposal_sites_anaerobic
        "5.B.1.a": "M.4.B.1.a",  # 5B1a_composting_municipal_solid_waste
        "5.B.2.a": "M.4.B.2.a",  # 5B2a_Anaerobic_digestion_municipal_solid_waste
        "5.C.1.a.ii.4": "M.4.C.1.a.ii.4",  # 5C1.1b_Biogenic:Sewage_sludge
        "5.C.1.b.i": "M.4.C.1.b.i",  # 5C1.2a_Non-biogenic:municipal_solid_waste
        "5.C.1.b.ii.3": "M.4.C.1.b.ii.3",  # 5C1.2b_Non-biogenic:Clinical_waste
        "5.C.2.a.ii.5": "M.4.C.2.a.ii.5",  # 5C2.1b_Biogenic:Other
        "5.C.2.b.ii.5": "M.4.C.2.b.ii.5",  # 5C2.2b_Non-biogenic:Other
        "5.D.1": "4.D.1",  # 5D1_Domestic_wastewater_treatment
        "5.D.2": "4.D.2",  # 5D2_Industrial_wastewater_treatment
        "Aviation_Bunkers": "M.BK.A",  # Aviation_Bunkers
        "Marine_Bunkers": "M.BK.B",  # Marine_Bunkers
    },
    "aggregate": {
        # need to aggregate the whole tree as only leaves are given in the data
        # 1
        ## 1.A
        "1.A.1.a": {"sources": ["1.A.1.a.i", "1.A.1.a.iii"]},
        "1.A.1.c": {"sources": ["1.A.1.c.i", "1.A.1.c.ii", "1.A.1.c.iii"]},
        "1.A.1": {"sources": ["1.A.1.a", "1.A.1.b", "1.A.1.c"]},
        "1.A.2.m": {"sources": ["1.A.2.m.i", "1.A.2.m.ii"]},
        "1.A.2": {
            "sources": [
                "1.A.2.a",
                "1.A.2.b",
                "1.A.2.c",
                "1.A.2.d",
                "1.A.2.e",
                "1.A.2.f",
                "1.A.2.i",
                "1.A.2.k",
                "1.A.2.m",
            ]
        },
        "1.A.3.a": {"sources": ["1.A.3.a.ii"]},
        "1.A.3.b": {
            "sources": [
                "1.A.3.b.i",
                "1.A.3.b.ii",
                "1.A.3.b.iii",
                "1.A.3.b.iv",
                "M.1.A.3.b.v",
            ]
        },
        "1.A.3.d": {"sources": ["1.A.3.d.ii"]},
        "1.A.3.e": {"sources": ["1.A.3.e.ii"]},
        "1.A.3": {"sources": ["1.A.3.a", "1.A.3.b", "1.A.3.c", "1.A.3.d", "1.A.3.e"]},
        "1.A.4.a": {"sources": ["1.A.4.a.i", "1.A.4.a.ii"]},
        "1.A.4.b": {"sources": ["1.A.4.b.i", "1.A.4.b.ii"]},
        "1.A.4.c": {"sources": ["1.A.4.c.i", "1.A.4.c.ii", "1.A.4.c.iii"]},
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"]},
        "1.A.5": {"sources": ["1.A.5.b"]},
        "1.A": {"sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"]},
        ## 1.B
        "1.B.1.a.i": {"sources": ["1.B.1.a.i.1", "1.B.1.a.i.2", "1.B.1.a.i.3"]},
        "1.B.1.a.ii": {"sources": ["1.B.1.a.ii.1"]},
        "1.B.1.a": {"sources": ["1.B.1.a.i", "1.B.1.a.ii"]},
        "1.B.1": {"sources": ["1.B.1.a", "1.B.1.c"]},
        "1.B.2.a.iii": {
            "sources": [
                "1.B.2.a.iii.1",
                "1.B.2.a.iii.2",
                "1.B.2.a.iii.3",
                "1.B.2.a.iii.4",
                "1.B.2.a.iii.6",
            ]
        },
        "1.B.2.a": {"sources": ["1.B.2.a.i", "1.B.2.a.ii", "1.B.2.a.iii"]},
        "1.B.2.b.iii": {
            "sources": [
                "1.B.2.b.iii.1",
                "1.B.2.b.iii.2",
                "1.B.2.b.iii.3",
                "1.B.2.b.iii.4",
                "1.B.2.b.iii.5",
            ]
        },
        "1.B.2.b": {"sources": ["1.B.2.b.i", "1.B.2.b.ii", "1.B.2.b.iii"]},
        "1.B.2": {"sources": ["1.B.2.a", "1.B.2.b"]},
        "1.B.3": {"sources": ["1.B.3.b"]},
        "1.B": {"sources": ["1.B.1", "1.B.2", "1.B.3"]},
        ## 1
        "1": {"sources": ["1.A", "1.B"]},
        # 2
        ## 2.A
        "2.A.4": {"sources": ["2.A.4.a", "2.A.4.b", "2.A.4.d"]},
        "2.A": {"sources": ["2.A.1", "2.A.2", "2.A.3", "2.A.4"]},
        ## 2.B
        "2.B.8": {
            "sources": [
                "2.B.8.a",
                "2.B.8.b",
                "2.B.8.c",
                "2.B.8.d",
                "2.B.8.e",
                "2.B.8.f",
                "2.B.8.g",
            ]
        },
        "2.B.9.a": {"sources": ["2.B.9.a.i"]},
        "2.B.9.b": {"sources": ["2.B.9.b.iii"]},
        "2.B.9": {"sources": ["2.B.9.a", "2.B.9.b"]},
        "2.B": {
            "sources": [
                "2.B.1",
                "2.B.2",
                "2.B.3",
                "2.B.6",
                "2.B.7",
                "2.B.8",
                "2.B.9",
                "2.B.10",
            ]
        },
        ## 2.C
        "2.C.1": {"sources": ["2.C.1.a", "2.C.1.b", "2.C.1.d"]},
        "2.C.3": {"sources": ["2.C.3.a", "2.C.3.b"]},
        "2.C": {"sources": ["2.C.1", "2.C.3", "2.C.4", "2.C.6"]},
        ## 2.D
        "2.D": {"sources": ["2.D.1", "2.D.2", "2.D.3"]},
        ## 2.E
        "2.E": {"sources": ["2.E.1"]},
        ## 2.F
        "2.F.1.a": {
            "sources": [
                "M.2.F.1.a.i",
                "M.2.F.1.a.ii",
                "M.2.F.1.a.iii",
                "M.2.F.1.a.iv",
                "M.2.F.1.a.v",
            ]
        },
        "2.F.1": {"sources": ["2.F.1.a", "2.F.1.b"]},
        "2.F.2": {"sources": ["M.2.F.2.a", "M.2.F.2.b"]},
        "2.F.4": {"sources": ["M.2.F.4.a", "M.2.F.4.b"]},
        "2.F.6": {"sources": ["2.F.6.b"]},
        "2.F": {"sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4", "2.F.5", "2.F.6"]},
        ## 2.G
        "2.G.2.c": {"sources": ["M.2.G.2.c.i"]},
        "2.G.2": {"sources": ["2.G.2.a", "2.G.2.b", "2.G.2.c"]},
        "2.G.3": {"sources": ["2.G.3.a", "2.G.3.c"]},
        "2.G": {"sources": ["2.G.1", "2.G.2", "2.G.3", "2.G.4"]},
        ## 2
        "2": {"sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G"]},
        # 3
        ## 3.A
        "3.A.1.a": {"sources": ["3.A.1.a.i", "3.A.1.a.ii"]},
        "3.A.1": {"sources": ["3.A.1.a", "3.A.1.c", "3.A.1.h", "3.A.1.j"]},
        "3.A.2.a": {"sources": ["3.A.2.a.i", "3.A.2.a.ii"]},
        "3.A.2": {"sources": ["3.A.2.a", "3.A.2.c", "3.A.2.h", "3.A.2.i"]},
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        ## 3.B
        "3.B.1": {"sources": ["3.B.1.a", "3.B.1.b", "M.3.B.1.DR"]},
        "3.B.2": {"sources": ["3.B.2.a", "3.B.2.b"]},
        "3.B.3": {"sources": ["3.B.3.a", "3.B.3.b", "M.3.B.3.DR"]},
        "3.B.4": {"sources": ["3.B.4.a", "3.B.4.b", "M.3.B.4.DR"]},
        "3.B.5": {"sources": ["3.B.5.a", "3.B.5.b", "M.3.B.5.DR"]},
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5"]},
        ## 3.C
        "3.C.1.b": {
            "sources": ["M.3.C.1.b.i", "M.3.C.1.b.ii", "M.3.C.1.b.iii", "M.3.C.1.b.iv"]
        },
        "3.C.1": {"sources": ["3.C.1.b"]},
        "M.3.C.1.AG": {"sources": ["3.C.1.b"]},
        "M.3.C.2.AG": {"sources": ["M.3.C.2.a.AG", "M.3.C.2.b.AG"]},
        "3.C.2": {"sources": ["M.3.C.2.AG"]},
        "3.C.3": {"sources": ["M.3.C.3.AG"]},
        "3.C.4.a": {"sources": ["M.3.C.4.a.AG"]},
        "M.3.C.4.b.AG": {
            "sources": ["M.3.C.4.b.i.AG", "M.3.C.4.b.ii.AG", "M.3.C.4.b.iii.AG"]
        },
        "3.C.4.b": {"sources": ["M.3.C.4.b.AG"]},
        "3.C.4.e": {"sources": ["M.3.C.4.e.AG"]},
        "3.C.4.f": {"sources": ["M.3.C.4.f.AG"]},
        "M.3.C.4.AG": {
            "sources": [
                "3.C.4.a.AG",
                "3.C.4.b.AG",
                "3.C.4.c",
                "3.C.4.d",
                "M.3.C.4.e.AG",
                "M.3.C.4.f.AG",
            ]
        },
        "3.C.4": {
            "sources": [
                "3.C.4.a",
                "3.C.4.b",
                "3.C.4.c",
                "3.C.4.d",
                "3.C.4.e",
                "3.C.4.f",
            ]
        },
        "M.3.C.5.AG": {"sources": ["M.3.C.5.a.AG", "M.3.C.5.b.AG"]},
        "3.C.5": {"sources": ["M.3.C.5.AG", "M.3.C.5.LU"]},
        "3.C": {"sources": ["3.C.1", "3.C.2", "3.C.3", "3.C.4", "3.C.5", "3.C.6"]},
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "M.3.C.2.AG",
                "M.3.C.3.AG",
                "M.3.C.4.AG",
                "M.3.C.5.AG",
                "3.C.6",
            ]
        },
        "M.3.C.LU": {"sources": ["M.3.C.5.LU"]},
        "M.3.D.LU": {"sources": ["3.D.1"]},
        # 3.D
        "3.D": {"sources": ["3.D.1"]},
        "M.AG.ELV": {"sources": ["M.3.C.AG"]},
        "3": {"sources": ["3.A", "3.B", "3.C", "3.D"]},
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},
        "M.LULUCF": {"sources": ["3.B", "M.3.C.LU", "M.3.D.LU"]},
        # 4
        "4.A.1": {"sources": ["M.4.A.1.a"]},
        "4.A": {"sources": ["4.A.1"]},
        "4.B.1": {"sources": ["M.4.B.1.a"]},
        "4.B.2": {"sources": ["M.4.B.2.a"]},
        "4.B": {"sources": ["4.B.1", "4.B.2"]},
        "4.C.1": {"sources": ["M.4.C.1.a.ii.4", "M.4.C.1.b.i", "M.4.C.1.b.ii.3"]},
        "4.C.2": {"sources": ["M.4.C.2.a.ii.5", "M.4.C.2.b.ii.5"]},
        "4.C": {"sources": ["4.C.1", "4.C.2"]},
        "4.D": {"sources": ["4.D.1", "4.D.2"]},
        "4": {"sources": ["4.A", "4.B", "4.C", "4.D"]},
        # top level and bunkers
        "0": {"sources": ["1", "2", "3", "4"]},
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
        "M.BK": {"sources": ["M.BK.A", "M.BK.B"]},
    },
}

basket_copy = {
    "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
    "entities": ["HFCS", "PFCS"],
    "source_GWP": gwp_to_use,
}

gas_baskets = {
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)", "PFCS (SARGWP100)", "SF6", "NF3"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)", "PFCS (AR4GWP100)", "SF6", "NF3"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)", "PFCS (AR5GWP100)", "SF6", "NF3"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)", "PFCS (AR6GWP100)", "SF6", "NF3"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
