"""
Dynamic Plugin Marketplace Loader for NexusAI OS.
Scans local plugins/ folder, parses plugin manifests, and automatically discovers & registers tools.
"""
import json
import logging
import os
from typing import Any, Dict, List

from nexusai.mcp.engine import discovery_engine
from nexusai.mcp.registry import ToolMetadata, RiskLevel, tool_registry

logger = logging.getLogger("nexusai.mcp_plugins")


class PluginMarketplaceLoader:
    """Scans plugins directory and auto-loads plugin tools."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = plugins_dir
        self.registry = tool_registry

    async def scan_and_load_plugins() -> List[Dict[str, Any]]:
        """Scans plugins folder for plugin manifests."""
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir, exist_ok=True)

        loaded_plugins = []
        for root, dirs, files in os.walk(self.plugins_dir):
            for f in files:
                if f.endswith("manifest.json") or f.endswith("plugin.json"):
                    manifest_path = os.path.join(root, f)
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as pf:
                            manifest = json.load(pf)
                            loaded_plugins.append(manifest)

                            # Register plugin tool into ToolRegistry
                            tool_id = manifest.get("id") or f"plugin_{manifest.get('name', 'custom')}"
                            meta = ToolMetadata(
                                tool_id=tool_id,
                                tool_name=manifest.get("name", "Custom Plugin Tool"),
                                provider="plugin-marketplace",
                                description=manifest.get("description", "Dynamic plugin tool"),
                                permissions=manifest.get("permissions", []),
                                risk_level=RiskLevel.LOW
                            )
                            self.registry.register_tool(meta)
                            logger.info(f"Loaded plugin manifest: {manifest.get('name')} ({tool_id})")
                    except Exception as exc:
                        logger.error(f"Error loading plugin manifest at {manifest_path}: {exc}")

        # Also trigger discovery of core tools
        await discovery_engine.discover_and_index_all_tools()
        return loaded_plugins


plugin_marketplace_loader = PluginMarketplaceLoader()
