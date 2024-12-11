from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_core import (
    get_info_from_crf_filename,
)


def test_get_info_from_crf_filename():
    # crf
    filename = "BLR_2021_1990_30032021_192048.xlsx"
    expected = {
        "party": "BLR",
        "submission_year": 2021,
        "data_year": 1990,
        "date": "30032021",
        "extra": "192048",
    }
    assert expected == get_info_from_crf_filename(filename)

    # crt
    filename = "GUY-CRT-2024-V0.3-1992-20240927-191031_started.xlsx"
    expected = {
        "party": "GUY",
        "submission_year": 2024,
        "data_year": 1992,
        "date": "20240927",
        "extra": "191031_started",
        "version": "V0.3",
    }
    assert expected == get_info_from_crf_filename(filename)
