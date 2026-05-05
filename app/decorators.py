

def fence(func):
    def wrapper(*args, **kwargs):
        print("Entering the fence...")
        result = func(*args, **kwargs)
        print("Exiting the fence...")
        return result
    return wrapper

@fence
def log(a:int, b:list[int]):
  
  print("Logging... Value:", a, "List:", b)

log(1, [2, 3, 4])