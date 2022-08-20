from flask import Blueprint, render_template

mandelbrot = Blueprint('mandelbrot', __name__,
                       template_folder='templates',
                       static_folder='static')


@mandelbrot.route('/python')
def pythonMandelbrot():
    return render_template('mandelbrotPython.html')


@mandelbrot.route('/js')
def jsMandelbrot():
    return render_template('mandelbrotJs.html')


@mandelbrot.route('/')
def index():
    return render_template('mandelbrot.html')
