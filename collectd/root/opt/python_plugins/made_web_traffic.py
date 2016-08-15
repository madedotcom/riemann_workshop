import collectd
from numpy.random import poisson, normal, choice
from collections import Counter, defaultdict, namedtuple

"""
This collectd plugin provides a crappy model of a busy-ish e-commerce site
that attracts around 200k sessions a day, with a 0.5% conversion rate.

To do that, they display around 1M web pages, and around 10 assets per-page.

Every web response and attempted sale might fail for a number of reasons.

The site has 4 different means of payment.

The probabilities for those things are all enumerated below.
"""

payment_provider = namedtuple('pp',
                    ['id',
                     'popularity',
                     'user_error_rate',
                     'error_rate',
                     'fraud_rate'])

# This is the interval on which collectd calls us, used to extrapolate
# the per-second event rates.
interval = 10


# These weights define the likelihood of non 200 responses.
# Some of these are because of the usual bugs, or stale links on the internets
# some of them are script kiddies.

wt_500 = 0.001
wt_400 = 0.006
wt_200 = (1 - wt_500 - wt_400)

# This is the distribution of page response times in milliseconds.
page_latency_mean = 150
page_latency_stddev = 50

# This is the likelihood of 404s on images etc.
asset_500_wt = 0.00012
asset_400_wt = 0.008
asset_200_wt = (1 - asset_400_wt - asset_500_wt)

# This is the distribution of asset response times in milliseconds
asset_latency_mean = 10
asset_latency_stddev = 1

# These are the event rates

page_hits_per_sec = 11.5
asset_hits_per_sec = 100
new_users_per_sec = 2.4
sales_per_sec = 100 #0.012

# code, popularity, user error probability, provider failure rate, fraud rate
providers = {
    'a': payment_provider('a', 0.4, 0.01, 0.001, 0.3),
    'b': payment_provider('b', 0.3, 0.01, 0.001, 0.003),
    'c': payment_provider('c', 0.1, 0.01, 0.001, 0.003),
    'd': payment_provider('d', 0.2, 0.01, 0.001, 0.003)
}

def get_page_latency():
    return normal(page_latency_mean, page_latency_stddev, 1)[0]

def get_asset_latency():
    return normal(asset_latency_mean, asset_latency_stddev, 1)[0]

def get_event_count(rate):
    return sum(poisson(rate, interval))

def get_outcomes(count, outcomes, weights):
    return Counter(choice(outcomes, count, p=weights))

def send_gauge(name, val):
    collectd.Values(plugin="ecommerce",
                    type="gauge",
                    type_instance=name,
                    values=[val]).dispatch()

ctr_vals = defaultdict(int)

def send_counter(name, val):
    ctr_vals[name] += val
    collectd.Values(plugin="ecommerce",
                    type="counter",
                    type_instance=name,
                    values=[ctr_vals[name]]).dispatch()

def calculate_payment_results(count, provider):
    success_rate = 1 - (provider.user_error_rate
                        + provider.error_rate
                        + provider.fraud_rate)
    return get_outcomes(count,
        ["success", "user_error", "provider_error", "fraud"],
        [success_rate, provider.user_error_rate, provider.error_rate, provider.fraud_rate])

def read():
    num_new_users = get_event_count(new_users_per_sec)
    num_sales = get_event_count(sales_per_sec)
    num_page_hits = get_event_count(page_hits_per_sec)
    num_asset_hits = get_event_count(asset_hits_per_sec)

    payment_counts = get_outcomes(num_sales,
        providers.keys(),
        [providers[p].popularity for p in providers.keys()])

    provider_results = {
        k: calculate_payment_results(payment_counts[k], providers[k])
        for k in providers.keys()
    }

    page_results = get_outcomes(num_page_hits,
        ["200", "400", "500"],
        [wt_200, wt_400, wt_500])

    asset_results = get_outcomes(num_asset_hits,
        ["200", "400", "500"],
        [asset_200_wt, asset_400_wt, asset_500_wt])

    send_counter("new-sessions", num_new_users)

    for id, result in provider_results.items():
        for outcome, freq in result.items():
            send_counter("payment-provider-"+id+"."+outcome, freq)

    send_gauge("page-latency.mean", get_page_latency())
    send_gauge("asset-latency.mean", get_asset_latency())
    send_counter("page-hits-total", sum(page_results.values()))
    send_counter("asset-hits-total", sum(asset_results.values()))

    for k,v in page_results.items():
        send_counter("page-response-code-"+k, v)

    for k,v in asset_results.items():
        send_counter("asset-response-code-"+k, v)


def config(c):
    pass

collectd.register_read(read)
