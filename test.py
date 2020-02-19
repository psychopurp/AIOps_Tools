
import visualization



def test(*args,**kwargs):
    for i in args:
        print(i)
    print(kwargs)
    for i in kwargs:
        print(i)

test(1,2,3,4,a='12',b='c')

# print(a,b)