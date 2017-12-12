
# coding: utf-8

# # `whereami`
# 
# Logic circuits to identify the context a notebook's derived source is executing in.
# 
# * Is Jupyter running this?
# * Is source in an Interactive session?
# * Is this a command line tool?
# ---
# 
# > [Demonstration](index.ipynb) | [`readme`](readme.ipynb)

# In[180]:


__doc__ = """whereami tests

Basic usage.

>>> state = __import__('whereami').huh(globals())


One of the main uses of whereami differentiates between interactive Jupyter 
sessions and imperative, procedural Python operations.

>>> if state.JUPYTER:
...     assert not state.FILE and state.MAIN and state.INTERACTIVE
... else:
...     assert state.FILE

>>> assert __import__('whereami').state.MODULE
"""

__all__ = 'huh', 'dunder'


# ## whereami exports

# `dunder` is short hand for **d**ouble**under**core.

# In[182]:


dunder = "__%s__"


# # Where are we `huh`?  

# In[184]:


class huh(object):
    def __init__(x, object:dict=None):
        """When creating the object, decide if the state is INTERACTIVE or not?
        >>> assert isinstance(huh().globals, dict)
        """
        try:
            import IPython
            ip = IPython.get_ipython()
            x.INTERACTIVE = isinstance(IPython.get_ipython(), 
                                         IPython.core.interactiveshell.InteractiveShell)
            if not object: object = ip.user_ns
        except:
            x.INTERACTIVE = False
            if not object: object = globals()
        x.globals = object
    
    @classmethod
    def state(cls, callable, decorate=True):
        """Append attributes to huh.  Non-upper case attributes are created as properties."""
        setattr(cls, callable.__name__, property(callable) if callable.__name__[0].isupper() else callable)


# # Are we in a live 🥁 kernel?

# In[210]:


@huh.state
def __init__(x:huh, object:dict=None):
    """When creating the object, decide if the state is INTERACTIVE or not?
    >>> assert isinstance(huh().globals, dict)
    """
    try:
        import IPython
        ip = IPython.get_ipython()
        x.INTERACTIVE = isinstance(IPython.get_ipython(), 
                                     IPython.core.interactiveshell.InteractiveShell)
        if not object: object = ip.user_ns
    except:
        x.INTERACTIVE = False
        if not object: object = globals()
    x.globals = object
    
huh(globals()).INTERACTIVE and __import__('IPython').get_ipython()


# # We know that we are running 🐍.

# In[211]:


@huh.state
def PYTHON(x:huh): return __import__("sys").version_info.major


# ### What about J🐍?

# In[212]:


@huh.state
def JYTHON(x:huh): return "java" in __import__("platform").system().lower()


# ### ...or 🍰🍰?

# In[213]:


@huh.state
def PYPY(x:huh): return "pypy" in __import__("platform").python_implementation().lower()


# ## Are we running code from a `__file__`?

# In[293]:


@huh.state
def FILE(x:huh): 
    """Does file exists in the namespace?
    
    %run is a special case where a jupyter application has a file.
    """
    return dunder%'file' in x.globals


# ## Are we running code in the `__main__` context?
# 
# Jupyter applications and Python applications may be run in the main context.

# In[294]:


@huh.state
def MAIN(x:huh): 
    """
    >>> assert not state.MAIN or state.MAIN and dunder%'name' in state.globals
    """
    return x.globals.get(dunder%'name') == dunder%'main'
__name__


# ### _most_ Jupyter applications _do not_ rely on a `__file__`.

# In[289]:


@huh.state
def JUPYTER(x): 
    """Is jupyter running the application?"""
    return x.MAIN and not x.FILE


# ## Are we running code as a [scripting language]()?

# In[290]:


@huh.state
def SCRIPT(x): 
    """Is the command procedural?"""
    return x.FILE and x.MAIN


# In[291]:


@huh.state
def MODULE(x): 
    """Is the script imported by Python?
    
    >>> if state.SCRIPT:
    ...     assert not state.MODULE
    """
    return x.FILE and not x.MAIN


# ## What does `huh` look like, huh?

# In[292]:


@huh.state
def __iter__(self):
    yield from ((key, bool(getattr(self, key))) for key in dir(self) if key[0].isupper())

@huh.state    
def __repr__(self):
    return "\n%s\n"%repr(dict(
        (k, "🚫✅"[v]) for k, v in self)).replace("'", "")


# # Internal Usage
# 
# `whereami.state` records it's state when it is used.s

# In[285]:


state = huh(globals())
state.__doc__ = """The state of the imported `whereami` module."""


# ## Development and Testing

# In[286]:


if state.MAIN and not state.FILE:
    print(__import__('doctest').testmod())
    get_ipython().system('jupyter nbconvert --to script whereami.ipynb')
    get_ipython().system('python whereami.py')


# ## Run `whereami` as a script.
# 
#     if __name__ == dunder%'main':
#         print(state)

# In[267]:


if state.MAIN:
    print(state)


# ## [Make it an IPython extension.](http://ipython.readthedocs.io/en/stable/config/extensions/#writing-extensions)

# In[208]:


def load_ipython_extension(ip):
    print(huh())

