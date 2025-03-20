import pandas as pd


# =========================================== #
# ================ Endpoints ================ #
# =========================================== #
def _list(PAGES=10):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-list?pages={PAGES}')


def raw(SLUG='microsoft'):
    return pd.read_json(f'http://project-finance-backend.onrender.com/financial-raw/{SLUG}')