(ns made.util)

(defn is-nan?
     [event]
     (and
       (not (nil? (:metric event)))
       (Double/isNaN (:metric event))))
