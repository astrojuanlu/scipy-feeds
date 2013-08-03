import urllib.request
import json

from flask import request, render_template

from spfeeds import app

ORG = "scipy"
REPO = "scipy"
BASE_URL = "https://api.github.com/repos/{}/{}/".format(ORG, REPO)


@app.route('/issues.xml')
def issues():
    """Feed of issues, optionally filtered by labels.

    """
    label = request.args.get('label', None)
    if not label:
        url = BASE_URL + "issues"
    else:
        if label not in get_labels():
            return "Error: label does not exist", 400
        url = BASE_URL + "issues?labels={}".format(label)
    headers = {"Accept": "application/vnd.github.VERSION.html+json"}
    req = urllib.request.Request(url, headers=headers)
    rsp = urllib.request.urlopen(req)
    data = json.loads(rsp.read().decode('utf-8'))
    return render_template('atom.xml', label=label, issues=data)


def get_labels():
    """Gets label of repository.

    """
    url = "https://api.github.com/repos/scipy/scipy/labels"
    rsp = urllib.request.urlopen(url)
    data = json.loads(rsp.read().decode('utf-8'))
    for elem in data:
        yield elem['name']
