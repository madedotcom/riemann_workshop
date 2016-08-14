import collectd
from numpy.random import poisson, normal, choice
from collections import Counter

"""
This collectd plugin provides a crappy model of a busy-ish e-commerce site
that attracts around 200k sessions a day, with a 0.5% conversion rate.

To do that, they display around 1M web pages, and around 10 assets per-page.

Every web response and attempted sale might fail for a number of reasons.

The site has 4 different means of payment.

The probabilities for those things are all enumerated below.
"""


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
sales_per_sec = 0.012

# The likelihoods that a customer chooses payment provider x
provider_1_weight = 0.4
provider_2_weight = 0.3
provider_3_weight = 0.1
provider_4_weight = 0.2

# The likelihood of various kinds of failure.
user_error_rate = 0.01
provider_error_rate = 0.001
fraud_detector_rate = 0.003
payment_success_rate = (1 - user_error_rate - provider_error_rate - fraud_detector_rate)

def get_page_latency():
    return normal(page_latency_mean, page_latency_stddev, 1)[0]

def get_asset_latency():
    return normal(asset_latency_mean, asset_latency_stddev, 1)[0]

def get_event_count(rate):
    return sum(poisson(rate, interval))

def get_outcomes(count, outcomes, weights):
    return Counter(choice(outcomes, count, p=weights))

def send(name, val):
    collectd.Values(plugin="ecommerce",
                    type="gauge",
                    type_instance=name,
                    values=[val]).dispatch()

def read():
    num_new_users = get_event_count(new_users_per_sec)
    num_sales = get_event_count(sales_per_sec)
    num_page_hits = get_event_count(page_hits_per_sec)
    num_asset_hits = get_event_count(asset_hits_per_sec)

    payment_providers = get_outcomes(num_sales,
        ["provider-a", "provider-b", "provider-c", "provider-d"],
        [provider_1_weight, provider_2_weight, provider_3_weight, provider_4_weight])

    provider_a = get_outcomes(payment_providers["provider-a"],
        ["success", "user_error", "provider_error", "fraud"],
        [payment_success_rate, user_error_rate, provider_error_rate, fraud_detector_rate])

    provider_b = get_outcomes(payment_providers["provider-b"],
        ["success", "user_error", "provider_error", "fraud"],
        [payment_success_rate, user_error_rate, provider_error_rate, fraud_detector_rate])

    provider_c = get_outcomes(payment_providers["provider-c"],
        ["success", "user_error", "provider_error", "fraud"],
        [payment_success_rate, user_error_rate, provider_error_rate, fraud_detector_rate])

    provider_d = get_outcomes(payment_providers["provider-d"],
        ["success", "user_error", "provider_error", "fraud"],
        [payment_success_rate, user_error_rate, provider_error_rate, fraud_detector_rate])

    page_results = get_outcomes(num_page_hits,
        ["200", "400", "500"],
        [wt_200, wt_400, wt_500])

    asset_results = get_outcomes(num_asset_hits,
        ["200", "400", "500"],
        [asset_200_wt, asset_400_wt, asset_500_wt])

    send("new-sessions", num_new_users)

    for k,v in provider_a.items():
        send("payment-provider-a."+k, v)
    for k,v in provider_b.items():
        send("payment-provider-b."+k, v)
    for k,v in provider_c.items():
        send("payment-provider-c."+k, v)
    for k,v in provider_d.items():
        send("payment-provider-d."+k, v)

    send("page-latency.mean", get_page_latency())
    send("asset-latency.mean", get_asset_latency())
    send("page-hits-total", sum(page_results.values()))
    send("asset-hits-total", sum(asset_results.values()))

    for k,v in page_results.items():
        send("page-response-code-"+k, v)

    for k,v in asset_results.items():
        send("asset-response-code-"+k, v)


def config(c):
    print "Hello!"

collectd.register_read(read)
