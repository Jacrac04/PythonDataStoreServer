from flask import Blueprint, render_template
from flask_login import login_required, current_user

mandelbrot = Blueprint('mandelbrot', __name__, 
                            template_folder='templates',
                            static_folder='static')


@mandelbrot.route('/')
def index():
    return render_template('mandelbrot.html')


