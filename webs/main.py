import SimpleHTTPServer
import SocketServer

PORT = 8201

class my_handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = "/var/local/www/index.html"
        try:
            f_index = open(self.path)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(f_index.read())
            f_index.close()
        except IOError:
            self.send_error(404, "Arquivo nao encontrado: %s" % self.path)
        return

try:
    httpd = SocketServer.ThreadingTCPServer(('', PORT), my_handler)

    print("servidor web rodando na porta ", PORT)
    httpd.serve_forever()

except KeyboardInterrupt:
    print("Voce pressionou ^C, encerrando...")
    httpd.socket.close()