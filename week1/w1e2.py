# Моё решение
import sys

stairs = int(sys.argv[1])

for step in range(stairs):
    print(" " * (stairs - step - 1), "#" * (step + 1), sep="")


# Решение от преподавателей
# import sys
#
# num_steps = int(sys.argv[1])
#
# for i in range(num_steps):
#     print(" " * (num_steps - i - 1), "#" * (i + 1), sep="")