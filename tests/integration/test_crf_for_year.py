from timeit import default_timer as timer

from src.unfccc_ghg_data.unfccc_crf_reader.crf_raw_for_year_sparse_arrays import (
    crf_raw_for_year_original_version,
    crf_raw_for_year_pandas,
    crf_raw_for_year_sparse_arrays,
)


def test_crf_for_year_original_version(tmp_path):
    start = timer()
    n_countries = 3
    crf_raw_for_year_original_version(
        submission_year=2023,
        submission_type="CRF",
        n_countries=n_countries,
        output_folder=tmp_path,
    )
    end = timer()
    print(f"Processing time: {end - start} seconds for {n_countries} countries")


# Processing time: 9.024652959080413 seconds for 3 countries
# Processing time: 93.27503691602033 seconds for 10 countries


def test_crf_for_year_sparse_arrays(tmp_path):
    start = timer()
    n_countries = 20 # 100 will find 26 countries
    crf_raw_for_year_sparse_arrays(
        submission_year=1,
        submission_type="CRT",
        n_countries=n_countries,
        output_folder=tmp_path,
    )

    end = timer()
    print(f"Processing time: {end - start} seconds for {n_countries} countries")


# Processing time: 34.15730241697747 seconds for 3 countries


def test_crf_for_year_pandas(tmp_path):
    start = timer()
    n_countries = 3
    crf_raw_for_year_pandas(
        submission_year=2023,
        type="CRF",
        n_countries=n_countries,
        output_folder=tmp_path,
    )

    end = timer()
    print(f"Processing time: {end - start} seconds for {n_countries} countries")
