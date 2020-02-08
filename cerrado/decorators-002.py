def call(x):
    def decorator(func):
        return print(func(x))
    return decorator


@call(42)
def start(x):
    version = x / 100
    print("Hello World!")
    print(f"Iniciando meu programa {version}")
    return version
