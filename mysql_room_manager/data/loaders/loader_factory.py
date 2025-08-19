from typing import Dict, Type, List

from ...interfaces.loader_interface import LoaderInterface
from ...exceptions.exceptions import UnsupportedFormatError
from .json_loader import JsonLoader


class LoaderFactory: 
    
    _loaders: Dict[str, Type[LoaderInterface]] = {
        'json': JsonLoader,
    }
    
    @classmethod
    def create_loader(cls, format_name: str) -> LoaderInterface:
        format_lower = format_name.lower()
        loader_class = cls._loaders.get(format_lower)
        
        if not loader_class:
            supported = list(cls._loaders.keys())
            raise UnsupportedFormatError(format_name, supported)
        
        return loader_class()
    
    @classmethod
    def get_supported_formats(cls) -> List[str]:
        return list(cls._loaders.keys())

