from typing import Dict, Type, List

from ...interfaces.data_loader_interface import DataLoaderInterface
from ...exceptions.custom_exceptions import UnsupportedFormatError
from .json_data_loader import JSONDataLoader


class DataLoaderFactory:
    
    _loaders: Dict[str, Type[DataLoaderInterface]] = {
        'json': JSONDataLoader,
    }
    
    @classmethod
    def create_loader(cls, format_name: str) -> DataLoaderInterface:
        format_lower = format_name.lower()
        loader_class = cls._loaders.get(format_lower)
        
        if not loader_class:
            supported = list(cls._loaders.keys())
            raise UnsupportedFormatError(format_name, supported)
        
        return loader_class()
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        return list(cls._loaders.keys())

