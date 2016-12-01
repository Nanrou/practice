#coding:utf8

from app import app 
#在app文件夹下创建__init__.py,使其变成一个可以被引用的包。
#现在就可以直接导入来使用了
#思路：将程序的逻辑部分单独打包，以防混乱。
app.run(debug=True,port=8000)#直接运行