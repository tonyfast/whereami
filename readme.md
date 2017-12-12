
# [whereami](https://github.com/tonyfast/whereami)

<code>[pip install git+https://github.com/tonyfast/whereami](https://github.com/tonyfast/whereami)</code>

Logic circuits to identify the context a notebook's derived source is executing in.

* Is Jupyter running this?
* Is source in an Interactive session?
* Is this a command line tool?


> [Original Presentation](http://nbviewer.jupyter.org/format/slides/github/tonyfast/whereami/blob/master/whereami.ipynb#/)

---

        ipython setup.py develop

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
    %run whereami.ipynb
    %run whereami.py
```

    
    {FILE: 🚫, INTERACTIVE: ✅, JUPYTER: ✅, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: 🚫}
    
    
    {FILE: ✅, INTERACTIVE: ✅, JUPYTER: 🚫, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: ✅}
    
    
    {FILE: ✅, INTERACTIVE: ✅, JUPYTER: 🚫, JYTHON: 🚫, MAIN: ✅, MODULE: 🚫, PYPY: 🚫, PYTHON: ✅, SCRIPT: ✅}
    


# Developer

`whereami` contains it's own build steps.  Run that notebook in `--execute` mode by checking for `huh.JUPYTER`.


```python
    %%file setup.py
    __import__('setuptools').setup(name="whereami", py_modules=['whereami'])        
```

    Overwriting setup.py



```python
    huh = __import__('whereami').huh(globals())
    if huh.JUPYTER:
        !jupyter nbconvert --to markdown --execute whereami.ipynb
        !python -m doctest whereami.py
        !python -m pydoc -w whereami
        !jupyter nbconvert --to python readme.ipynb
        !jupyter nbconvert --to markdown readme.ipynb
        !jupyter nbconvert index.ipynb
```

    [NbConvertApp] Converting notebook whereami.ipynb to markdown
    [NbConvertApp] Executing notebook with kernel: other-env


`whereami` as a package.


```python
    if huh.MAIN and not huh.JUPYTER:
        !ipython setup.py develop
```
