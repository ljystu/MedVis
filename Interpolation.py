import numpy as np


"""      a = 0.6
    x0---R--x1
"""
def linear_interp(x0, x1, a):
  v=(1-a)*x0+a*x1
  return v
  
"""    a = 0.6
  x00----x01
   |   |  |
   |---R--| b = 0.4
   |   |  |
  x10----x11
"""
def bilinear_interp(x00, x01, x10, x11, a, b):
  v=x00*(1-a)*(1-b)+x01*(1-b)*a+x10*(1-a)*b+x11*a*b
  return v

"""    a = 0.6
  x00----x01
   |   |  | \
   |---R0--| b = 0.4
   |   |\ |
  x10----x11
   \      R       \
        / y00----y01
      c    | \ |  |
           |---R1--| b = 0.4
        \  |   |  |
          y10----y11
  
"""
def trilinear_interp(x00, x01, x10, x11, y00, y01, y10, y11, a, b, c):
  v=x00*(1-a)*(1-b)*(1-c)+x01*(1-b)*a*(1-c)+x10*(1-a)*b*(1-c)+x11*a*b*(1-c) + y00*(1-a)*(1-b)*(c)+y01*(1-b)*a*(c)+y10*(1-a)*b*(c)+y11*a*b*(c)
  return v
