# CS348 Project Server

### Prerequisite
miniconda - linux
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```
miniconda - mac
```
mkdir -p ~/miniconda3
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
~/miniconda3/bin/conda init bash
```

### basic setup - Linux
```
make init
````
the above command installs all the requirment libraries to run this app

Then, copy rename template.env file to .env and fill up the database connection strings.

After these steps we are good to go run the app with command below

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
