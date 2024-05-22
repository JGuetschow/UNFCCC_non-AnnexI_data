"""
Read the inventory underlying Argentina's BUR5 from csv.

This script reads data from Argentina's 2023 national inventory which is underlying BUR5

Data are read from the csv file available for download under the URL
https://ciam.ambiente.gob.ar/repositorio.php?tid=9&stid=36&did=394#

license probably CC-BY 4.0
(see https://datos.gob.ar/dataset/ambiente-emisiones-gases-efecto-invernadero-gei)

*Further information*
* Data are in long format. Columns needed are
'año' 'id_ipcc' 'tipo_de_gas' 'valor_en_toneladas_de_gas'
* columns to irgnore are
columns_to_ignore = ['sector', 'actividad', 'subactividad', 'categoria',
'valor_en_toneladas_de_co2e']
* sector codes are in primap1 format (no dots), reading should be possible
directly from CSV into interchange format
* postprocessing needed is aggregation of gas baskets and categories as only
the highest detail categories are present

"""

import pandas as pd
import primap2 as pm2
from config_arg_bur5 import (
    cats_to_agg,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_filling,
    coords_value_mapping,
    filter_keep,
    filter_remove,
    meta_data,
    time_format,
    unit,
)

from unfccc_ghg_data.helper import (
    compression,
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    # folders and files
    input_folder = downloaded_data_path / "UNFCCC" / "Argentina" / "BUR5"
    output_folder = extracted_data_path / "UNFCCC" / "Argentina"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "ARG_BUR5_2023_"

    csv_file = "emisiones_gei_inventario_datos_totales_1990_2020.csv"

    # read the data
    data_pd = pd.read_csv(
        input_folder / csv_file,
        sep=";",
        parse_dates=[coords_cols["time"]],
        usecols=list(coords_cols.values()),
    )

    data_pd["unit"] = unit
    coords_cols["unit"] = "unit"

    data_if = pm2.pm2io.convert_long_dataframe_if(
        data_pd,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_value_mapping=coords_value_mapping,
        coords_value_filling=coords_value_filling,
        coords_terminologies=coords_terminologies,
        filter_remove=filter_remove,
        filter_keep=filter_keep,
        meta_data=meta_data,
        time_format=time_format,
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)
    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw" + ".nc"),
        encoding=encoding,
    )

    ### processing
    data_proc_pm2 = data_pm2

    # actual processing
    country_processing = {
        "aggregate_cats": cats_to_agg,
    }
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing,
    )

    # adapt source and metadata
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)
    data_proc_pm2 = data_proc_pm2.pr.loc[{"source": ["BUR_NIR"]}]

    # ###
    # save data to IF and native format
    # ###
    data_proc_if = data_proc_pm2.pr.to_interchange_format()
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]),
        data_proc_if,
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )
