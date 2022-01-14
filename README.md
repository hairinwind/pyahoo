# pyahoo

## setup linux machine
- install git
- git clone 
- install python3 ``` yum install -y python3 ```
- install pipenv ``` python3 -m pip install --user pipenv ```
- goto pyahoo dir, run pipenv install ``` python3 -m pipenv install ```

## to run it 
python main.py

## run it on ubuntu backend
It is now pipenv enabled  
```
python3 -m pipenv run  nohup python3 main.py &
```

## .bash_profile 
add "source ~/pyahoo/system/.bash_commons" in .bash_profile  
any changes could be checked in https://github.com/hairinwind/pyahoo/blob/master/system/.bash_commons

## auto run it after reboot
A service was made, see https://github.com/hairinwind/pyahoo/blob/master/system/make_pyahoo_service

## symbol file env var
```export PYAHOO_SYMBOL_FILE=symbol.1.txt```
this shall be replaced by ip mapping

To get the ip
```
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
```

create an ip mapping file


## Docker command 
the command to build the image
```
docker build --tag=pyahoo:latest --rm=true . --no-cache
```

the command to run the container
```
docker run -d -v /root/pyahoo/quotes:/opt/pyahoo/quotes -v /root/pyahoo/log:/opt/pyahoo/log -v /root/pyahoo/config:/opt/pyahoo/config --env PYAHOO_SYMBOL_FILE=symbol.top.txt --name=pyahoo pyahoo:latest
```
/root/pyahoo is the directory on my cloudcost

the command to look into the image
```
docker exec -it pyahoo bash
```

the command to login docker hub
```
docker login
```

the command to tag
```
docker tag pyahoo hairinwind/pyahoo:latest
```

the command to push
```
docker push hairinwind/pyahoo:latest
```

## upgrade pip 
'pip install --upgrade pip'
