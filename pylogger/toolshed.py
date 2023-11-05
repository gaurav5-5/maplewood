import os
from re import M
from .chainsaw import Chainsaw

class ToolShed:
    
    __log_dir : str = ""
    __logs    : dict[str, Chainsaw]
    
    def __init__(self, log_dir : str):
        
        self.__logs = dict[str, Chainsaw]()
        self.__log_dir = log_dir
        try:
            os.makedirs(log_dir)
        except OSError:
            pass
    
    def write(self, lname:str, message:str):
        if lname in self.__logs.keys():
            self.__logs[lname].write(message=message)
        
    def new_no_open(self,
            fname:str='',
            fmt_str:str='',
            success_msg:str='', 
            failure_msg:str='',
            module:str=''
        ) -> Chainsaw:
        
        if fname in self.__logs.keys():
            raise RuntimeError(f"Log {fname} already exists")
        
        key = fname
        fname = fname + '.txt' if '.txt' not in fname else fname
        
        log = Chainsaw(fdir=self.__log_dir, fname=fname,
                           format=fmt_str,
                           success_msg=success_msg, failure_msg=failure_msg,
                           module=module)
        self.__logs[key] = log
        
        return log
    
    def new(self,
            fname:str='',
            fmt_str:str='',
            success_msg:str='', 
            failure_msg:str='',
            module:str=''
        ) -> Chainsaw:
        
        log = self.new_no_open(fname=fname, fmt_str=fmt_str, success_msg=success_msg,
                               failure_msg=failure_msg, module=module)
        log.open()
        return log
    
    
    def get_dir(self) -> str:
        return self.__log_dir
    
    def get_logs(self) -> dict[str, Chainsaw]:
        return self.__logs
    
    def get_log(self, name:str) -> Chainsaw:
        if name in self.__logs.keys():
            return self.__logs[name]
        else:
            raise( KeyError(f"{name} not initialized"))
    
    def get_log_status(self, name:str) -> bool:
        if name in self.get_logs().keys():
            return self.__logs[name].is_open()
        else:
            raise( KeyError(f"{name} not initialized"))
    
    def remove(self, name:str):
        if name in self.__logs.keys():
            if self.__logs[name].is_open():
                self.__logs[name].close()
            del self.__logs[name]
        else:
            raise( KeyError(f"{name} not initialized"))
    
    def close_all(self):
        for k, log in self.__logs.items():
            if log.is_open():
                log.close()
            
    def close(self, name:str):
        if name not in self.get_logs().keys():
            raise KeyError(f'Log {name} not initialized')
        try:
            self.__logs[name].close()
        except Exception as e:
            print(e)