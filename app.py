from flask import Flask, render_template, request
from waitress import serve
from flask import Flask, url_for
import random, os

app = Flask(__name__)
app.debug = False


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
def work():
  path = "static/img/projects"
  fname = []
  for root, d_names, f_names in os.walk(path):
    for f in f_names:
      fname.append(os.path.join(root, f))
  return render_template('work.html', work_list = fname)

@app.route('/projects/<project>')
def project(project):
  path = "static/img/projects/" + project
  fname = []
  for root, d_names, f_names in os.walk(path):
    for f in f_names:
      fname.append(os.path.join(root, f))
  return render_template('projects/' + project + '.html', project = project, work_list = fname)

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
    