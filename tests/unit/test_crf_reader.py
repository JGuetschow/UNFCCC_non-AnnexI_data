from pathlib import Path

from unfccc_ghg_data.helper import downloaded_data_path_UNFCCC
from unfccc_ghg_data.unfccc_crf_reader.unfccc_crf_reader_core import (
    filter_category,
    find_latest_version,
    get_country_folders,
    get_info_from_crf_filename,
    get_latest_date_for_country,
    get_latest_version_for_country,
)


def test_get_latest_date_for_country():
    # RUS CRF
    expected = "22082023"
    date = get_latest_date_for_country("RUS", 2023, submission_type="CRF")
    assert date == expected

    # AUS CRT
    expected = "12042024"
    date = get_latest_date_for_country("AUS", 1, submission_type="CRT")
    assert date == expected

    # RUS CRT
    expected = "20241220"
    date = get_latest_date_for_country("RUS", 1, submission_type="CRT")
    assert date == expected

    # AUT CRTAI
    expected = "20250414"
    date = get_latest_date_for_country(
        "AUT", submission_year=2025, submission_type="CRTAI"
    )
    assert date == expected


def test_get_latest_version_for_country():
    # AUS CRT
    expected = "V0.0"
    date = get_latest_version_for_country("AUS", 1)
    assert date == expected

    # RUS CRT
    expected = "V1.0"
    date = get_latest_version_for_country("RUS", 1)
    assert date == expected

    # AUT CRTAI
    expected = "V1.0"
    version = get_latest_version_for_country(
        "AUT", submission_round=2025, submission_type="CRTAI"
    )
    assert version == expected

    # TUR CRTAI
    expected = "V0.2"
    version = get_latest_version_for_country(
        "TUR", submission_round=2025, submission_type="CRTAI"
    )
    assert version == expected


def test_find_latest():
    test_list = ["V0.01", "V0.3", "V0.2"]
    expected = "V0.3"
    version = find_latest_version(test_list)

    assert version == expected


def test_get_info_from_crf_filename():
    # crf
    filename = "BLR_2021_1990_30032021_192048.xlsx"
    expected = {
        "party": "BLR",
        "submission_year": 2021,
        "data_year": 1990,
        "date": "30032021",
        "extra": "192048",
        "version": "V0.0",
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


def test_filter_category():
    # general
    map_gen = [["Option C (country-specific):"], ["\\IGNORE"], 4]
    assert filter_category(map_gen, "MOZ") == map_gen

    # country specific
    expected = [
        ["Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    expected_remove = [["\\REMOVE"], ["3.A.1.C"], 5]
    # exclude multiple
    map_excl_multiple = [
        ["\\C!-AUS-MLT-LUX-POL-SVN-USA\\ Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    assert filter_category(map_excl_multiple, "MOZ") == expected
    assert filter_category(map_excl_multiple, "MLT") == expected_remove

    # exclude single
    map_excl_single = [
        ["\\C!-AUS\\ Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    expected = [
        ["Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    expected_remove = [["\\REMOVE"], ["3.A.1.C"], 5]
    assert filter_category(map_excl_single, "MOZ") == expected
    assert filter_category(map_excl_single, "AUS") == expected_remove

    # include multiple
    map_incl_multiple = [
        ["\\C-AUS-NLD\\ Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    assert filter_category(map_incl_multiple, "MOZ") == expected_remove
    assert filter_category(map_incl_multiple, "AUS") == expected
    assert filter_category(map_incl_multiple, "NLD") == expected

    # include single
    map_incl_single = [
        ["\\C-AUS\\ Other (as specified in table 3(I).A)"],
        ["3.A.1.C"],
        5,
    ]
    assert filter_category(map_incl_single, "MOZ") == expected_remove
    assert filter_category(map_incl_single, "AUS") == expected

    # multiple items
    map_incl_mult_items = [
        [
            "\\C-AUS\\ Other (as specified in table 3(I).A)",
            "\\C-NLD\\ Other (as specified in table 3(I).A)",
        ],
        ["3.A.1.C"],
        5,
    ]
    assert filter_category(map_incl_mult_items, "MOZ") == expected_remove
    assert filter_category(map_incl_mult_items, "AUS") == expected


def test_get_country_folders():
    # BTR1
    expected = [
        Path("Russian_Federation/BTR1"),
        Path("Australia/BTR1"),
        Path("Guyana/BTR1"),
    ]
    folders = get_country_folders(
        country_codes=["RUS", "AUS", "GUY"],
        submission_year=1,
        submission_type="CRT",
    )
    folders = [folder.relative_to(downloaded_data_path_UNFCCC) for folder in folders]
    assert expected == folders

    # CRF 2023
    expected = [
        Path("Russian_Federation/CRF2023"),
        Path("Australia/CRF2023"),
        Path("Germany/CRF2023"),
    ]
    folders = get_country_folders(
        country_codes=["RUS", "AUS", "DEU"],
        submission_year=2023,
        submission_type="CRF",
    )
    folders = [folder.relative_to(downloaded_data_path_UNFCCC) for folder in folders]
    assert expected == folders

    # CRTAI 2025
    expected = [
        Path("Russian_Federation/CRT2025"),
        Path("Australia/CRT2025"),
        Path("Germany/CRT2025"),
    ]
    folders = get_country_folders(
        country_codes=["RUS", "AUS", "DEU"],
        submission_year=2025,
        submission_type="CRTAI",
    )
    folders = [folder.relative_to(downloaded_data_path_UNFCCC) for folder in folders]
    assert expected == folders
