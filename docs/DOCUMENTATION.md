# website-monitor documentation

"website-monitor" is an app that monitor websites availability over the network with in time interval using **Kafka** Producer which will periodically checks the target websites  and sends the check results to a kafka topic, then a kafka consumer storing the data to an Aiven PostgresSQL database table.

# Configuration

To configure tasks simply create a YAML file containing your interval and websites, patterns. Here’s an example:

to check list of websites 
```
interval: 5
monitors:
  - name: monitor 1
    url: http://www.google.com
    pattern : google
  
  - name: monitor 2
    url: http://www.facebook.com
    pattern : fb
  
  - name: monitor 3
    url: http://www.bla.com

  - name: monitor 4
    url: http://www.bar.com
```

## YAML Configuration options

* `interval` **(integer)** : The period interval which is kafka producer going to check the website and sends to the provided topic
* `monitors` **(list)** : **List** of all websites
    * `name` **(string) (optional)** : Give a name for proper logging
    * `url` **(string)** : The website url which has to be monitored
    * `pattern` **(regex|string) (optional)** : A string pattern which has to be checked it can be regex


## KAFKA & DB Configuration options

The used DB is PostgresQL

Config file is
[here](https://github.com/moogacs/monitor/blob/master/utils/config.py)

```
#Monitor File path
MONITERFILE:  Monitor file naming convention

#DB PSQL  PostgresQL Configuration
PS_DATABASE_NAME: DB Name
PS_USERNAME: DB access username
PS_PASSWORD: DB access pw
PS_HOST: DB access host
PS_PORT: DB access port
PS_WEBSITE_TABLE_NAME: DB table name that the consumer uses to storing the results
PS_TEST_WEBSITE_TABLE_NAME: DB table name that is used during tests

#KAFKA Kafka Configuration
K_HOST: Kafka access host
K_PORT: Kafka acess port
K_SECURITY_PROTOCOL: Kafka acess security protcol
K_SSL_CAT_FILE: SSL Certificate
K_SSL_CERT_FILE: SSL Certificate
K_SSL_KEY_FILE: SSL key
K_MONITOR_TOPIC: topic name
K_MONITOR_TEST_TOPIC: topic name for test
K_REPLICA_FACTOR: in case of creating the topic, what is the replication factor number
K_NO_PARTITIONS: in case of creating the topic, what is the partition number

#REGEX
URL_REGEX: Golbal regex to validate entered URLS
```



## DOCKER
The current docker [file](https://github.com/moogacs/monitor/blob/master/Dockerfile) is ready to just use which will create a  container and install the required packages, then runs the app

```
docker build -t monitor .

docker run monitor
```

# Multiprocessing

The kafka-producer and kafka-consumer are threads and for the approach of that solution [multiprocessing](https://docs.python.org/3/library/multiprocessing.html) package is used for **parallelism** by looking throught the code snippet below:

* because of `multiprocessing.Pool()` is used in without certin number of processes, then the number returned by `os.cpu_count()` is used which is returning the number of CPUs in the system.

* by calling `map_sync` which make the request for the url in an individual process **in parallel** then return the results to a callback function `send_result` to send the result from the producer.

* till the producer not stopped or killed the system will sleep the time interval requested, then going to create another processes to handle the next interval

* at the end for waiting all process to be finished one call `pool.join()`

```
pool = multiprocessing.Pool()
while not self.stop_event.is_set():
    if self.stop_event.is_set():
        break
    
    pool.map_async(Network.get_website_status, self.tasks, callback=self.send_results)

    i += 1
    time.sleep(self.interval)

# block at this line until all processes are done
pool.close()
pool.join()
self.producer.close()
```


```
def send_results(self, res):
        results = []
        results.extend(res)

        for website_status in results:
            if website_status:
                self.producer.send(self.topic, website_status)

                print("\nProducer sends ", end="")

                if website_status['name']:
                    print(website_status['name'])

                print(str(website_status))

                self.message_count += 1
```