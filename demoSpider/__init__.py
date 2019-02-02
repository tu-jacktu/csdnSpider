# -*- coding: utf-8 -*-

# def test1():
#     var = 1
#     print(var)
#     yield var
#
# print("test1:")
# test1()

# print("next():")
# next(test1())

def test2():
    var = 1
    for i in [1,2,3]:
       var += 1
       yield var
       print("我是yield 之后的:"+str(var))
for i in test2():
    print(i)
