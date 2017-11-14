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


##### doesn't work. app engine doesnot allow background thread after request is processed.
# google appengine backend or task queue needs to be implements
from google.cloud import datastore
datastore_client = datastore.Client()

def datastore_to_search(dr):
    fields = []
    if dr['product_name']:
        fields.append(search.TextField(name='product_name', value=dr['product_name']))
    if dr['product_link']:
        fields.append(search.TextField(name='product_link', value=dr['product_link']))
    if dr['product_price']:
        fields.append(search.NumberField(name='product_price', value=dr['product_price']))
    if dr['price_symbol']:
        fields.append(search.AtomField(name='price_symbol', value=dr['price_symbol']))
    return search.Document(doc_id=str(dr.key.id), fields=fields)

def insert(dr):
    idx.put(datastore_to_search(dr))

from threading import Thread, current_thread
from time import sleep


job_generator = iter(datastore_client.query(kind='products').fetch())

counter = 0
def worke_func():
    global counter
    global job_generator
    try:
        while True:
            dr = job_generator.next()
            print(current_thread().name, dr)
            counter += 1
            sleep(3)
    except StopIteration as e:
        pass
    except Exception as e:
        raise e


workers = [Thread(name='worker_'+str(i), target=worke_func) for i in range(5)]
[w.start() for w in workers]

# in case of ChunkedEncodingError apply patch https://stackoverflow.com/a/37181539

@app.route('/counter')
def get_counter():
    global counter
    return "total records inserted: {}".format(counter)

@app.route('/workers')
def worers_status():
    global workers
    return jsonify([w.is_alive() for w in workers])

@app.route('/start_workers')
def start_workers():
    global workers
    return jsonify([w.start() for w in workers])
