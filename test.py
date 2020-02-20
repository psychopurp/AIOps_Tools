
import common_tools as ct


def test(a):
    b = a
    b[0] = 'test'
    print(a, id(a))
    print(b, id(b))
    return a


if __name__ == "__main__":
    data_handler = ct.DataHandler('./data/1/1_7days.txt')
    x, y = data_handler.get_data()
    dta = ct.date_to_series(x, y)
    ts = ct.diff_smooth(dta)
    # print(ts)
    print(ts['2020-02-13 23:30'])
