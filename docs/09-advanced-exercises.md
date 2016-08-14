# Moving beyond basic monitoring

Riemann, collectd, influx, and grafana make it really simple to perform monitoring of technical metrics; set threshold levels for resource usage; and display graphs of current and historical performance, but there is much more that we can do.

The file collectd/root/opt/python_plugins/made_web_traffic.py is a collectd plugin that sends random values to simulate web traffic and e-commerce metrics.

Using these data, we can make interesting graphs, and we can perform basic anomaly detection. Riemann's complex event processing model makes this a tractable problem.

You can feel free to tackle these in any order. 

# Monitoring web traffic

We raise events for every web response:

    ecommerce/gauge-page-response-200 
    ecommerce/gauge-page-response-400 
    ecommerce/gauge-page-response-500 

are the counts of 2xx, 4xx, and 5xx responses for generated web pages.

    ecommerce/gauge-asset-response-200
    ecommerce/gauge-asset-response-400
    ecommerce/gauge-asset-response-500

are the counts of 2xx, 4xx, and 5xx responses for assets like js and images.

we also send:
 
    ecommerce/gauge-asset-hits-total
    ecommerce/gauge-page-hits-total

for the raw request numbers without any response-code breakdown and

    ecommerce/gauge-asset-latency-mean
    ecommerce/gauge-page-latency-mean

to record the response times in milliseconds.

1. Show a bar chart showing the total traffic over time and overlay a line graph of the latency. Since this is just a model, you will not see any correlation, but this is a key graph for a live system.

2. Trip an alert if there is a spike in latency. To achieve this you can use the moving-window function, and the folds/stddev function. If the stddev changes by more than some threshold value, raise a critical alert. You can test this by changing the standard deviation of the latency in the collectd plugin, or (even better) by writing some unit tests.

3. Trip an alert if there is a sudden spike in traffic volume. 

4. Trip an alert if the percentage of failed requests (400 + 500) goes above 10% in any single 5 minute period.

5. Trip an alert if the percentage of 500 errors goes above 1% in any single 5 minute period.

6. Write a clojure function that uses both the latency and the error rate to compute a "health" state of "ok", "warn", or "error". Write this health state to the alerts stream every 5 minutes.

# Monitoring payments

We raise events every time a payment attempt is made.

For each of payment providers a, b, c, d we raise the following events:

    ecommerce/payment-provider-x.user_error if a user enters a bad card number or similar
    ecommerce/payment-provider-x.provider_error if there is a technical fault
    ecommerce/payment-provider-x.fraud if the provider returns a fraud alert for the card
    ecommerce/payment-provider-x.success if the payment is successful.

We also raise the count of new sessions with the event

    ecommerce/new-sessions

1. Calculate the conversion rate by hour, by dividing the new sessions by total successful payments.

2. Trip an alert if there are more than X fraud errors in a single 1 hour window.

3. Trip an alert if any provider begins to return regular provider_error metrics. You will need to decide on an appropriate way to measure this.

4. Trip an alert if the number of payments received suddenly drops (e. a negative spike)
