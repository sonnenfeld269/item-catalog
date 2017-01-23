from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_service import *

#### Handler
class webserverHandler(BaseHTTPRequestHandler):
    """Decides what code to execute based on the HTTP Request from the client.
    """

    output = ""

    def do_GET(self):
        """Creates responses based on the get requests from the client.
        """

        try:
            self.doBefore()
            if self.path.endswith("/hello"):
                self.output += """Hello!<form method='POST' enctype='multipart/form-data' action='/
                hello'><h2>What would you like me to say?</h2><input
                name='message' type='text'><input type='submit' value='Submit'></form>"""
            elif self.path.endswith("/restaurants"):
                self.output += "<a href='restaurants/new'>Make a new restaurant</a><br><br>"
                for restaurant in readAllRestaurants():
                    self.output += restaurant.name + """
                    <br><a href='restaurants/%s/edit'>Edit</a>
                    <br><a href='restaurants/%s/delete'>Delete</a>
                    <br>
                    <br>
                    """ % (restaurant.id,restaurant.id)
            elif self.path.endswith("/restaurants/new"):
                self.output += """<h2>Create restaurant</h2>
                <form method='POST' enctype='multipart/form-data'
                action='/restaurants/new'>
                    <input name='restaurant_name' type='text'>
                    <input type='submit' value='Create'>
                </form>"""
            elif self.path.endswith("/edit"):
                self.output += """<h2>%s</h2>
                <form method='POST' enctype='multipart/form-data'
                action='/restaurants/%s/edit'>
                    <input name='restaurant_name' type='text'>
                    <input type='submit' value='Edit'>
                </form>
                """ % (readRestaurantById(self.path.split("/")[2]).name, self.path.split("/")[2])
            elif self.path.endswith("/delete"):
                self.output += """<h2>do u really want to delete?</h2>
                <form method='POST' enctype='multipart/form-data'
                action='/restaurants/%s/delete'>
                    <input type='submit' value='Delete'>
                </form>
                """ % self.path.split("/")[2]
            self.doAfter()
        except IOError:
            self.send_error(404,"file not found %s" % self.path)

    def do_POST(self):
        """Creates responses based on the post requests from the client.
        """
        try:
            if self.path.endswith("/restaurants/new"):
                restaurant_name = self.getMessageContent("restaurant_name")
                createRestaurant(name=restaurant_name)
                self.doAfterPost("/restaurants")
            elif self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                deleteRestaurant(restaurant_id)
                self.doAfterPost("/restaurants")
            elif self.path.endswith("/edit"):
                restaurant_name = self.getMessageContent("restaurant_name")
                restaurant_id = self.path.split("/")[2]
                updateRestaurant(restaurant_id,restaurant_name)
                self.doAfterPost("/restaurants")

        except:
            pass

    def doBefore(self):
        """Executes at the beginning of a get request"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.output += "<html><body>"

    def doAfter(self):
        """Executes at the end of a get request"""

        self.output += "</html></body>"
        self.wfile.write(self.output)

    def getMessageContent(self, fieldname):
        """Extracts form data and returns the message content. This method should
        be called at the beginning of each post request.

        Args:
            fieldname: name of the form field

        Returns:
            messagecontent[0]: the content of the fields
        """

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            fields=cgi.parse_multipart(self.rfile, pdict)
        messagecontent = fields.get(fieldname)
        return messagecontent[0]

    def doAfterPost(self, redirectTo):
        """Executes at the end of a post request.

        Args:
            redirectTo: path to the redirect url
        """
        self.send_response(301)
        self.send_header('Content-type','text/html')
        if redirectTo:
            self.send_header('Location',redirectTo)

        self.end_headers()


#### Main

def main():
    """initates the server and specifies the port to listen on"""

    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered. stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
