from importlib_metadata import entry_points
from typing import Iterable, Type
from xcmap.cores.plugins.interface import PluginProtocol


class PluginLoader:
    def __init__(self, group: str = "facebook"):
        self.group = group
        self._plugins: dict[str, Type[PluginProtocol]] = {}

    def discover(self) -> None:
        """发现所有可用插件"""
        try:
            eps = entry_points(group=self.group)
        except Exception as e:
            raise RuntimeError(f"Entry points loading failed: {str(e)}") from e

        for ep in eps:
            try:
                plugin_cls: Type[PluginProtocol] = ep.load()
                if not isinstance(plugin_cls, type):
                    raise TypeError(f"Invalid plugin type: {ep.name}")

                # 创建临时实例并检查协议
                temp_instance = plugin_cls()
                if not isinstance(temp_instance, PluginProtocol):
                    raise TypeError(f"Plugin {ep.name} does not conform to protocol")

                self._plugins[ep.name] = plugin_cls
            except (ImportError, AttributeError, TypeError) as e:
                print(f"Skipping invalid plugin {ep.name}: {str(e)}")

    def get_plugin(self, name: str) -> PluginProtocol:
        """获取插件实例"""
        if name not in self._plugins:
            raise KeyError(f"Plugin {name} not found")
        return self._plugins[name]()

    def get_all_plugins(self) -> Iterable[PluginProtocol]:
        """获取所有插件实例"""
        return (cls() for cls in self._plugins.values())
