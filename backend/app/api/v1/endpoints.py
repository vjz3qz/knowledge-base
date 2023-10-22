from . import v1

@v1.route('/users')
def get_users():
    return {"users": ["Alice", "Bob"]}



# place holder

@v1.route("/")
def hello():
  return "Hello World!"