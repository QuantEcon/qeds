"""
Construct simulated versions of shopify order history datasets
"""
from itertools import chain
import random
import pandas as pd
import numpy as np
from .util import random_dates

_n_orders_per_cust_dist = np.array([
    5.50529075e-01, 1.77840915e-01, 8.93340883e-02, 5.35855351e-02,
    3.42330369e-02, 2.31633265e-02, 1.73860566e-02, 1.23411166e-02,
    9.28296078e-03, 6.82151830e-03, 5.29244039e-03, 3.87524623e-03,
    3.00390915e-03, 2.46822332e-03, 1.84099624e-03, 1.55281082e-03,
    1.25106374e-03, 1.04424833e-03, 8.06919162e-04, 6.71302496e-04,
    5.83151664e-04, 4.67877497e-04, 3.45822498e-04, 3.45822498e-04,
    2.23767499e-04, 2.20377082e-04, 1.69520832e-04, 1.72911249e-04,
    1.28835833e-04, 1.28835833e-04, 8.47604162e-05, 7.79795829e-05,
    9.49316662e-05, 5.42466664e-05, 7.11987496e-05, 5.42466664e-05,
    6.10274997e-05, 4.06849998e-05, 2.37329165e-05, 2.71233332e-05,
    2.71233332e-05, 2.71233332e-05, 2.03424999e-05, 1.69520832e-05,
    2.03424999e-05, 1.69520832e-05, 3.39041665e-05, 1.35616666e-05,
    6.78083330e-06, 1.69520832e-05, 6.78083330e-06, 6.78083330e-06,
    1.01712499e-05, 6.78083330e-06, 6.78083330e-06, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    3.39041665e-06, 0.00000000e+00, 6.78083330e-06, 3.39041665e-06,
    0.00000000e+00, 0.00000000e+00, 3.39041665e-06, 0.00000000e+00,
    3.39041665e-06, 0.00000000e+00, 3.39041665e-06, 0.00000000e+00,
    3.39041665e-06, 0.00000000e+00, 3.39041665e-06, 0.00000000e+00,
    3.39041665e-06, 3.39041665e-06, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 3.39041665e-06, 0.00000000e+00,
    0.00000000e+00, 3.39041665e-06, 0.00000000e+00, 0.00000000e+00,
    3.39041665e-06, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 3.39041665e-06, 0.00000000e+00, 3.39041665e-06,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 3.39041665e-06, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 3.39041665e-06
])
_order_dist_size = _n_orders_per_cust_dist.size

_n_orders_per_row_dist = np.array([
    9.78999910e-01, 1.36144247e-02, 1.20596195e-03, 3.44755224e-04,
    1.47168238e-04, 8.72108076e-05, 4.08800661e-05, 2.45280396e-05,
    2.18027019e-05, 6.81334434e-06, 6.81334434e-06, 1.09013509e-05,
    4.08800661e-06, 2.72533774e-06, 2.72533774e-06, 1.36266887e-06,
    1.36266887e-06, 0.00000000e+00, 1.36266887e-06, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 1.36266887e-06, 0.00000000e+00, 1.36266887e-06,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
    1.36266887e-06
])


