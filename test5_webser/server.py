#coding:UTF8

import BaseHTTPServer
import sys,os


#-------------------------------------------------------------
class ServerException(Exception):
    ''' 创建异常类。'''
    pass       
#-------------------------------------------------------------

#-------------------------------------------------------------
class base_case(object):
    def handle_file(self,handler,full_path):#处理静态文件
        try:
            with open(full_path,'rb') as reader:#打开所请求的文件
                content = reader.read()#直接read可能会有爆内存的风险
            handler.send_content(content)#给回主函数输入页面
        except IOError as msg:#处理IO异常
            msg = " '{0}' cannot be read:{1}".format(full_path,msg)#将文件路径和错误信息加在一起
            handler.handle_error(msg)#返回给主函数的异常处理函数
    
    def index_path(self,handler):
        return os.path.join(handler.full_path,'index.html')#将这个索引文件名加到路径的后面
    
    def test(self,handler):
        assert False,'Not implemented.'
    def act(self,handler):
        assert False,'Not implemented.'
#-------------------------------------------------------------

#-------------------------------------------------------------
class case_no_file(base_case):
    ''' 处理不存在的路径请求。'''
    def test(self,handler):
        return not os.path.exists(handler.full_path)#判断是否存在。存在为flase；不存在为true
    def act(self,handler):
        raise ServerException(" '{0}' not found".format(handler.path))#不存在的话，返回一个带信息的异常
#-------------------------------------------------------------

#-------------------------------------------------------------
class case_existing_file(base_case):
    ''' 处理存在的文件请求。'''
    def test(self,handler):
        return os.path.isfile(handler.full_path)#如果是文件就返回true
    def act(self,handler):
        self.handle_file(handler,handler.full_path)#直接用父类处理静态文件的方法处理
#-------------------------------------------------------------

#-------------------------------------------------------------
class case_always_fail(base_case):
    '''所有情况都不符合时的默认处理类。'''
    def test(self,handler):
        return True
    def act(self,handler):
        raise ServerException('Unkown object "{0}"'.format(handler.path))#抛出异常
#-------------------------------------------------------------

#-------------------------------------------------------------
class case_directory_index_file(base_case):
    ''' 处理索引页的请求。'''
    def test(self,handler):
        return os.path.isdir(handler.full_path) and\
            os.path.isfile(self.index_path(handler))#存在路径和该路径导向的是文件
    def act(self,handler):
        self.handle_file(handler,self.index_path(handler))#处理index.html文件
#-------------------------------------------------------------

#-------------------------------------------------------------
import subprocess
class case_cgi_file(base_case):
    ''' CGI？处理脚本文件的类'''
    def test(self,handler):
        return os.path.isfile(handler.full_path) and \
            handler.full_path.endswith('.py')#判断是否路径导向文件，并且判断是不是py文件
    
    def act(self,handler):
        self.run_cgi(handler)
    
    def run_cgi(self,handler):
      data = subprocess.check_output(['python',handler.full_path])#运行脚本文件
      handler.send_content(data)#返回数据给主函数处理
#-------------------------------------------------------------

#-------------------------------------------------------------
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    ''' 相应的主体函数，继承基础httpserver。'''
    
    Cases = [case_no_file(),case_cgi_file(),case_existing_file(),case_directory_index_file(),case_always_fail()]
    #要注意元素的次序
    #先判断是否存在对应路径，然后是运行脚本，然后是响应静态文件，然后是默认页（这个应该可以包到前面那个类里面去），所有都不的处理方法，因为直接是返回true，所以必须放到最后
    def do_GET(self):
        try:
            self.full_path = os.getcwd() + self.path#前者是当前工作目录，后者是请求的相对路径。后者是父类里面已经封装好的属性

            for case in self.Cases:#遍历事件的类，再通过统一接口调用
                if case.test(self):
                    case.act(self)
                    break
                
        except Exception as msg:#处理异常
            self.handle_error(msg)
    #异常界面
    Error_Page = '''\
                <html>
                <body>
                <h1>Error accessing {path}</h1>
                <p>{msg}</p>
                </body>
                </html>
    '''
    def handle_error(self,msg):#处理异常的函数
        content = self.Error_Page.format(path = self.path , msg = msg)
        self.send_content(content,404)        
        
            
    def send_content(self, content,status=200):#形成界面
        self.send_response(status)#返回状态码
        self.send_header('Content-type', 'text/html')#告诉客户端要用处理html文件的方式处理返回的内容
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()#插入空白行来结束头部
        self.wfile.write(content)        

#-------------------------------------------------------------
    
if __name__ == '__main__':
    serverAddress = ('',8000)#设置为本地的8000端口
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    print 'Listening...'
    server.serve_forever()