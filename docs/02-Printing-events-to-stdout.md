# Printing events to stdout

When debugging and developing riemann configs, it's often useful to make riemann dump things to the console.

The two functions you should use for this are `prn` and `info`.

Open the riemann config at riemann/src/riemann.config and add the following line.

`(streams prn)`

reload the configuration with the riemann-reload.sh script and wait a few seconds. Riemann should begin printing all metrics to stdout.

Change the line to read `(streams #(info "received event" %))` and reload again. Riemann will now print each event as an info-level log.

The `streams` function is the main entry point into riemann's config. A riemann stream is a function that receives an event. If Clojure were a statically typed language, each stream would have the type Event -> ().

The `streams` function takes a list of streams, and applies each one to every incoming event. Its type, therefore is [(Event -> ())]-> ().
