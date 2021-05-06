class Task2:
    def run_task(self):
        print("Set sequence length")
        length = input()
        if length.isnumeric():
            length = int(length)
            prev_vals = [0, 1]
            for i in range(2):
                print("{}-th value is {}".format(i, i))
            for i in range(1, length + 1):
                new_val = prev_vals[0] + prev_vals[1]
                prev_vals[0] = prev_vals[1]
                prev_vals[1] = new_val
                print("{}-th value is {}".format(i, new_val))
        else:
            raise ValueError("Input must be numerical")
        return

       

def fib(length):
    a, b = 0, 1
    for _ in range(length):
        yield a
        a, b = b, a + b

print(list(fib(10)))
