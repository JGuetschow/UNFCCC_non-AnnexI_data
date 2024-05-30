"""
Read data from China's BUR3.

Data are read from pdf. The file contains a detailed inventory for 2018 and
recalculated 2005 data for the main sectors and gases.

Inventories for mainland China (CHN), Hong Kong (HKG) and Macau (MAC) are reported in
individual inventories.
"""


import camelot
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
)
from unfccc_ghg_data.unfccc_reader.China.config_chn_bur3_nc4 import (
    config_bur3,
    coords_value_mapping,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "China" / "BUR3"
    output_folder = extracted_data_path / "UNFCCC" / "China"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "CHN_BUR3_"
    inventory_file = "China_BUR3_English.pdf"

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # read the tables from pdf
    # ###

    for table_group in config_bur3["table_groups"].keys():
        current_group = config_bur3["table_groups"][table_group]
        for country in current_group["pages"].keys():
            for page in current_group["pages"][country]:
                print(f"Reading {country}, {table_group}, page {page}")
                page_str = str(page)
                page_def = config_bur3["page_def"][page_str]
                if "rows_to_fix" in page_def:
                    rows_to_fix = page_def.pop("rows_to_fix")
                else:
                    rows_to_fix = {}
                tables_read = camelot.read_pdf(
                    str(input_folder / inventory_file), pages=page_str, **page_def
                )
                table_df = tables_read[0].df
                # fix split rows
                if rows_to_fix:
                    for n_rows in rows_to_fix.keys():
                        table_df = fix_rows(table_df, rows_to_fix[n_rows], 0, n_rows)
                # remove unwanted characters
                table_df[0] = table_df[0].str.replace("\n", " ")
                table_df[0] = table_df[0].str.replace("⎯ ", "")
                table_df[0] = table_df[0].str.replace("♦", "")
                table_df = pm2.pm2io.nir_add_unit_information(
                    table_df,
                    unit_row=0,
                    entity_row=0,
                    regexp_entity=".*",
                    default_unit=current_group["unit"],
                )
                table_df = table_df.set_index(table_df.columns[0])
                table_long = pm2.pm2io.nir_convert_df_to_long(
                    table_df,
                    year=current_group["year"],
                    header_long=["category", "entity", "unit", "time", "data"],
                )
                table_long["entity"] = table_long["entity"].str.strip()

    print(sorted(list(set(coords_value_mapping["category"].values()))))
