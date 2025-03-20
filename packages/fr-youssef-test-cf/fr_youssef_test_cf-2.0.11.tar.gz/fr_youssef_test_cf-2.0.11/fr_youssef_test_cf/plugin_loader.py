import logging
import importlib
import pkgutil

def snake_to_camel_case(snake_str: str) -> str:
    # Split the string by underscores
    words = snake_str.split('_')

    # Capitalize each word and join them together
    camel_case_str = ''.join(word.capitalize() for word in words)

    return camel_case_str

def load_plugins() -> dict:
    plugins = {}
    package = 'plugins'

    logging.info(f'Loading package: {package}')

    for _, name, _ in pkgutil.iter_modules([package.replace('.', '/')]):
        logging.debug(f'Found module: {name}')
        
        module = importlib.import_module(f"{package}.{name}.{name}_data_source_plugin")
        class_attr_name = snake_to_camel_case(name) + 'DataSourcePlugin'

        if hasattr(module, class_attr_name):
            plugin_class = getattr(module, class_attr_name)
            plugins[name] = plugin_class

    logging.debug(f'Loaded modules: {list(plugins.keys())}')
    
    return plugins