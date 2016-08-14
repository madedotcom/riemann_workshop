(ns made.alerts)
(require '[riemann.streams :refer [default changed-state splitp where with]])
(require '[clojure.tools.logging :refer [info warn error]])

(def alert
  ; if our event doesn't already have a state, set it to ok
  (default {:state "ok"}
    ; changed-state acts as a filter. If an incoming event
    ; has a new state, it forwards the event to its children,
    ; if the state remains the same, it will drop the event.
    (changed-state {:init "ok"}

        ; splitp is used to divide incoming events into individual
        ; streams. here we're splitting things by the state
        ; but we could split by any field.
        (splitp = state
          "ok" (fn [x] (info "state is ok! " x))
          "warn" (fn [x] (warn "state is ungood " x))
          "critical" (fn [x] (error "everything is awful" x))))))

(def threshold-and-alert
  (default {:metric 0}
    ; these are the thresholds for "random" service
    (where (service "random")
        ; split by metric where the threshold is less than the value.
        (splitp < metric
            ; if 1000 < metric set the state to critical and alert
            1000 (with :state "critical" alert)
            ; if 500 < metric set the state to warn and alert
            500 (with :state "warn" alert)
            ; else set the state to ok and alert
            (with :state "ok" alert)))
  ))
