

#############################################################################################################
###
### Programming tools and introspection
###
#############################################################################################################

import time
from .bpyth_human import human_readable_seconds

class runstat:
    '''
    wraps a function, to keep a running count of how many times it's been called

    Example:
        print_with_stat = runstat(print)        # or decoreate your function with @runstat
        print_with_stat()                       # now works like print
        print_with_stat.time_since_last_call()  # When was the function last called?
        print_with_stat.count                   # How often has the function been called?
    
    '''

    def __init__(self, func):
        """
        Initializes the runstat decorator.

        Args:
            func: The function to be wrapped.
        """
        self.func = func
        self.count = 0
        self.last_call_time = None

    def time_since_last_call(self):
        """
        Returns the time elapsed (in seconds) since the last call to the wrapped function.

        Returns:
            str: The time elapsed
        """
        if self.last_call_time is None:
            return 0.0
        result = human_readable_seconds(time.perf_counter() - self.last_call_time)
        return result # "{} sec".format(result)


    def __call__(self, *args, **kwargs):
        """
        Calls the wrapped function and updates the statistics.

        Args:
            *args: Positional arguments to pass to the wrapped function.
            **kwargs: Keyword arguments to pass to the wrapped function.

        Returns:
            The return value of the wrapped function.
        """
        self.count += 1
        self.last_call_time  = time.perf_counter()
        return self.func(*args, **kwargs)
    



def raise_if(error):
# ---------------------------------------------------------------------------------------------       
    if error:
        raise Exception(error)    
# ---------------------------------------------------------------------------------------------      



    

    
 
    