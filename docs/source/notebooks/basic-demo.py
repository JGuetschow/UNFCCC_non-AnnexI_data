# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Basic demo
#
# This notebook gives a basic demonstration of how to use Country greenhouse gas data submitted to the UNFCCC.

# %%
from src import unfccc_ghg_data

# %%
print(f"You are using unfccc_ghg_data version {unfccc_ghg_data.__version__}")
