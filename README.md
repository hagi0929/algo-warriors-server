## project setup
#### linux
if python and pythonvenv is not installed
```
apt-get update -y
python3-venv
```
then
```
make init
````
the above command installs all the requirment libraries to run this app

Then, copy rename template.env file to .env and fill up the database connection strings.

After these steps are good to go run the app with command below

```
make run
```

---
## conventions
* try best to use type hint
* controller, service, repos pattern for the architecture
* follow python conventions for all the varible and file names
* we will use sqlalchemy for the db library but not it's orm. 
* add more things
