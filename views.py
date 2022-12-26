import flask

views = flask.Blueprint('views', __name__, template_folder = 'templates')

@views.route('/')
def index():
  return flask.render_template('index.html')

@views.route('/chats/<server>/<channel>')
def chat(server, channel):
  return flask.render_template('chat.html')

@views.route('/login')
def login():
  return flask.render_template('login.html')

@views.route('/signup')
def signup():
  return flask.render_template('signup.html')