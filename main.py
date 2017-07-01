from flask import Flask, request, redirect, url_for, render_template
import requests
import logic


app = Flask(__name__)


@app.route('/<account>', methods=['GET', 'POST'])
def index(account=None):
    page = request.form['page']
    url = request.form['url']
    return render_template('index.html', option=account, page=page, url=url)

@app.route('/', methods=['GET', 'POST'])
def reditect():
    return redirect('/planets/1')


@app.route('/logger', methods=['GET', 'POST'])
def logger():
    page = request.form['page']
    url = request.form['url']
    if_failed = request.form['type']
    user_info = logic.logger()
    if (user_info is None) or (user_info is False):
        return render_template('index.html', option=if_failed, page=page, url=url)
    global username
    username = user_info['username']
    global user_id
    user_id = user_info['user_id']
    if page == 1:
        planets = logic.get_planets()
    else:
        planets = logic.get_planets(url)
    all_votes = logic.vote_upVader()
    user_votes = logic.vote_statistics(user_id)
    return render_template('planets.html', planets=planets, username=username, user_id=user_id, page=page, url=url, all_votes=all_votes, user_votes=user_votes)


@app.route('/planets/<page>', methods=['GET', 'POST'])
def loggedin(page=None):
    all_votes = logic.vote_upVader()
    if page is None:
        page = 1
    if username:
        user_votes = logic.vote_statistics(user_id)
    else:
        user_votes = None
    if request.method == 'GET':
        planets = logic.get_planets()
        url = planets[1]
    else:
        if 'option' in request.form:
            user_info = logic.logger()
            global username
            username = user_info['username']
        if 'url' in request.form:
            url = request.form['url']
            planets = logic.get_planets(url)
        if 'page' in request.form:
            page = request.form['page']
        if page == 1 or page == '1':
            planets = logic.get_planets()
        if user_id:
            logic.cookiemaker(user_id)
    return render_template('planets.html', planets=planets, page=page, username=username, user_id=user_id, url=url, all_votes=all_votes, user_votes=user_votes)


if __name__ == '__main__':
    username = None
    user_id = None
