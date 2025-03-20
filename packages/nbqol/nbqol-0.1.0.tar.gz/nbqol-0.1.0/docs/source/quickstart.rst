Quickstart
==========

NB-QOL provides various utilities to enhance your Jupyter notebook workflow. Here are some common use cases:

CUDA Device Management
-------------------------

Check and manage your CUDA devices:

.. code-block:: python

   from nbqol import devices
   
   # List all available CUDA devices
   devices.cuda_device_report()
   
   # Select specific CUDA devices to use
   devices.set_cuda_visibles(0, 1)  # Use CUDA devices 0 and 1

IPython Configuration
------------------------

Configure IPython environment:

.. code-block:: python

   from nbqol import settings
   
   # Enable autoreload to automatically reload modules during development
   settings.set_autoreload('complete')
   
   # Hide warning messages
   settings.hide_warnings()
   
   # Get environment settings
   env_settings = settings.get_main_env_settings()

Path Operations
----------------

Work with notebook paths:

.. code-block:: python

   from nbqol import path_op
   
   # Get the path of the current notebook
   nb_path = path_op.notebook_path()
   
   # Find the Git repository root
   git_root = path_op.path_to_git_root()

Styling Notebooks
-------------------

Apply CSS styling to your notebooks:

.. code-block:: python

   from nbqol import stylizer
   
   # Apply VS Code style
   stylizer.apply_vscode_style()