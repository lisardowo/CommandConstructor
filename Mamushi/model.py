

#Let me give yall a heads up this is sum completely clauded shi
#Ill be taking a look back at this later but rn I can not say mucho about how it works

#DA FUCK DOES @runtime_checkable MEANS



from typing import Optional, Protocol, runtime_checkable
from .msg import Msg
from .commands import Cmd

@runtime_checkable
class Model(Protocol):
    def init(self) -> Optional[Cmd]:
        # Ellipsis(...) Is supposed to represent this is empty on purpose
        # Basically all of this models are not like actually something to be used
        # Its simply a "template" so the interpreter can check that the model that is 
        # in fact to be rendered has the same attributes
        ...
    
    def update(self, msg: Msg) -> Optional[Cmd]:
        
        ...
        
    def view(self) -> str:
        
        ...
        
class BaseModel:
    
    def init(self) -> Optional[Cmd]:
        return None
    def update(self, msg:Msg) -> Optional[Cmd]:
        raise NotImplementedError
    def view(self) -> str:
        raise NotImplementedError