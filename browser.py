import socket
import ssl

class URL:
    def __init__(self, url=None):

        if url == None:
            self.path = "testforbrowser.txt"
            self.scheme = "file"
            return

        self.scheme, url = url.split("://", 1)
        print(self.scheme, "this is self.scheme")
        assert self.scheme in ["http", "https", "file"]

        if "/" not in url:
            url = url + "/"
        
        self.host, url = url.split("/", 1)

        if self.scheme == "file":
            self.path = self.host + url
            print(self.path, "this is self.path")
            self.host = None
            self.port = None
            return

        if ":" in self.host:
            self.host, port = self.host.split(":", 1)
            self.port = int(port)

        self.path = "/" + url

        if self.scheme == "http":
            self.port = 80
        elif self.scheme == "https":
            self.port = 443

    def request(self):

        if self.scheme == "file":

            file_path = "/home/suojaola/" + self.path
            print(file_path, "this is file_path")

            with open(file_path, "r") as f:
                content = f.read()
                return content

        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )

        # remember to make it easier to add headers

        self.connection = "close"
        self.user_agent = "abc"

        s.connect((self.host, self.port))
        if self.scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=self.host)

        request = "GET {} HTTP/1.1\r\n".format(self.path)
        request += "Host: {}\r\n".format(self.host)
        request += "Connection: {}\r\n".format(self.connection)
        request += "User-Agent: {}\r\n".format(self.user_agent)
        request += "\r\n"
        s.send(request.encode("utf8"))

        response = s.makefile("r", encoding="utf8", newline="\r\n")
        statusline = response.readline()
        version, status, explanation = statusline.split(" ", 2)

        response_headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            response_headers[header.casefold()] = value.strip()
        assert "transfer-encoding" not in response_headers
        assert "content-encoding" not in response_headers
        content = response.read()
        s.close()

        return content

def show(body):
    in_tag = False
    for i in body:
        if i == "<":
            in_tag = True
        elif i == ">":
            in_tag = False
        elif not in_tag:
            print(i, end="")

def load(url):
    body = url.request()
    show(body)

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        load(URL(sys.argv[1]))
    
    else:
        load(URL(None))



        
