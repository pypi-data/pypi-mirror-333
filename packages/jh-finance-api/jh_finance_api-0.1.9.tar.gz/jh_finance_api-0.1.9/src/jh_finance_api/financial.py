import sys; sys.dont_write_bytecode=True
import pandas as pd


# =========================================== #
# ================ Endpoints ================ #
# =========================================== #
def _list(pages=10):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-list?pages={pages}')


def raw(slug='microsoft'):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-raw/{slug}')