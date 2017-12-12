
# whereami

Logic circuits to identify the context a notebook's derived source is executing in.

* Is Jupyter running this?
* Is source in an Interactive session?
* Is this a command line tool?

## Basic usage


```python
    huh = __import__('whereami').huh(globals())
    huh
```




    
    {FILE: 🚫, INTERACTIVE: ✅, JUPYTER: ✅, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: 🚫}



## Advanced

`whereami` contains an object `state` that contains


```python
    import whereami
    whereami.state
```




    
    {FILE: ✅, INTERACTIVE: ✅, JUPYTER: 🚫, JYTHON: 🚫, MAIN: 🚫, MODULE: ✅, PYPY: 🚫, PYTHON: ✅, SCRIPT: 🚫}



## IPython magic


```python
    %reload_ext whereami
```

    
    {FILE: 🚫, INTERACTIVE: ✅, JUPYTER: ✅, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: 🚫}
    



```python
    %run whereami.ipynb
```

    TestResults(failed=0, attempted=6)
    [NbConvertApp] Converting notebook whereami.ipynb to script
    [NbConvertApp] Writing 4957 bytes to whereami.py
    
    {PYPY: 🚫, JUPYTER: 🚫, MODULE: 🚫, FILE: ✅, SCRIPT: ✅, INTERACTIVE: 🚫, JYTHON: 🚫, PYTHON: ✅, MAIN: ✅}
    
    
    {FILE: ✅, INTERACTIVE: ✅, JUPYTER: ✅, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: ✅}
    



```python
    %run whereami.py
```

    
    {FILE: ✅, INTERACTIVE: ✅, JUPYTER: 🚫, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: ✅}
    



```python
    %run -n whereami.py
```

# Developer

`whereami` contains it's own build steps.  Run that notebook in `--execute` mode by checking for `huh.JUPYTER`.


```python
    %%file setup.py
    __import__('setuptools').setup(name="whereami", py_modules=['whereami'])        
```

    Writing setup.py



```python
    huh = __import__('whereami').huh(globals())
    if huh.JUPYTER:
        !jupyter nbconvert --to markdown --execute whereami.ipynb
        !python -m doctest whereami.py
        !python -m pydoc -w whereami
        !jupyter nbconvert --to python readme.ipynb
        !jupyter nbconvert --to markdown readme.ipynb
        !jupyter nbconvert index.ipynb
    elif huh.MAIN:
        !ipython setup.py develop

```
