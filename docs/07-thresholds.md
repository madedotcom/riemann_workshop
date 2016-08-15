# Setting up error thresholds.

In order to use Riemann for alerts, we need to be able to define exceptional behaviour. In the next exercise we're going to set up an alert that will trigger if our average CPU goes above 90%.

Before we do that, though, we'll need a way to test it. Thankfully Riemann has support for unit testing your configuration, so we don't actually need to cause an outage to see whether it works.

Open the file /riemann/src/riemann-test.clj and read the carefully considered comments.

There are two tests in the file that need to be completed. 

You can run your unit tests with run_tests.sh script in the root of the project.


When you first run the tests you should see the following output

```
INFO [2016-08-12 15:17:56,920] main - riemann.bin - Loading /opt/riemann/etc/riemann-test.clj

Testing riemann.config-test

FAIL in (events-are-sent-to-influx) (riemann-test.clj:72)
expected: (= (get (inject! [e]) :influx) [e])
  actual: (not (= nil [{:service "myservice", :metric 23, :host "localhost", :state "ok"}]))
```

Since we don't have a tap named "influx" yet, the get function is returning nil, and nil does not equal the expected event.


## Setting the state based on a threshold

Once your tests are passing, we can write some new functionality to raise alerts if cpu goes over certain limits.

In your riemann.config you should require the namespace made.alerts, and :refer the `alert` function. This function will log a message when a service changes state. In a production system you might want to send the events to Pagerduty or Slack instead.

Add the alert stream into your streams declaration and reload the config. You can test it by sending events from the python container.

`riemann-client --host riemann --port 5555 send -s myservice -S "error"`
`riemann-client --host riemann --port 5555 send -s myservice -S "ok"`

Notice that if you send the same state twice, you don't see a repeat of the log. 

Now refer and add the threshold-and-alert stream from the made.alerts namespace.

Test this in the python container like so:

`riemann-client --host riemann --port 5555 send -s random -m 1` 
`riemann-client --host riemann --port 5555 send -s random -m 500` 
`riemann-client --host riemann --port 5555 send -s random -m 501` 
`riemann-client --host riemann --port 5555 send -s random -m 551` 
`riemann-client --host riemann --port 5555 send -s random -m 50051` 
`riemann-client --host riemann --port 5555 send -s random -m 5000` 
`riemann-client --host riemann --port 5555 send -s random -m 550` 
`riemann-client --host riemann --port 5555 send -s random -m 5` 

Check the code in the alerts namespace and make sure you understand it what it's doing. Refer to the riemann.streams documentation or shout for help if you're stuck.

Add a tap to the alert stream and write some tests:

* If the aggregation-cpu-average/cpu-idle service is below 10 then raise a critical error.
* If the service is below 30 raise a warning.
* Otherwise raise "ok"

Once your tests pass, check your new functionality with the riemann-client and rejoice.

If you want to play with thresholds some more, add the df plugin to collectd and set up thresholds for disk usage.
