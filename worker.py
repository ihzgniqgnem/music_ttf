import threading
class worker():
    def __init__(self, func, *args, **kwargs):
        def func_(*args,**kwargs):
            self.result = func(*args,**kwargs)
            self.running=False
        self.func = func_
        self.args = args
        self.kwargs = kwargs
        class none_type:
            def __eq__(self, other):
                if type(other)==none_type:return 0
                else:return 1
        self.none_type=none_type
        self.result = self.none_type
        self.running = False
    def get(self):
        if (not self.running)and (self.result == self.none_type):self.run(*self.args,**self.kwargs)
        if self.running:self.thread.join()
        result = self.result
        self.result = self.none_type
        return result
    def run(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        self.thread = threading.Thread(target=self.func, args=args, kwargs=kwargs)
        self.thread.start()
        self.running = True
        return self