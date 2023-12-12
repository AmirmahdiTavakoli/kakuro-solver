# This is a sample Python script.
from kakuro_solver import *
from puzzels import *
import time

kakuro = Kakuro_solver(easy1)
kakuro.print_puzzle()
start_time = time.time()
#kakuro.solve()
end_time = time.time()
kakuro.print_puzzle()
elapsed_time = end_time - start_time
print(f"The code segment took {elapsed_time:.5f} seconds to execute.")
