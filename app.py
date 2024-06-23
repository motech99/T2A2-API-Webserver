
from init import app



@app.route('/')
def index():
    return "Pokemon!"