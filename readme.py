
# coding: utf-8

# # whereami
# 
# Logic circuits to identify the context a notebook's derived source is executing in.
# 
# * Is Jupyter running this?
# * Is source in an Interactive session?
# * Is this a command line tool?

# ## Basic usage

# In[40]:


huh = __import__('whereami').huh(globals())
huh


# ## Advanced
# 
# `whereami` contains an object `state` that contains

# In[7]:


import whereami
whereami.state


# ## IPython magic

# In[6]:


get_ipython().magic('reload_ext whereami')


# In[16]:


get_ipython().magic('run whereami.ipynb')


# In[22]:


get_ipython().magic('run whereami.py')


# In[23]:


get_ipython().magic('run -n whereami.py')


# # Developer
# 
# `whereami` contains it's own build steps.  Run that notebook in `--execute` mode by checking for `huh.JUPYTER`.

# In[43]:


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
elif huh.MAIN:
    get_ipython().system('ipython setup.py develop')

