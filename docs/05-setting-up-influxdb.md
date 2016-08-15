# Setting up influx

At this point we have metrics writing to the console, but we're yet to do anything interesting with them. Let's set up influxdb, and then graph some metrics.

Influxdb should already be running, you can verify that by opening http://localhost:8083

To get our metrics into Riemann, we're going to create a new stream and use it in our config.

Create a new file named influxdb.clj in riemann/src/made.

```
(ns made.influxdb)

; riemann already ships with support for influxdb, so we just need to require the function
(require '[riemann.influxdb :refer [influxdb]])
(require '[riemann.streams :refer [batch]])
(require '[riemann.test :refer [tap io]])

; here we set up an associative array that contains our configuration
; the (def) special form declares a variable; (def name value).
(def cfg 
    {
        :host "influxdb"
        :port 8086
        :db "riemann-local"
        :username "root"
        :password "root"
        :version :0.9
    })

; Here we define a stream named "influx" that sends events to influx.
; We batch the events so that we send events when
;    a) we have 1000 events in our queue or
;    b) 2 seconds have passed since the last batch.
; This reduces our total number of network round-trips, and improves throughput.

(def influx
    (batch 1000 2
        (influxdb cfg)))
```

To use our new influx stream, we'll need to import it into our riemann config.

Open riemann.config and at the top add `(require '[made.influxdb :refer [influx]])`

Now you can use your stream in the streams declaration. Most streams, including `where*` accept a list of other streams so you can just add influx to the list.

(streams
    (where* is-not-nan?
        prn
        influx))


Reload the riemann config and wait a few seconds. You should start to see logs from influxdb like this: 

```
influxdb | [http] 2016/08/12 13:42:19 172.17.0.4 - root [12/Aug/2016:13:42:19 +0000] POST /write?db=riemann-local&precision=s HTTP/1.1 204 0 - Apache-HttpClient/4.5 (Java/1.8.0_92) 96bcde50-6092-11e6-8011-000000000000 13.060991ms

```

Visit localhost:8083 in your browser and change the database drop-down in the upper right to "riemann-local". 

Use the Query Templates dropdown and select "Show Measurements". Hit enter, and influx will give a list of all the metrics it has so-far received.

This is really useful for testing whether your metrics are actually being persisted.

Change the Query textbox to read `SHOW TAG VALUES WITH KEY = "host"` and hit enter, you will now see a list of all your metrics, and all the hosts that have reported them. Currently you only have a single host - localhost - listed.


IF you use the python container to send a new metric, from a different host, you should find it in this view.

