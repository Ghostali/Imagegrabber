# [START app]
import logging
import imagegrabber
from flask import Flask, render_template, redirect, url_for, request, Response, flash, session
import pymysql

app = Flask(__name__)

app.secret_key = 'randomized'

conn = pymysql.connect(host='35.187.42.64', user='root', passwd='Killer123', db='websites')
c = conn.cursor()


# Loads the index page and looks at inputs once submitted
@app.route('/', methods=['GET', 'POST'])
def index():
    urls = []
    s = c.execute("SELECT * from websites")
    for i in c.fetchall():
        urls.append(i[0])
    print(urls)
    if request.method == 'POST':
        url = request.form['link']
        if len(url) > 1:
            option = request.form['options']
            c.execute("""INSERT INTO websites (link) VALUES (%s)""", (url))
            conn.commit()
            print("this is the URL", url)
            session['url'] = url
            session['option'] = option
            return redirect(url_for('images'))
        else:
            return redirect(url_for('index'))
    return render_template('home.html', s=s, urls=urls)


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
    app.run(host='0.0.0.0', debug=True)
# [END app]
