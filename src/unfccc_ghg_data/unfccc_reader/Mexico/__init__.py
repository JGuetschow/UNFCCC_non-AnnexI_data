"""Read Mexico's BURs, NIRs, NCs

Scripts and configurations to read Mexico's submissions to the UNFCCC.
Currently, the following submissions and datasets are available (all datasets
including DI (red using the DI-reader) and legacy BUR/NIR (no code)):

.. exec_code::
    :hide:

    from unfccc_ghg_data.helper.functions import (get_country_datasets,
                                                  get_country_submissions)
    country = 'MEX'
    # print available submissions
    print("="*15 + " Available submissions " + "="*15)
    get_country_submissions(country, True)
    print("")

    #print available datasets
    print("="*15 + " Available datasets " + "="*15)
    get_country_datasets(country, True)

You can also obtain this information running

.. code-block:: bash

    poetry run doit country_info country=MEX

See below for a listing of scripts for BUR/NIR reading including links.

"""
