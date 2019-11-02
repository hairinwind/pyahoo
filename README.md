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
- 