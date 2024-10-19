## IoT Decibel Meter and Dashboard
This is the companion repo for my talk "Bringing ideas to life with DIY IoT: Visualizing Noise Pollution".

### Instructions

#### Setting up the hardware
1. First, you will need a raspberry pi, I'm using a 3B+, but any model that supports HATs should do. 
2. Get an Enviro module for the PI. I got the base model without air quality, but either will work. You can purchase them online [here](https://shop.pimoroni.com/products/enviro?variant=31155658489939) or from [Microcenter](https://www.microcenter.com/product/656584/pimoroni-enviro-indoor-environmental-monitor)
3. Attach the enviro to the Pi, simply push it down on the pins, no soldering necessary. You can find full instructions for this [here](https://learn.pimoroni.com/article/getting-started-with-enviro-plus)
4. Before finding a spot to place your pi, be sure to connect it to your wifi network and take note of its IP address. 
5. Find a good spot inside or outside where you want to capture data and place the pi. Make sure you're able to run power to it, it's within range of wifi, and won't get wet. 

#### Server 
Next on the agenda is getting a home server ready to go. Nothing fancy is needed here, just a computer that has some storage on it that can store your data and run the dashboard. Once you've got the server, you will need to install [Docker](https://www.docker.com/) on it. The rest of this tutorial will assume you are using Linux or a Linux-like system, if you're using Windows you will need to adjust accordingly. 

#### InfluxDB
1. Pull this repo down on your server, you will then need to open a terminal and navigate to the `influx` folder as you will be running commands and using some of the files.
2. Next run what is in `setup.sh`. Influx depends on `mytelegraf.conf` being in the right place. You can take a look at the file but shouldn't need to change anything in it. 
2. Create a `influx2.env` file. You will then need to populate it with your own values, most of these values can be whatever you want to set them to. 

```
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=yourusername
DOCKER_INFLUXDB_INIT_PASSWORD=yourpassword
DOCKER_INFLUXDB_INIT_ORG=yourorgname
DOCKER_INFLUXDB_INIT_BUCKET=environmental
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=yoursecrettoken
```

When influx starts up, it will depend on that file being created and in the right place, the root of the `influx` directory.

3. Now it's time to spin everything up. Take a look at the `docker-compose.yml` file and make sure everything looks good. Then run `docker compose up -d`

4. After your containers come up, you should then be able to login to Influx at `localhost:8006`. The login credentials should be the same values you set in the env file earlier. If something goes wrong, check the logs of your main influx container.
> `docker ps` will list all the containers, then [docker logs](https://> docs.docker.com/reference/cli/docker/container/logs/)

5. [Generate an API token](https://docs.influxdata.com/influxdb/cloud/admin/tokens/create-token/) and take note of it, you will need it later

6. Login to influx and make sure the bucket you specified in the env was created. Then make sure you can hit influx from a machine other than the server itself. The address should be something like `${server_ip}:8086`.

#### Recording the sound data
Now that you have InfluxDb up and running we can now set up the meter and start sending the data to influx. 

1. Login to the pi over ssh and clone this repo to it.
2. Copy the `src/.asoundrc` file in the repo over to the home directory of the pi
3. Using `vi` or `vim`, create `src/.env` and fill out the following variables
```
API_TOKEN=yourtokenfrominflux
SERVER_ADDRESS='http://serverip:8086'
ORG='yourorg'
BUCKET='yourbucket'
```

4. Install the dependencies needed for the python program to run by running `pip3 install -r src/requirements.txt`

5. Test out the Python script by running `python3 src/DecibelMeter.py`
6. If all goes well, stop the script. If there are any missing dependencies install them. 
7. In `src/decibel-meter.service`, replace the path for `ExecStart` to the path where your python script is located.
8. Copy the service file to your system `cp src/decibel-meter.service /etc/systemd/system/decibel-meter.service`
7. Reload the daemon so it knows about the new service `sudo systemctl daemon-reload`
8. Enable the new service `sudo systemctl enable decibel-meter.service`
9. Use the following commands to start, stop, or restart the service
```
sudo systemctl start decibel-meter
sudo systemctl stop decibel-meter
sudo systemctl restart decibel-meter
```
> You can also give the Docker approach a try. I have started Dockerizing the script but as of now it is not finished. If the service is started, it will continuously run the Python script, even after a reboot.

> For some reason, after a reboot, something in the system deletes the `.asoundrc` file, and the Python script is unable to run successfully without it. Upon reboot, you will need to stop the service, wait for the file to get deleted, restore it, then start the service again. I'm sure there is a solution for this, but I've not put time into solving it at this time. 

> Most of the code in `DecibelMeter.py` is not my own. It is generously made available by [roscoe81](https://github.com/roscoe81/northcliff_spl_monitor) and has been adapted for the meter. You can find the full list of acknowledgements at the bottom of the file.

#### Grafana
If you made it this far, congrats! The worst of it is over. Setting up Grafana is fairly simple and straightforward and very similar to how InfluxDB was setup. Grafana is the tool we will be using to actually read the data and build a meaningful dashboard. 
1. The easiest way to go about this may be to follow the [official docs for running via docker compose](https://grafana.com/docs/grafana/latest/setup-grafana/installation/docker/#run-grafana-via-docker-compose), however I have supplied an example `grafana/docker-compose.yml` here as well. You will need to replace the env values in the file for your own. 
> On my setup I am hosting grafana on my own domain. I hope to add full instructions for how to do this at some point, but for now that is beyond the scope of this guide. If you have a domain and know how to port-forward, you should be able to set the proper env vars in the compose file and run from there. 
2. One Grafana spins up, check to see if you can login at port 3000. 
3. Once logged in, go to datasources and setup InfluxDB as a datasource, pointing to it your hosted Influx instance. 
4. After getting the datasource configured create a new dashboard and point it to the datasource you just configured. You are now free to add whatever visualizations you want. An example dashboard config has been supplied for you at `grafana/dashboard.json`. You can import this to a new dashboard but you will probably have to change the datasource as yours will be different. 

### End
If you made it to the end, nice work! I hope this was a fun and inspiring project for you to work on. If you have found a problem with the code or instructions, please open an issue or a PR to this repo. If you would like to contribute data to the project and hook into my existing dashboard open an issue so we can get in touch. 