from flask import Flask, render_template, request
from waitress import serve
from flask import Flask, url_for
import random, os
import json


app = Flask(__name__)
app.debug = False

def load_project_data():
    with open("projects.json") as f:
        return json.load(f)


@app.template_filter('shuffle')
def filter_shuffle(seq):
  try:
    result = list(seq)
    random.shuffle(result)
    return result
  except:
    return seq


  
@app.template_filter('capfirst')
def filter_capfirst(s):
  return s[:1].upper() + s[1:]


@app.route('/')
def face():
    project_list = load_project_data()

    # attach full image paths
    for project in project_list:
        project["image"] = url_for('static', filename=f'img/projects/{project["slug"]}/{project["image"]}')

    return render_template('face.html', projects=project_list)

@app.route('/carousel')
def carousel():
   return render_template('carousel.html')


@app.route('/work')
def work():
  path = "static/img/projects"
  fname = []
  for root, d_names, f_names in os.walk(path):
    for f in f_names:
      fname.append(os.path.join(root, f))
  return render_template('work.html', work_list = fname)

import json

@app.route('/projects/<project>')
def project(project):

    # 1. Build image list
    path = "static/img/projects/" + project
    fname = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            if not f.startswith('.'):
                fname.append(os.path.join(root, f))

    # 2. Load metadata (active + backup)
    all_projects = []

    try:
        with open('projects.json') as f:
            all_projects.extend(json.load(f))
    except FileNotFoundError:
        print("projects.json not found.")

    try:
        with open('backup.json') as f:
            all_projects.extend(json.load(f))
    except FileNotFoundError:
        print("backup.json not found.")

    project_data = next(
        (p for p in all_projects if p.get("slug") == project),
        {}
    )

    # 3. SINGLE return (only once!)
    return render_template(
        f'projects/{project}.html',
        project=project,
        work_list=fname,
        **project_data
    )


@app.context_processor
def inject_projects():
    path = "templates/projects"
    projects = []
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            # Filter for HTML files only
            if f.endswith('.html'):
                project_name = f.split('.')[0]  # Remove the file extension
                projects.append(project_name)
    return dict(projects=projects)


#@app.route('/')
#@app.route('/index')
#def index():
#   return render_template('index.html')


@app.context_processor
def override_url_for():
  return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
  if endpoint == 'static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path, endpoint, filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **values)
  
#if __name__ == '__main__':
 #app.run(host='0.0.0.0') 

if __name__ == '__main__':
  app. run(host='0.0.0.0', port=3000)
    


@app.context_processor
def override_url_for():
  return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
  if endpoint == 'static':
    filename = values.get('filename', None)
    if filename:
      file_path = os.path.join(app.root_path, endpoint, filename)
      values['q'] = int(os.stat(file_path).st_mtime)
  return url_for(endpoint, **values)