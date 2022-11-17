from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Used to create form / form fields for add.html


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(
        'Cafe Location on Google Maps (URL)', validators=[URL()])
    opening = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing Time e.g. 5:30PM',
                          validators=[DataRequired()])
    rating = SelectField('Coffee Rating', choices=[(
        '1', '☕️'), ('2', '☕️☕️'), ('3', '☕️☕️☕️'), ('4', '☕️☕️☕️☕️'), ('5', '☕️☕️☕️☕️☕️')])
    wifi = SelectField('Coffee Rating', choices=[(
        '0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')])
    socket = SelectField('Coffee Rating', choices=[(
        '0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    return render_template("index.html")

# Adds data from form to csv file


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', 'a', newline='') as cafe_csv:
            cafe_csv.write(
                f'\n {form.cafe.data}, {form.location.data}, {form.opening.data}, {form.closing.data}, {form.rating.data}, {form.wifi.data}, {form.socket.data},')
        return render_template('index.html')
    return render_template('add.html', form=form)

# Populates cafe.html with data from csv file


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