def simulate_orders(N=700_000, start_date="2014-01-01", end_date=None):
    """
    Parameters
    ----------
    N: int, optional(default=700_000)
        The target number of observations. The actual number of observations
        will be very close to this number

    start_date, end_date: optional(default=2014 to today)
        The starting and ending dates for the dataset


    Returns
    -------
    df: pandas.DataFrame
        A pandas DataFrame containing a simulated dataset
    """

    # NOTE: this is stuff that _must_ hold in the data set...
    # total_sales = (Gross_sales + Tax + Discounts + Returns + Shipping)
    # Net_sales = (Gross_sales + Discounts + Returns)
    # Net_quantity = (Ordered_quantity + Returned_quantity)

    # to be used later...
    quantiles = np.array([0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8,
                          0.9, 0.95, 0.99])

    if end_date is None:
        end_date = pd.datetime.now().strftime("%Y-%m-%d")

    # ------- Customer ID
    # bisect to find correct number of customers
    def obj(n_cust):
        np.random.seed(42)
        cust_orders = np.random.multinomial(n_cust, _n_orders_per_cust_dist)
        order_dist_range = range(1, _order_dist_size+1)
        orders = sum(n*i for (n, i) in zip(order_dist_range, cust_orders))
        return orders - N

    a = 1
    b = N
    mid = (a + b) >> 1
    fa = obj(a)

    while True:
        mid = (a + b) >> 1
        if abs(a - mid) <= 1:
            mid = a
            break
        if abs(b - mid) <= 1:
            mid = b
            break

        fmid = obj(mid)
        if abs(fmid) < 10:
            break

        if fmid * fa > 0:
            a = mid
            fa = fmid
        else:
            b = mid

    cust_counts = np.random.multinomial(mid, _n_orders_per_cust_dist)
    cutoffs = np.concatenate(([0], cust_counts.cumsum()))
    unique_cust_ids = np.random.randint(
        100000000, 9999999999, cust_counts.sum())
    cust_id_index = list(chain(*[
        np.repeat(range(cutoffs[i], cutoffs[i+1]), i+1)
        for i in range(cust_counts.size)
    ]))
    customer_id = unique_cust_ids[cust_id_index]
    out = pd.DataFrame(
        {"Customer ID": customer_id}
    )

    # ------- Day
    real_N = out.shape[0]
    out["Day"] = pd.Series(
        random_dates(start_date, end_date, real_N)
    ).sort_values().values

    # ------- customer_type
    # Let's say 0.5% of customers don't have a First-Time entry
    def _ctype(n_orders):
        return [0 if random.random() > 0.005 else 1] + [1] * (n_orders-1)

    customer_type_ind = list(chain(*[
        chain(*[_ctype(n_orders_m + 1) for _ in range(n_cust)])
        for (n_orders_m, n_cust) in enumerate(cust_counts)
    ]))

    ctypes = np.array(["First-time", "Returning"])
    out["customer_type"] = ctypes[customer_type_ind]

    # ------- orders
    orders_counts = np.random.multinomial(real_N, _n_orders_per_row_dist)
    orders = np.array(
        list(chain(*[[i+1]*n for (i, n) in enumerate(orders_counts)]))
    )
    np.random.shuffle(orders)
    out["orders"] = orders

    # ------- Ordered quantity
    quantity_per_order_qs = np.array([1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 8, 11, 18])
    out["Ordered quantity"] = np.round(np.interp(
        np.random.rand(real_N),
        quantiles,
        quantity_per_order_qs
    )) * out["orders"]
    out["Ordered quantity"] = out["Ordered quantity"].astype(int)

    # ------- Gross sales: float (always non-negative)
    price_per_item_qs = np.array([0.0, 4.95, 6.95, 8.95, 11.95, 15.95, 20.95,
                                  23.95, 31.95, 33.95, 50.95, 62.95, 144.95])
    price_per_item = np.interp(
        np.random.rand(real_N),
        quantiles,
        price_per_item_qs
    )
    out["Gross sales"] = price_per_item * out["Ordered quantity"]

    # ------- Discounts: float (negative)
    discounted = np.random.rand(real_N) < 0.121639
    non_neg_discount_qs = np.array([
        -5.74646e+01, -3.01200e+01, -2.34160e+01, -1.47720e+01, -1.03400e+01,
        -7.76000e+00, -5.81000e+00, -5.00000e+00, -3.99000e+00, -2.99000e+00,
        -1.89000e+00, -1.09000e+00, -1.00000e-02
    ])
    out["Discounts"] = np.interp(
        np.random.rand(real_N),
        quantiles,
        non_neg_discount_qs
    ) * discounted

    # ------- Tax: float (positive for sales, negative for returns)
    tax_rate_qs = np.array([
        12.39583333, 12.50896809, 12.9095838, 13.31521739, 13.32923833,
        13.33787466, 13.35106383, 13.76923077, 13.79003559, 13.80769231,
        14.82717649, 16.42160934, 23.09853488
     ])
    taxed = np.random.rand(real_N) < 0.087235
    out["Tax"] = np.interp(
        np.random.rand(real_N),
        quantiles,
        tax_rate_qs
    ) * out["Gross sales"] * taxed / 100

    # ------- Shipping: float
    shipping = np.random.rand(real_N) < 0.1602846
    non_zero_shipping_per_order_qs = np.array(
        [2.95, 2.95, 2.95, 5.99, 5.99, 5.99, 7.95, 7.99, 7.99, 7.99, 12.95,
         19.99, 45.99]
     )
    out["Shipping"] = np.interp(
        np.random.rand(real_N),
        quantiles,
        non_zero_shipping_per_order_qs
    ) * shipping

    # ------- Returns
    # we will treat returns differently, decide which rows correspond to
    # returns here
    returns_indicator = np.random.rand(real_N) < 0.011875
    out.loc[returns_indicator, ["Gross sales", "Ordered quantity"]] = 0

    # ------- Returned quantity:  int (negative)
    out["Returned quantity"] = np.round(np.interp(
        np.random.rand(real_N),
        quantiles,
        quantity_per_order_qs
    )) * returns_indicator * out["orders"]
    out["Returned quantity"] = out["Returned quantity"].astype(int)
    out["Returns"] = -price_per_item * out["Returned quantity"]

    out["total_sales"] = (
        out["Gross sales"] + out["Tax"] + out["Discounts"] + out["Returns"] +
        out["Shipping"]
    )
    out["Net sales"] = (
        out["Gross sales"] + out["Discounts"] + out["Returns"]
    )
    out["Net quantity"] = out["Ordered quantity"] + out["Returned quantity"]

    # now fix up the order of columns and content of Day column and
    # precision of floats
    out["Day"] = out["Day"].dt.strftime("%Y-%m-%d")
    col_order = ['Day',
                 'customer_type',
                 'Customer ID',
                 'orders',
                 'total_sales',
                 'Returns',
                 'Ordered quantity',
                 'Gross sales',
                 'Net sales',
                 'Shipping',
                 'Tax',
                 'Net quantity',
                 'Returned quantity',
                 'Discounts']

    for col in ["total_sales", "Returns", "Gross sales", "Net sales",
                "Shipping", "Tax", "Discounts"]:
        out[col] = out[col].round(2)

    locs = np.copy(out.index.values)
    np.random.shuffle(locs)
    return out.loc[locs, col_order].reset_index(drop=True)
