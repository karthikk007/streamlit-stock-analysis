# Double Checked Locking singleton pattern
import threading
 
 
class SingletonDoubleChecked(object):
 
    # resources shared by each and every
    # instance
 
    __singleton_lock = threading.Lock()
    __singleton_instance = None
 
    # define the classmethod
    @classmethod
    def instance(cls):
 
        # check for the singleton instance
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
 
        # return the singleton instance
        return cls.__singleton_instance

    # def __init__(self):
    #   """ Virtually private constructor. """
    #   if SingletonDoubleChecked.__singleton_instance != None:
    #      raise Exception("This class is a singleton!")
    #   else:
    #      SingletonDoubleChecked.__singleton_instance = self



            
        
