"""
Read Saint Kitts and Nevis' BUR1 from pdf
"""
import camelot
import pandas as pd

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path
from unfccc_ghg_data.unfccc_reader.Saint_Kitts_and_Nevis.config_kna_bur1 import conf

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Saint_Kitts_and_Nevis" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Saint_Kitts_and_Nevis"
    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "First_BUR_St.Kitts_Nevis.pdf"
    output_filename = "KNA_BUR1_2023_"
    compression = dict(zlib=True, complevel=9)

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # 1. Read in main tables
    # ###

    df_main = None
    for sector in conf.keys():
        print("-" * 45)
        print(f"Reading table for {sector}.")

        df_sector = None
        for page in conf[sector]["page_defs"].keys():
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                flavor="lattice",
                # split_text=True,
            )

            df_page = tables_inventory_original[0].df

            if df_sector is None:
                df_sector = df_page
            else:
                df_sector = pd.concat(
                    [
                        df_sector,
                        df_page,
                    ],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

        pass
