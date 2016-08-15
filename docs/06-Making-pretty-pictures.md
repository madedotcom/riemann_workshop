# Setting up Grafana

Now that we have our metrics flowing into influxdb we can graph them.

Start by adding some more metrics. 

Open collectd.conf from collectd/root/etc/collectd/ and add the following lines

```
LoadPlugin Load
LoadPlugin Memory
LoadPlugin Interface
```

Reload the collectd config. You should start to receive metrics on memory, cpu load, and network traffic. Verify this using the influxdb admin interface on localhost:8083.

Now navigate to grafana, which is listening at localhost:3001. The username is admin, and the password is "password" because I hate security.

Before we can show metrics, we need to connect grafana to Influxdb. Click the Grafana logo in the top left, and then click "Data Sources" in the menu that drops down.

Click "Add Datasource" and fill in the following details:

Name: Influx
Default: yes
Type: InfluxDB
Url: http://influxdb:8086
Database: riemann-local
User: root
Password: password


Click the green "Add" button and you should get a flash to say "Success
Data source is working"

Click the grafana logo again, and then Dashboards > New.

There is a green tab to the left of the screen, click on that to add a new graph panel. 

In the general section, change the title to "CPU".
In the metrics tab click "select measurement" to choose one of your cpu metrics, you should see it appear on the graph.

Change the time period in the upper right to "Last 15 mins" and set refresh to every 10 secs.

Grafana and Influx allow you to select metrics by regular expression. Change the measurement to `/aggregate-cpu-average\/*/`. You should see all the aggregate-cpu-average metrics appear on your graph.

In the display tab change the Left-Y axis's Unit dropdown to "None > percent (0 - 100)".

You can display multiple metrics on a single graph, which is great for showing, for example, throughput vs latency, or CPU usage versus incoming web requests.

In the Metrics tab, Click "Add query" and set the measurement to "load/load/shortterm". 

Unfortunately for us, load has a different scale from cpu usage. You can check this by navigating to the influxdb admin page and running the following queries:

'SELECT * from "aggregation-cpu-average/cpu-user' (values are between 0 and 100)
'SELECT * from "load/load/shortterm"' (values are between 0 and 1)

To display it properly, we'll need to move it to the other axis. In grafana click "Display" then "Add Series Specific Option". For "alias or regex" type load and select "load/load/shortterm".

Now click the plus button at the end of the row and choose Y-Axis, setting it to "2".

You should see that the load/load/shortterm label in the legend moves to the right, and you have a second scale on the right of your graph.


Click the green tab at the left again and add a second panel. This time use the measurement regex `/memory\/*/` to show all your memory metrics.

In the display tab click the Stack checkbox, and change the Stacked Value dropdown to "individual".

You should now see that the graph is showing the total breakdown of memory use on your machine, eg. if you have 16Gb of RAM, the topmost line is at 16Gb. You can hover over the metrics to see their individual values.

Cumulative graphs like this are handy for showing breakdowns; eg web requests by http response codes or varnish hit/miss status.

In the lower right is a button marked "Add row". Click it, and you'll have a second green tab at the left of the screen. Create a new graph for network statistics. Use a regular expression to show the if_octets/tx and if_octets/rx for every interface. Select an appropriate unit of measurement in the display tab remembering that octet is network-speak for "byte".


Add another row and add some metrics for riemann, showing the throughput of events vs the 95th percentile latency. Since the network graph is showing the network traffic of the collectd container, you should notice a nice correlation between "riemann server tcp in rate" and "if_octets/tx".

Admire your handiwork - you've reproduced our entire monitoring stack and now we can do something more interesting :)
