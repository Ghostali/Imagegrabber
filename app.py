# [START app]
import logging
import imagegrabber
from flask import Flask, render_template, redirect, url_for, request, flash, session
import os
app = Flask(__name__)

app.secret_key = 'randomized'


# Loads the index page and looks at inputs once submitted
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['link']
        if len(url) > 1:
            option = request.form['options']
            print("this is the URL", url)
            session['url'] = url
            session['option'] = option
            return redirect(url_for('images'))
        else:
            return redirect(url_for('index'))
    return render_template('index.html')


# returns the images scrawled on given website
@app.route('/images', methods=['GET', 'POST'])
def images():
    if request.method == 'POST':
        url = request.form['link']
        if len(url) > 1:
            option = request.form['options']
            print("this is the URL", url)
            session['url'] = url
            session['option'] = option
            return redirect(url_for('images'))
        else:
            return redirect(url_for('index'))

    url = session.get('url')
    option = session.get('option')
    links = imagegrabber.website(url, option)
    if len(links) == 0:
        flash('No image was found')
        return redirect(url_for('index'))
    print("this is the links", links)
    return render_template('images.html', links=links)


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
# [END app]
