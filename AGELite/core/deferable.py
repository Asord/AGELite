from typing import Callable

class Deferable:
    """
    Allow to defer the execution of a function. Usefull if calling the function is costly or need to access locked data (ie. from GPU).

    Usage:

        class MyClass(Deferable):
            def __init__(self):
                super().__init__([<Optional: queues names>]) # order is respected if using run_all

            @Deferable.defer(<queue name>) # called from run(<queue name>) or run_all
            def something_defered(self, ...): pass
        
        m = MyClass()
        m.something_defered()
        ...
        m.run_all() # or m.run(<queue name>)
        """


    def __init__(self, queues: list[str|int]=None):
        if queues is None or len(queues) == 0:
            self._q = {0: []}
        else:
            self._q = {i: [] for i in queues}

    def _defer(self, func: Callable, queue_name: str|int=0):
        """ Add a function to a queue. Please use @Deferable.defer() instead. """
        self._q[queue_name].append(func)

    def exec(self, queue_name: str|int|None=None):
        """ Execute all functions from all queues if queue_name is not specified else execute all functions from the specified queue """
        if queue_name is None:
            self.run_all()
        else:
            self.run(queue_name)

    def run(self, queue_name: str|int=0):
        """ Execute all functions in the specified queue """
        if queue_name not in self._q or len(self._q[queue_name]) == 0:
            return
        
        [func() for func in self._q[queue_name]]
        self._q[queue_name].clear()

    def run_all(self):
        """ Execute all functions in all queues """
        if len(self._q) == 0:
            return
        [self.run(q) for q in self._q]
            
    def clear(self, queue_name: str|int|None=None):
        """ Clear all queues if queue_name is not specified else clear only the specified queue """
        if queue_name is None:
            [self._q[qname].clear() for qname in self._q]
        else:
            self._q[queue_name].clear()

    def defer(queue_name: str):
        """ defer a function to a queue """
        def decorator(func: Callable):
            def wrapper(self: 'Deferable', *args, **kwargs):
                if type(queue_name) in [int, str]:
                    if queue_name not in self._q:
                        self._q[queue_name] = []
                self._defer(lambda:func(self, *args, **kwargs), queue_name)
                return None
            return wrapper
        return decorator
    

if __name__ == "__main__":
    class Test(Deferable):
        def __init__(self):
            super().__init__(["q2", "q1"]) # <- order is important

        @Deferable.defer("q1") # called from run("q1") or run_all
        def q1(self):
            print("q1")

        @Deferable.defer("q2") # called from run("q2") or run_all
        def q2(self):
            print("q2")

    t = Test()

    t.q1()
    t.q2()
    print("run all:"); t.run_all()    # expected output: q2, q1

    t.q1()
    t.q1()
    print("Run q2:"); t.run("q2")     # expected none outputs
    print("Run q1:"); t.run("q1")     # expected output: q1, q1

    t.q1()
    t.clear()
    t.q2()
    print("run all:"); t.run_all()

    """ expected output: 
    run all
    q2
    q1
    Run q2
    Run q1
    q1
    q1
    run all
    q2
    """