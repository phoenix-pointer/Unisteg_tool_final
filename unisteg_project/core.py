# src/universal_steg/core.py

import os
import importlib
from typing import Dict, List, Optional, Type
from . import file_detector

from .plugins.base import Analyzer  # your ABC


# Global registry: plugin_name -> plugin_class
_PLUGIN_REGISTRY: Dict[str, Type[Analyzer]] = {}


def _load_plugins() -> None:
    """
    Discover and register all Analyzer plugins from the plugins/package.
    Called lazily on first use.
    """
    global _PLUGIN_REGISTRY

    if _PLUGIN_REGISTRY:
        return  # already loaded

    # The package where plugins live
    package_name = "unisteg_project.plugins"
    package = importlib.import_module(package_name)
    package_path = os.path.dirname(package.__file__)  # type: ignore[attr-defined]

    for filename in os.listdir(package_path):
        # Skip non-.py files and base module
        if not filename.endswith(".py") or filename in ("__init__.py", "base.py"):
            continue

        module_name = f"{package_name}.{filename[:-3]}"
        module = importlib.import_module(module_name)

        # Convention: each plugin defines a class called Analyzer
        plugin_cls = getattr(module, "Analyzer", None)
        if plugin_cls is None:
            continue

        # Ensure it’s actually a subclass of our base Analyzer
        if not issubclass(plugin_cls, Analyzer):
            continue

        # Use the plugin's `name` as key
        _PLUGIN_REGISTRY[plugin_cls.name] = plugin_cls


def list_plugins() -> List[str]:
    """
    Return a list of available plugin names.
    """
    _load_plugins()
    return sorted(_PLUGIN_REGISTRY.keys())


def get_plugin(name: str) -> Optional[Type[Analyzer]]:
    """
    Get a plugin class by its registered name.
    """
    _load_plugins()
    return _PLUGIN_REGISTRY.get(name)


def _plugins_for_path(file_path: str) -> List[Type[Analyzer]]:
    """
    Return all plugin classes that support this file (by mimetype).
    """
    _load_plugins()
    ext = file_detector.detect_file_type(file_path)

    matches: List[Type[Analyzer]] = []
    for plugin_cls in _PLUGIN_REGISTRY.values():
        if ext in getattr(plugin_cls, "supported_mimes", []):
            matches.append(plugin_cls)

    return matches


def analyze_file(file_path: str) -> str:
    """
    Run all matching plugins on the file.
    Stops at the first plugin that detects hidden data
    and returns its extracted payload.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    candidates = _plugins_for_path(file_path)
    if not candidates:
        return "No suitable plugins for this file type."

    for plugin_cls in candidates:
        plugin = plugin_cls()
        
        print(f"[{plugin.name}] {plugin.decode(file_path)}") 
        

    


def analyze_with_plugin(file_path: str, plugin_name: str) -> str:
    """
    Force analysis with a specific plugin by name.
    """
    plugin_cls = get_plugin(plugin_name)
    if plugin_cls is None:
        return f"Plugin '{plugin_name}' not found."

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    plugin = plugin_cls()
    

    payload = plugin.decode(file_path)
    return f"[{plugin.name}] {payload}"
def encode(file_path: str, plugin_name: str, secret_data, destination: str):
    plugin_cls = get_plugin(plugin_name)
    if plugin_cls is None:
        return f"Plugin '{plugin_name}' not found."
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if plugin_name not in _plugins_for_path(file_path):
        return f"{plugin_name} is not suitable for this file type"
    plugin = plugin_cls()
    plugin.encode(file_path, secret_data, destination)