#coding:UTF8

import BaseHTTPServer
import sys,os



class ServerException(Exception):
    pass       
class case_no_file(object):
    def test(self,handler):
        return not os.path.exists(handler.full_path)
    def act(self,handler):
        raise ServerException(" '{0}' not found".format(handler.path))

class case_existing_file(object):
    def test(self,handler):
        return os.path.isfile(handler.full_path)
    def act(self,handler):
        handler.handle_file(handler.full_path)

class case_always_fail(object):
    def test(self,handler):
        return True
    def act(self,handler):
        raise ServerException('Unkown object "{0}"'.format(handler.path))

class case_directory_index_file(object):
    def index_path(self,handler):
        return os.path.join(handler.full_path,'index.html')
    def test(self,handler):
        return os.path.isdir(handler.full_path) and\
            os.path.isfile(self.index_path(handler))
    def act(self,handler):
        handler.handle_file(self.index_path(handler))
        
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    Page = '''\
            <html>
            <body>
            <table>
            <tr>    <td>Header</td>            <td>Value</td>              </tr>
            <tr>    <td>Date and time</td>     <td>{date_time}</td>        </tr>
            <tr>    <td>Client host</td>       <td>{client_host}</td>      </tr>
            <tr>    <td>Client port</td>       <td>{client_port}</td>      </tr>
            <tr>    <td>Command</td>           <td>{command}</td>          </tr>
            <tr>    <td>Path</td>              <td>{path}</td>             </tr>
            </table>
            </body>
            </html>
        '''
    

    def create_page(self):
        values = {
            'date_time'   : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command'     : self.command,
            'path'        : self.path
            }
        page = self.Page.format(**values)#替换原字符串中{}的部分
        return page
    
    def send_content(self, content,status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    Cases = [case_no_file(),case_existing_file(),case_directory_index_file(),case_always_fail()]
    #要注意元素的次序
    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path
            self.full_path = full_path
            for case in self.Cases:
                handler = case
                if handler.test(self):
                    handler.act(self)
                    break
                
                
        except Exception as msg:
            self.handle_error(msg)
    
    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = " '{0}' cannot be read:{1}".format(self.path,msg)
            self.handle_error(msg)
    
    Error_Page = '''\
                <html>
                <body>
                <h1>Error accessing {path}</h1>
                <p>{msg}</p>
                </body>
                </html>
    '''
    def handle_error(self,msg):
        content = self.Error_Page.format(path = self.path , msg = msg)
        self.send_content(content,404)
    
    
if __name__ == '__main__':
    serverAddress = ('',8000)
    server = BaseHTTPServer.HTTPServer(serverAddress,RequestHandler)
    print 'Listening...'
    server.serve_forever()