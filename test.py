
def decor(func):
    def wrap(text):
        print("============")
        func(text)
        print("============")
    return wrap

@decor
def print_text(text):
    print(text)
    
print_text("hi")