# Using where to filter metrics

Use the collectd-reload script to restart collectd and watch the riemann logs. You should see some metrics arrive from collectd with the :metric NaN.

This is because collectd is forwarding the *rate of change* for CPU. When collectd first starts, it doesn't have an initial measurement to compare against, and it forwards NaN.

This is a problem because it will break influxdb later, but we can filter those events out.

The `where` streams takes a condition, and a list of streams. For example `(where (service "myservice") prn)` will print every event where the service is "myservice".

Test that by changing your streams declaration like this:

```
(streams
    (where (service "myservice")
        prn))
```

Reload the riemann config and use the python container to send a metric with the service "myservice".


To filter out the NaN metrics, we need to use the `where*` function - this takes a function rather than a condition. There is a function named "is-not-nan?" in the file riemann/src/made/util.clj that we can use as a filter.

```
(streams
    (where* is-not-nan?
        prn))
```


This function returns false if the metric value of an event is NaN, otherwise true. To avoid NullReference errors, we first ignore nil values.


reload the riemann config and collectd config and check that you are no longer seeing NaN events.


Take a couple of minutes to read the documentation on `where` and `where*` at http://riemann.io/api/riemann.streams.html 

If you're struggling to understand what the fuck the docs because I can't even like lolwut? grab Bob as he wanders around. You'll need to be able to read the docs later as we do more complex exercises.
