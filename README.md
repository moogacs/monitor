# Websites Monitor [![Build Status](https://travis-ci.com/moogacs/monitor.svg?branch=master)](https://travis-ci.com/moogacs/monitor)
This is an app that monitor websites availability over the network with in time interval and sends a response of 
* response code
* response message
* response time
* search content pattern (optional)

# Getting Started
1. Clone the repository
2. Cretate/update a configuration file, see [Configuration](https://github.com/moogacs/monitor/blob/master/docs/DOCUMENTATION.md/#configuration)
3. Install the contents of [requirements](https://github.com/moogacs/monitor/blob/master/requirements.txt) `requirements.txt` into a Python 3.6+ environment
4. Run the app according to Usage


## Quickstart
You can run the app using onr of 2 options
1. add websites to `monitor.yml` file
    ```
    python app.py
    ```
2. create your own file and use `monitor.yml` as an **example** which you can pass it as a variable to the app
    ```
    python app.py monitor.yml
    ```
   
### Createing a docker image:
```
docker build -t monitor .

docker run monitor
```

### Testing run command :
```
python -m unittest discover tests
```

## Documentation
Documentation
[here](https://github.com/moogacs/monitor/blob/master/docs/DOCUMENTATION.md)
