

class apple:

    def __init__(self, *args, **kwargs):
        self.num = 5

    def test(self, num=self.num):
        print(num)


a = apple()
a.test()
