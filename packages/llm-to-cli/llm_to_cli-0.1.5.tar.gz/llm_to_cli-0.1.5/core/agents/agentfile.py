from abc import ABC, abstractmethod
from .tools import BaseTool


class BaseAgent(ABC):
    tools:list[BaseTool] = []
    
    @abstractmethod
    def _run(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def _arun(self, *args, **kwargs):
        raise NotImplementedError
    
    def run(self, *args, **kwargs):
        return self._run(*args, **kwargs)
    
    async def arun(self, *arg, **kargs):
        return await self._arun(arg, kargs)
    
    