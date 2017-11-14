# coding: utf-8

from google.appengine.api import search
from flask import Flask, render_template, request, jsonify

idx = search.Index(name='products_idx')
app = Flask("sample autocomplete")

@app.route('/')
def form():
    return render_template('a.html')

@app.route('/autocomplete')
def query_autocomplete():
    q = request.args['term']
    if not q:
        return jsonify([])
    q = q.lower()
    results = idx.search('product_name: \"{}\"'.format(q))
    resuls_dict = [{f.name: f.value for f in r.fields} for r in results]
    return jsonify([r['product_name'] for r in resuls_dict])


