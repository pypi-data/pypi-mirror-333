"""
NB-QOL: Quality of Life tools for Jupyter Notebooks

A cross-platform, modular toolkit for enhancing the Jupyter notebook experience.
"""

__version__ = '0.1.0'

from . import devices
from . import outputs
from . import path_op
from . import settings
from . import stylizer

from .settings import (
    set_autoreload,
    hide_warnings,
    get_main_env_settings,
    save_main_env_settings_to_json,
)

from .devices import (
    set_cuda_visibles,
    cuda_visibles,
    count_cuda_devices,
    cuda_device_report,
)

from .path_op import (
    notebook_path,
    path_to_git_root,
    add_git_root_to_sys_path,
    diffpath,
)

from .outputs import (
    capture_output,
)

from .stylizer import (
    auto_style,
    is_running_in_jupyter,
    is_running_in_vscode,
    is_running_in_vscode_jupyter,
)

__all__ = [
    # Modules
    'devices',
    'outputs',
    'path_op',
    'settings',
    'stylizer',
    
    # Settings functions
    'set_autoreload',
    'hide_warnings',
    'get_main_env_settings',
    'save_main_env_settings_to_json',
    
    # Device functions
    'set_cuda_visibles',
    'cuda_visibles', 
    'count_cuda_devices',
    'cuda_device_report',
    
    # Path functions
    'notebook_path',
    'path_to_git_root',
    'add_git_root_to_sys_path',
    'diffpath',
    
    # Output functions
    'capture_output',
    
    # Stylizer functions
    'auto_style',
    'is_running_in_jupyter',
    'is_running_in_vscode',
    'is_running_in_vscode_jupyter',
]

