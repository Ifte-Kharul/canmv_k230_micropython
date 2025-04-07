from ulab import numpy as np

rng = np.random.Generator(123456)
print(rng)

# returning new objects
print(rng.random())
print('\n', rng.random(size=(3,3)))

# supplying a buffer
a = np.array(range(9), dtype=np.float).reshape((3,3))
print('\nbuffer array before:\n', a)
rng.random(out=a)
print('\nbuffer array after:\n', a)
