from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_core import (
    get_info_from_crf_filename,
    get_latest_date_for_country,
)

# def test_get_submission_dates()
#     filter = {}
#
#     folder: Path,
# file_filter: dict[str, Union[str, int, list]],


def test_get_latest_date_for_country():
    # RUS CRF
    expected = "22082023"
    date = get_latest_date_for_country("RUS", 2023, type="CRF")
    assert date == expected

    # AUS CRT
    expected = "12042024"
    date = get_latest_date_for_country("AUS", 1, type="CRT")
    assert date == expected

    # RUS CRT
    expected = "20241108"
    date = get_latest_date_for_country("RUS", 1, type="CRT")
    assert date == expected


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
