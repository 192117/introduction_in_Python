# Моё решение
import sys

digit_string = sys.argv[1]
sum = 0
for letter in digit_string:
    sum += int(letter)
print(sum)


# Решение от преподавателей
# import sys
# print(sum([int(x) for x in sys.argv[1]]))