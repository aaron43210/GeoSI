# -*- coding: utf-8 -*-
"""
GeoSI Engine — Tool Registry

This module defines the ToolRegistry, which is the central hub for discovering
and executing all GIS tools in the GeoSI engine. It handles:
    1. Tool Discovery: Finding tools in the tools/ directory.
    2. Tool Registration: Mapping tool names to their implementation classes.
    3. Tool Execution: Providing a standard interface to run any tool.

The registry is used by the Agent to see what's possible, and by the Executor
to run the steps in an execution plan.

See FILE_CONNECTIONS.md:
    - IMPORTS FROM: base.py, models.py, tools/*.py
    - USED BY: agent.py, executor.py, geosi_plugin/, geosi_server/
"""

import importlib
import inspect
import pkgutil
from typing import Dict, List, Optional, Type

from geosi_engine.base import GISTool, BackendTool, PortableTool, QGISProcessingTool
from geosi_engine.models import ToolSpec, ToolResult

_BASE_CLASSES = {GISTool, BackendTool, PortableTool, QGISProcessingTool}


class ToolRegistry:
    """
    Central registry for all GIS tools in the GeoSI engine.

    The registry maintains a mapping of tool names to GISTool instances.
    When initialized, it automatically discovers and registers all tools
    defined in the geosi_engine.tools package.

    Attributes:
        _tools: Dictionary mapping tool names to GISTool instances.
    """

    def __init__(self, auto_discover: bool = True):
        """
        Initialize the tool registry.

        Args:
            auto_discover: If True, automatically find and register tools
                           from the geosi_engine.tools package.
        """
        self._tools: Dict[str, GISTool] = {}
        if auto_discover:
            self.discover_tools()

    def register_tool(self, tool: GISTool) -> None:
        """
        Register a single tool instance.

        Args:
            tool: An instance of a GISTool subclass.
        """
        spec = tool.spec()
        self._tools[spec.name] = tool

    def discover_tools(self) -> None:
        """
        Automatically discover and register all tools in geosi_engine.tools.

        This method walks through all modules in the geosi_engine.tools
        package, finds any class that inherits from GISTool (and is not
        GISTool itself or other abstract bases), and registers an instance.
        """
        import geosi_engine.tools as tools_pkg

        # Walk through all modules in the tools package
        for _, modname, ispkg in pkgutil.walk_packages(
            tools_pkg.__path__, tools_pkg.__name__ + "."
        ):
            if ispkg:
                continue

            try:
                # Import the module
                module = importlib.import_module(modname)

                # Find all GISTool subclasses in the module
                for name, obj in inspect.getmembers(module):
                    if (
                        inspect.isclass(obj)
                        and issubclass(obj, GISTool)
                        and not inspect.isabstract(obj)
                        and obj not in _BASE_CLASSES
                    ):
                        # Create an instance and register it
                        try:
                            tool_instance = obj()
                            self.register_tool(tool_instance)
                        except Exception as e:
                            print(f"Error registering tool {name} from {modname}: {e}")

            except Exception as e:
                print(f"Error importing module {modname}: {e}")

    def get_tool(self, name: str) -> Optional[GISTool]:
        """
        Get a tool instance by its name.

        Args:
            name: Unique name of the tool (from its spec).

        Returns:
            The GISTool instance, or None if not found.
        """
        return self._tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[ToolSpec]:
        """
        List the specifications of all registered tools.

        Args:
            category: Optional category to filter by (e.g., "vector", "raster").

        Returns:
            List of ToolSpec objects.
        """
        specs = [tool.spec() for tool in self._tools.values()]
        if category:
            specs = [s for s in specs if s.category == category]
        return specs

    def execute_tool(self, name: str, **kwargs) -> ToolResult:
        """
        Execute a tool by name with the given parameters.

        This is a convenience method that finds the tool and calls
        its safe_execute() method.

        Args:
            name: Unique name of the tool.
            **kwargs: Parameters for the tool.

        Returns:
            ToolResult with the output or error.
        """
        tool = self.get_tool(name)
        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{name}' not found in registry",
                message=f"Execution failed: unknown tool"
            )

        return tool.safe_execute(**kwargs)
