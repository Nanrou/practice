#coding:utf8
import copy

will = ['Will',29,["Python",'C#','JavaScript']]

#wilber = will#对象id一样，属性id也一样。新对象，属性均指向旧对象。等于是镜像，旧对象发生改变，新对象也跟着改变
wilber = copy.copy(will)#对象id不一样，属性id一样。创造了一个新对象，但属性都是原来对象提供的
#注意，新对象的属性id是指向旧对象属性id，当旧对象属性变化，指向一个新id的时候，不对前者产生影响
#wilber = copy.deepcopy(will)#对象id，属性id都不一样。就是等于创建了一个一模一样的新对象

print id(will)
print will
print [id(i) for i in will]
print '-'*20
print id(wilber)
print wilber
print [id(i) for i in wilber]
print '\n'
will[0] = 'Bob'
will[2].append('XML')
print id(will)
print will
print [id(i) for i in will]
print '-'*20
print id(wilber)
print wilber
print [id(i) for i in wilber]