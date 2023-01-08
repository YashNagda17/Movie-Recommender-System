from django.test import TestCase

# Create your tests here.
from ml_code import Movie_Pred

dct = {1:4,
       2:5,
       3:5,
       4:3,
       5:2,
       6:1,
       7:2,
       8:5,
       9:5,
       10:2}

d = Movie_Pred(dct)
dct1 = d.run()
print(dct1)