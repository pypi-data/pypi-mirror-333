from abc import ABC, abstractmethod


class BaseTool(ABC):
    
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