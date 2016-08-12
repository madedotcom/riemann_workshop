# Getting Started

All the components you'll need are set up as docker files in this directory structure. 

You can bring everything up with `docker-compose up`.

After everything has built, you should see a whole bunch of logs.

Since we'll be modifying configs a lot, I've mounted config directories as volumes, this means you can change the configs without rebuilding the containers.

To reload the configs, you can use the shell scripts "/collectd-reload.sh" and "riemann-reload.sh"

Riemann's config is written in clojure, which is enormously off-putting at first glance, but is actually kinda nice when you get used to it.


Some quick things on syntax:

Single line comments are marked with a semicolon:

; This is a clojure comment

 Clojure is a Lisp, so everything in Clojure is either a List `(1 2 3)` or an atom `1`.

Variable declarations are lists of two elements, where the first element is the name of the var, and the second element is the value,eg.

(def x 23)

Functions calls are also lists, where the first element is the function, and the remainder of the elements are the arguments.

eg. (+ 1 2) calls the + function with the args 1 and 2.

Symbols are commonly used to denote names of things, much as you'd use an enum or a const string in other languages. Symbols are prepended with a colon like :this.

Riemann chiefly works with maps (dicts for you pythonistas). You can declare a map like this:

(def mymap
    {
        :key value
        :key2 value2 
    })

For conditionals, we can use if like so:

(if true 
    ; true clause
    (println "true is true") 
    ; optional false clause
    (println "true is not true"))

Or we can use the cond form, which is like a switch statement:

(cond 
    ; cond's body comprises pairs of conditionals and results.
    (> x 10) (println "x is greater than 10")

    (< x 2) (println "x is smaller than 2)

    ; you can use the symbol :else for the default case
    :else (println "x is neither of those things))

There's a handy reference to basic syntax here: https://github.com/jasongilman/clojure-101/blob/master/src/clojure_101/core.clj

Clojure is a strongly typed dynamic language, much like Python, but to aid understanding, I've included ML style type signatures in the documentation. If you're not a Haskeller, and the type signatures confuse you, ignore them.
