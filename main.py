from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
import pandas as pd
import re
import os

#from werkzeug.datastructures import ImmutableMultiDict, FileStorage


app = Flask(__name__, template_folder="")

sorting = {}

@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
        f = request.files['file']
        if not f.filename == '':
            filename = f.filename
            return redirect(f'/file/{filename}')
        return redirect('/')
    elif request.method == 'GET':
        files = os.listdir('files/')
        return render_template('index.html', filenames = files)

@app.route("/file/<filename>")
def display_file(filename):
    if not filename in os.listdir('files/'):
        flash("file not found")
        return redirect('/')
    elif re.match(r'.*\.csv',filename):
        df = pd.read_csv(f'files/{filename}')
    else:
        flash("incorrect file format")
        return redirect('/')
    column = request.args.get('column', None)
    print(column)
    if not column == None:
        if filename not in sorting:
            sorting.update({filename: {}})
        if column not in sorting[filename]:
            sorting[filename].update({column: True})
        else:
            sorting[filename].update({column: not sorting[filename][column]})
        asc = sorting[filename][column]

        if column == 'index':
            df = df.sort_index(ascending = asc)
        else:
            df = df.sort_values(by=column, ascending = asc)
    return render_template('files.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route("/delete/<path:filename>")
def delete_file(filename):
    os.remove(f'files/{filename}')
    return redirect(f'/')

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='127.0.0.1', port=5000)    