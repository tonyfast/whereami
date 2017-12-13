
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
# > [Presentation](index.ipynb) | [`readme`](readme.ipynb)

# >A primary use of the `whereami` differentiates between interactive Jupyter sessions and imperative, procedural Python operations.

# In[1]:


__doc__ = """whereami tests

Basic usage.

>>> state = __import__('whereami').huh(globals())


>>> if state.JUPYTER:
...     assert not state.FILE and state.MAIN and state.INTERACTIVE
... else:
...     assert state.FILE

>>> assert __import__('whereami').state.MODULE
"""

__all__ = 'huh', 'dunder'

# dunder` is short hand for **d**ouble**under**core.
dunder = "__%s__"


# # Where are we `huh`?  

# In[2]:


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


# ## What does `huh` look like, huh?

# In[3]:


@huh.state
def __iter__(self):
    yield from ((key, bool(getattr(self, key))) for key in dir(self) if key[0].isupper())

@huh.state    
def __repr__(self):
    return "\n%s\n"%repr(dict(
        (k, "🚫✅"[v]) for k, v in self)).replace("'", "")


# # Are we in a live 🥁 kernel?
# 
# [`get_ipython` exists in every live notebook.](get_ipython.ipynb)

# In[4]:


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


# ## Are we running code from a `__file__`?
# 
# An interactive notebook does not have the `__file__` object.

# In[5]:


@huh.state
def FILE(x:huh): 
    """Does file exists in the namespace?
    
    %run is a special case where a jupyter application has a file.
    """
    return dunder%'file' in x.globals


# ## Are we running code in the `__main__` context?
# 
# Jupyter applications and some Python applications run in the main context.

# In[6]:


@huh.state
def MAIN(x:huh): 
    """
    >>> assert not state.MAIN or state.MAIN and dunder%'name' in state.globals
    """
    return x.globals.get(dunder%'name') == dunder%'main'
__name__


# ### _most_ Jupyter applications _do not_ rely on a `__file__` and run as `__main__`.
# 
# > The rarely used `%run` magic is an edge case.

# In[17]:


@huh.state
def JUPYTER(x): 
    """Is jupyter running the application?"""
    return x.MAIN and not x.FILE


# ## Are we running code as a [scripting language]()?

# In[8]:


@huh.state
def SCRIPT(x): 
    """Is the command procedural?"""
    return x.FILE and x.MAIN


# ### ...or a module.

# In[9]:


@huh.state
def MODULE(x): 
    """Is the script imported by Python?
    
    >>> if state.SCRIPT:
    ...     assert not state.MODULE
    """
    return x.FILE and not x.MAIN


# # Other interesting conditions
# 
# ## We know that we are running 🐍.

# In[10]:


@huh.state
def PYTHON(x:huh): return __import__("sys").version_info.major


# ### What about J🐍?

# In[11]:


@huh.state
def JYTHON(x:huh): return "java" in __import__("platform").system().lower()


# ### ...or 🍰🍰?

# In[12]:


@huh.state
def PYPY(x:huh): return "pypy" in __import__("platform").python_implementation().lower()


# # Internal Usage
# 
# `whereami.state` records it's state anytime it is executed including imports.

# In[13]:


state = huh(globals())
state.__doc__ = """The state of the imported `whereami` module."""


# ## Development and Testing

# In[14]:


if state.MAIN and not state.FILE:
    print(__import__('doctest').testmod())
    get_ipython().system('jupyter nbconvert --to script whereami.ipynb')
    get_ipython().system('python whereami.py')


# ## Run `whereami` as a script.

# In[15]:


if state.MAIN:
    print(state)


# ### Equivalent to.
# 
#     if __name__ == '__main__':
#         print(state)

# ## [Make it an IPython extension.](http://ipython.readthedocs.io/en/stable/config/extensions/#writing-extensions)

# In[16]:


def load_ipython_extension(ip):
    print(huh())


# # [`readme.ipynb`](readme.ipynb)
