# Data reading FAQ

## How to choose which tables to read from a PDF?

## What's behind `gwp_to_use`?

## How do I know what's the correct GWP (`gwp_to_use`) for a report?

The report should mention which GWP conversion was used. Search for `gwp` in the report.

## How to choose the tolerance when merging datasets?

Should be at 0.1. The idea is to separate rounding error from actual inconsistencies in the data.

## How to deal with inconsistencies in a data source?

It is possible that a data source contains conflicting pieces of information. Sometimes it is obvious that one of the
values was wrongly added to the data. In other cases, it is impossible which value is more trustworthy. In that case it
is better to leave it out completely.

Sometimes the reports hold incorrect values, which become obvious when trying to merge tables, for example the main
table's value for 1.A.2 for CO2 is 0.003 and the sector table's value for 1.A.2 and CO2 is 0.006.
Johannes: As A rule I would say: If it's rounding errors use `pr.merge` and tolerance. If the data is actually wrong
either correct manually if we know the correct value or set to `nan` manually if we don't know the correct value.

## How to aggregate categories

The aggregation of categories means combining existing categories from the source, for example the PDF document, into a
new category and adding up their values. Some categories help to interpret the data, but are rarely included in the
reports. For example, it can be helpful to show all emissions without the mostly negative emissions from the LULUCF
sector in one category. For this we use `M.0.EL` - National total emissions excluding LULUCF. There is a set of
categories that must be present in primap-hist (where can I look it up?)

It is not immediately obvious which categories need to be aggregated. In principle, there should be a parent category
for each category. For example, if category 3.A.1 has been imported, category 3.A should also be present in the final
data set. The parent categories are often already contained in the tables in the PDFs. In addition, the following extra
categories should also be created, if not already in the report:

* `0` - National total emissions
* `M.0.EL` - National total emissions excluding LULUCF
* `M.LULUCF` - LULUCF
* `M.3.D.LU` - Other (LULUCF)
* `M.AG` - Agriculture
* `M.AG.ELV` - Agriculture excluding livestock
* `M.3.C.AG` - Aggregate sources and non-CO2 emissions sources on land
* `M.3.D.AG` - Other (Agriculture)

To aggregate the categories, we use the `process_data_for_country` function. The parameter `processing_info_country`
defines the categories and their subcategories to be aggregated. The following example shows all additional categories
and their subcategories. Another place to look up the additional categories (the ones that start with M) and their
children-categories is ???. The parameter can be passed into the function in this format.

```python
country_processing_step1 = {
    "aggregate_cats" : {
        "M.3.C.AG" : {
            "sources" : [
                "3.C.1",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
                "3.C.8",
            ],
        }
        "M.3.D.AG" : {
            "sources" : [
                "3.D.2"
            ],
            "M.AG.ELV" : {
                "sources" : [
                    "M.3.C.AG",
                    "M.3.D.AG"
                ],
            },
            "M.AG" : {
                "sources" : [
                    "3.A",
                    "M.AG.ELV"
                ]
            },
            "M.3.D.LU" : {
                "sources" : [
                    "3.D.1"
                ]
            },
            "M.LULUCF" : {
                "sources" : [
                    "3.B",
                    "M.3.D.LU"
                ],
            },
            "M.0.EL" : {
                "sources" : [
                    "1",
                    "2",
                    "M.AG",
                    "4"
                ],
            },
        },
    }
```

We can use the concept of aggregation not only to create new categories, but also to perform **consistency checks**. We
know that the sum of categories `1`, `2`, `3` and `4` must equal the value of category `0`. If the category is already
contained in the data and we nevertheless aggregate a new category `0` from the subcategories, the original category `0`
and the aggregated category `0` are merged. However, this only works if the difference of the values does not exceed a
certain tolerance. We take 1% as the default value for the rounding error. This step can be incorporated into the
function as follows:

```python
country_processing_step1 = {
    "aggregate_cats" : {
        "0" : {
            "sources" : [
                "1",
                "2",
                "3",
                "4"
            ]
        },
        "3" : {
            "sources" : [
                "M.AG",
                "M.LULUCF"
            ],
        },
    },
}
```

Note that all the specified sources must be either already present in the dataset or aggregated in the same function
call.

## How to downscale values in the dataset
To generate as comprehensive a data set as possible, it may be worth interpolating or extrapolating values.

**Example**

The category `1.B` for `CH4` holds the following values

| entity | category (IPCC2006_PRIMAP) | 1990 | 1995 | 2000 | 2005 | 2010  | 2015 | 2020 |
| ------ | -------------------------- | ---- | ---- | ---- | ---- | ----- | ---- | ---- |
| CH4    | 1.B                        | 6.23 | 4.37 | 4.83 | 7.48 | 32.33 | 61.0 | 52.2 |

However the children categories `1.B.1` and `1.B.2`come in a lower temporal resolution


| entity | category (IPCC2006_PRIMAP) | 1990 | 1995 | 2000 | 2005 | 2010 | 2015 | 2020  |
| ------ | -------------------------- | ---- | ---- | ---- | ---- | ---- | ---- | ----- |
| CH4    | 1.B.1                      | 6.23 |      |      |      |      |      | 32.99 |
| CH4    | 1.B.2                      | 0    |      |      |      |      |      | 19.51 |

In the year 1990 100% of the emissions from `1.B` come from `1.B.1`. This ratio changed in 2020.

With `downcaling`we can now interpolate the ratio of `1.B.1`and `1.B.2`for the years 1995 to 2015 and divide the values from `1.B`accordingly.

The final result will look like this. Note that the calculation results in numbers with many decimal places. For the sake of simplicity, everything after the second decimal place has been cut off in this illustration.

| entity | category (IPCC2006_PRIMAP) | 1990 | 1995 | 2000 | 2005 | 2010  | 2015  | 2020  |
| ------ | -------------------------- | ---- | ---- | ---- | ---- | ----- | ----- | ----- |
| CH4    | 1.B                        | 6.23 | 4.37 | 4.83 | 7.48 | 32.33 | 61.0  | 52.2  |
| CH4    | 1.B.1                      | 6.23 | 4.09 | 4.23 | 6.09 | 24.32 | 42.10 | 32.99 |
| CH4    | 1.B.2                      | 0    | 0.27 | 0.59 | 1.38 | 8.00  | 18.89 | 19.51 |

There are also situations in which we have to limit the years for the downscaling.

The downscaling is described in the [Primap2 documentation.](https://primap2.readthedocs.io/en/stable/special_usage.html#Downscaling)