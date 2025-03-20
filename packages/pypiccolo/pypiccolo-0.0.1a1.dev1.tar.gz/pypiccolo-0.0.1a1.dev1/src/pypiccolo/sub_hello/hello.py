from ..hello import hello as super_hello

def hello(use_super=False):
    if use_super:
        return super_hello()
    return 'Hello, world!'

def say_hello(use_super=False):
    print(hello(use_super=use_super))