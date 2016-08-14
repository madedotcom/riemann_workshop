(ns made.influxdb)

; riemann already ships with support for influxdb, so we just need to require the function
(require '[riemann.influxdb :refer [influxdb]])
(require '[riemann.streams :refer [batch]])
(require '[riemann.test :refer [tap io]])


; here we set up an associative array that contains our configuration
(def cfg 
    {
        :version :0.9
        :host "influxdb"
        :port 8086
        :db "riemann-local"
        :username "root"
        :password "password"
    })

; Here we define a stream named "influx" that sends events to influx.
; We batch the events into groups of 1000, or sending events every 2 minutes
; This reduces our total number of network round-trips.

(def influx
        (batch 1000 2
        (influxdb cfg)))
