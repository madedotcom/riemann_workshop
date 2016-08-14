# Expiring events from the index


Riemann keeps events in memory for a short period of time so that it can perform correlation and display its own dashboards. The datastore for the events is called the index. Events are stored in the index for a period of time controlled by the :ttl property. Once the :ttl passes, the event is expired. The index is essentially a big map from (:host, :service) -> event. If riemann receives a new event for the same :host and :service, it will replace the previous one.

If riemann does not receive a new event before the ttl passes, it will replay the last received event, with a :state of "expired".

Change your streams declaration to look like this:

```
(streams
    ; if the event is not expired and the metric is not a NaN
    (where (not (state "expired"))
    (where* is-not-nan?

        ; keep events for 30 secs by default
        (default {:ttl 30 } 
        ; stick it in the index
        index
        ; raise any alerts
        threshold-and-alert
        ; send it to influx
        influx)))

    ; if the event IS expired, just print it to stdout.
    (expired
        prn))
```

Test this with the riemann-client. 

`riemann-client --host riemann --port 5555 send -S expired -s myservice`

You should see the event logged immediately. To check expiry, just send an event that is ok.

`riemann-client --host riemann --port 5555 send -S ok -s myservice -m 10`

After the 30 seconds has passed, riemann will expire the event, and put it back in the queue. You should see the event logged with a :state of expired.


## Using expiry as a heartbeat

Since new events will overwrite old ones in the index, your CPU and memory metrics shouldn't ever expire. If a new event does not arrive before the ttl is up, then we can process it differently.

This is useful for setting up "heartbeat" monitoring, where a service has to raise a metric every X seconds or minutes.

To play with this, let's set up a new collectd plugin.

Add a new file in collectd/root/etc/collectd.d called ping.conf and add the following:

```
LoadPlugin Ping

<Plugin Ping>
 host cheese.com
</Plugin>
```

We will now start collecting ping statistics for cheese.com. The metric is the latency of ping round-trips. If you're bored of clojure at this point, go make a pretty graph in grafana to show the response time of cheese.com. I can wait.

Use the influxdb admin page to find out what your new ping metric is called.

Now add a unit test.

```
 (deftest expired-pings-are-critical

        (def e
            {
                :service <name of service>
                :state "expired"
            })
        ; if we receive an expired ping alert
        ; we should set the state to critical
        ; and forward the event to the alert stream
        (is = (get (inject! [e]) :alert)
              [{
                :service <name of service>
                :state "critical"
                }]))
```

Use the `with` and `where` functions to call the alert stream if a ping event expires from the index.

Once you're happy that it works, reload your riemann config and test the functionality by disabling your network. After a few seconds you should receive an alert.
