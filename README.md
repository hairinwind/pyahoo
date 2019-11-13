# pyahoo

## to run it 
python main.py

## run it on ubuntu backend
It is now pipenv enabled  
```
python -m pipenv run  nohup python3 main.py &
```

## symbol file env var
export PYAHOO_SYMBOL_FILE=symbol.1.txt
export PYAHOO_SYMBOL_FILE=symbol.top.txt
export PYAHOO_SYMBOL_FILE=symbol.top2.txt

## todo list 
- write file synchronizely
- collect all threads and join at last
- stop collecting quote if it is weekend

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