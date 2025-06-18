import json
import os
from flask import Flask, render_template
#from flask_navigation import Navigation
from cfg import cfg as config
from pathlib import Path

app = Flask("Pirate Flow")
#nav = Navigation(app)

#def menu():
#    <a href="{{ url_for('home') }}">Home</a>

@app.route("/")
def index():
    return render_template('index.html') 

@app.route("/browse/")
def browse_downloads():
    path = os.path.abspath(config.DOWNLOADS)
    files = os.listdir(path)
    id = 0
    file_stats = list()
    for f in files:
        print("BRET", f, type(f))
        full_path = os.path.join(path, f)
        print("BRET", f, full_path)
        f_stats = os.stat(full_path)
        print("BRET", full_path, f_stats)
        file_stat = dict()
        file_stat['id'] = id
        file_stat['name'] = f
        file_stat['size'] = f_stats.st_size /(1024 * 1024)
        file_stat['date'] = f_stats.st_ctime
        id = id + 1
        file_stats.append(file_stat)
    return render_template('browse.html', files = file_stats)

@app.route('/about/')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    config.load()
    app.run(host=config.LISTEN_ADDR, port=config.PORT, threaded=config.DEV_THREADED, debug=config.DEBUG)
    # initializing Navigations 
    #nav.Bar('top', [ 
    #    nav.Item('Home', 'index'),
    #    nav.Item('Downloads', 'browse', {'page': 1}),
    #]) 

