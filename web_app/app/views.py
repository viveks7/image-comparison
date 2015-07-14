from flask import render_template, flash, redirect
from app import app
from .forms import LinkForm
import img


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LinkForm()
    if form.validate_on_submit():
        simi_percent=img.main(form.link_one.data, form.link_two.data)
        if simi_percent==101 or simi_percent ==102 or simi_percent == 103 or simi_percent==104 or simi_percent==105:
            flash("error %s" % simi_percent)
            return redirect('/Result')
        flash('%s percent' % (simi_percent))
        return redirect('/result')
    return render_template('form.html',
                           title='Home', form=form)


@app.route('/result')
def hello():
    return render_template('result.html', title='Result')
