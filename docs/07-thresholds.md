# Setting up error thresholds.

In order to use Riemann for alerts, we need to be able to define exceptional behaviour. In the next exercise we're going to set up an alert that will trigger if our average CPU goes above 90%.

Before we do that, though, we'll need a way to test it. Thankfully Riemann has support for unit testing your configuration, so we don't actually need to cause an outage to see whether it works.

Open the file /riemann/src/riemann-test.clj and read the carefully considered comments.

There are two tests in the file that need to be completed. 

You can run your unit tests with with run_tests.sh script in the root of the project.


When you first run the tests you should see the following output

```
INFO [2016-08-12 15:17:56,920] main - riemann.bin - Loading /opt/riemann/etc/riemann-test.clj

Testing riemann.config-test

FAIL in (events-are-sent-to-influx) (riemann-test.clj:72)
expected: (= (get (inject! [e]) :influx) [e])
  actual: (not (= nil [{:service "myservice", :metric 23, :host "localhost", :state "ok"}]))
```

Since we don't have a tap named "influx" yet, the get function is returning nil, and nil does not equal the expected event.
