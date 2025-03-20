def single_process():
    def decorator(func):
        func.parallel_mode = "singleProcess"
        return func
    return decorator


def multi_process():
    def decorator(func):
        func.parallel_mode = "multiProcess"
        return func
    return decorator


def generator_function():
    def decorator(func):
        func.parallel_mode = "generatorFunction"
        return func
    return decorator


def compatibility():
    def decorator(func):
        func.parallel_mode = "compatibility"
        return func
    return decorator


def global_thread():
    def decorator(func):
        func.parallel_mode = "globalThread"
        return func
    return decorator