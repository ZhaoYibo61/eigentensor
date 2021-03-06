#!/usr/bin/env python
# coding: UTF-8
from __future__ import division
import pylab
from build.multivariate_transition_tensor import mtt
import settings
from utils.sequence import init_data
from utils.tensor import tensor_three_mode_product, delta_tensor_norm, get_check_tensor


if __name__ == '__main__':
    # beijing = (39.433333, 41.05, 115.416667, 117.5)
    # haidian = (39.883333, 40.15, 116.05, 116.383333)
    region = (39.883333, 40.05, 116.05, 116.383333)
    filter_count = 600
    time_num = settings.TIME_SLICE
    train_percent = 0.1

    x_values = []
    y_values = []

    order = 1
    while train_percent < 1:
        data, axis_users, axis_pois, check_data = init_data(region, filter_count, train_percent)
        user_num = len(axis_users)
        poi_num = len(axis_pois)

        transition_tensor = mtt(data, user_num, poi_num)

        # equal_all_sum_one: equal
        init_tensor1 = [[[1/(poi_num * time_num * user_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]
        # user_slice_sum_one: equal
        init_tensor4 = [[[1/(poi_num * time_num) for i in range(poi_num)] for j in range(time_num)] for k in range(user_num)]

        res, iterator_values = tensor_three_mode_product(transition_tensor, init_tensor1)
        # print res

        check_tensor = get_check_tensor(check_data, user_num, time_num, poi_num)
        residual = delta_tensor_norm(res, check_tensor)

        x_values.append(train_percent)
        y_values.append(residual)
        train_percent += 0.1

    pylab.plot(x_values, y_values, 'rs', linewidth=1, linestyle="-", label=u"训练集比重")
    pylab.xlabel(u"训练集比重")
    pylab.ylabel(u"准确率")
    pylab.title(u"训练集比重与准确率的关系")
    pylab.legend(loc='center right')
    pylab.show()