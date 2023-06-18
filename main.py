import flask
from flask_sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///developer.db'
db = SQLAlchemy(app)


class Developers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET'])
def start():
    return flask.render_template('index.html', projects=Developers.query.all())


@app.route('/add_proj', methods=['POST'])
def add_proj():
    title = flask.request.form['title']
    link = flask.request.form['link']
    db.session.add(Developers(title=title, link=link))
    db.session.commit()

    return flask.redirect(flask.url_for('start'))


@app.route('/delete_all', methods=['POST'])
def delete():
    projects = Developers.query.all()
    for proj in projects:
        db.session.delete(proj)
    db.session.commit()

    return flask.redirect(flask.url_for('start'))


with app.app_context():
    db.create_all()

app.run()
