from flask import Flask, request, render_template, redirect, send_file
import requests
from RouteAdder import RouteAdder
from io import BytesIO

app = Flask(__name__)

def make_routes(html_string, site_root):
    route_adder = RouteAdder(site_root)
    route_adder.feed(html_string)
    return(route_adder.get_data())

@app.route("/")
@app.route("/<path:subpath>")
def root(subpath=None):
    if subpath != None:
        url = subpath

        if 'https://' not in url[0:9]:
            return redirect(f'/https://{url}')
        
        if 'https://www.google.com/url' in url: # exception for google redirects
            return redirect(f'/{request.args.get("q")}')

        req = requests.get(f"{url}?{request.query_string.decode()}")

        if req.headers.get('content-type').split('/')[0] == 'text': # for html / css / js
            text = make_routes(req.text, url.split('/')[2])
            return text
        else:
            file_data = BytesIO(req.content)
            file_data.seek(0)
            return send_file(file_data)
            
    
    else:
        return redirect(f'/https://www.google.com/search?&q=google&oq=google&')