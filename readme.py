
# coding: utf-8

# # [whereami](https://github.com/tonyfast/whereami)
# 
# <code>[https://github.com/tonyfast/whereami](https://github.com/tonyfast/whereami)</code>
# 
# Logic circuits to identify the context a notebook's derived source is executing in.
# 
# * Is Jupyter running this?
# * Is source in an Interactive session?
# * Is this a command line tool?
# 
# 
# > [Original Presentation](http://nbviewer.jupyter.org/format/slides/github/tonyfast/whereami/blob/master/whereami.ipynb#/)
# 
# ---
# 
#         ipython setup.py develop

# ## Basic usage

# In[55]:


huh = __import__('whereami').huh(globals())
huh


# ## Advanced
# 
# `whereami` contains an object `state` that contains

# In[56]:


import whereami
whereami.state


# ## IPython magic

# In[57]:


get_ipython().magic('reload_ext whereami')
get_ipython().magic('run whereami.ipynb')
get_ipython().magic('run whereami.py')


# # Developer
# 
# `whereami` contains it's own build steps.  Run that notebook in `--execute` mode by checking for `huh.JUPYTER`.

# In[58]:


get_ipython().run_cell_magic('file', 'setup.py', '__import__(\'setuptools\').setup(name="whereami", py_modules=[\'whereami\'])        ')


# In[ ]:


huh = __import__('whereami').huh(globals())
if huh.JUPYTER:
    get_ipython().system('jupyter nbconvert --to markdown --execute whereami.ipynb')
    get_ipython().system('python -m doctest whereami.py')
    get_ipython().system('python -m pydoc -w whereami')
    get_ipython().system('jupyter nbconvert --to python readme.ipynb')
    get_ipython().system('jupyter nbconvert --to markdown readme.ipynb')
    get_ipython().system('jupyter nbconvert index.ipynb')


# `whereami` as a package.

# In[60]:


if huh.MAIN and not huh.JUPYTER:
    get_ipython().system('ipython setup.py develop')

