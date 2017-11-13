from flask import Flask, render_template, request, jsonify
app = Flask("sample autocomplete")

words = ['Agent', 'Android', 'Anniversary', 'But', 'Chrome', 'Creation',
    'Creators', 'Developer', 'Edge', 'Emulation', 'F12', 'Firefox',
    'Fortunately', 'Google', 'Here', 'However', 'ISO', 'If', 'Language',
    'Media', 'Microsoft', 'Mozilla', 'N', 'PC', 'Press', 'Single', 'So',
    'Switcher', 'That', 'Tool', 'Tools', 'Update', 'User', 'Windows', 'With',
    'You', 'a', 'able', 'access', 'accessing', 'actually', 'agent', 'also',
    'an', 'and', 'are', 'around', 'as', 'available', 'avoid', 'be', 'bit',
    'both', 'browser', 'bummer', 'but', 'called', 'can', 'change', 'click',
    'created', 'decided', 'dedicated', 'device', 'different', 'do', 'don',
    'download', 'easily', 'easy', 'enough', 'extension', 'extensions',
    'files', 'fly', 'folks', 'for', 'from', 'get', 'giant', 'hands', 'has',
    'have', 'how', 'identifies', 'if', 'in', 'is', 'it', 'landing', 'latest',
    'lets', 'link', 'messing', 'now', 'of', 'on', 'operating', 'page',
    'provides', 'reads', 'redirect', 'redirected', 'released', 's', 'say',
    'sees', 'shouldn', 'similar', 'so', 'software', 'still', 'straight',
    'strangely', 'system', 't', 'tab', 'that', 'the', 'there', 'therefore',
    'to', 'too', 'use', 'user', 'users', 'version', 'want', 'website',
    'well', 'which', 'who', 'will', 'with', 'without', 'you', 'your']



@app.route('/')
def form():
    return render_template('a.html')

@app.route('/autocomplete')
def query_autocomplete():
    q = request.args['term']
    print(q)
    q = q and q.lower()
    results = [w for w in words if q in w.lower()]
    return jsonify(results)
