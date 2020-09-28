# monitor
This is an app that monitor websites availability over the network with in time interval and sends a response of 
* response code
* response message
* response time
* search content pattern (optional)

### Quickstart
You can run the app using 2 options with providing 
1. add websites to `monitor.yml` file
```
python app.py
```
1. create your own file and use `monitor.yml` as an **example** which you can pass it as a variable to the app
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