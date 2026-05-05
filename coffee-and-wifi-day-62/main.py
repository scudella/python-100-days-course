from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField('Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL(message="Please enter a valid website address.")])
    opening_time = StringField('Opening Time e.g. 8AM', validators=[DataRequired()])
    closing_time = StringField('Closing Time e.g. 5:30PM', validators=[DataRequired()])
    coffe_rating = SelectField('Coffe Rating', choices=["", "☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕" ], validators=[DataRequired()])
    wifi_strength = SelectField('WiFi Strength Rating', choices=["", "✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪" ], validators=[DataRequired()])
    power_supply = SelectField('Power Socket Availability', choices=["","🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"] , validators=[DataRequired()])
    submit = SubmitField('Submit')

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        # Find index of 'submit'
        keys = list(form.data.keys())
        idx = keys.index('submit')

        # Slice dictionary to get only items before 'submit'
        filtered_data = {k: form.data[k] for k in keys[:idx]}
        values_to_write = list(filtered_data.values())
        with open('cafe-data.csv', 'a', encoding='utf-8')  as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(values_to_write)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows, length=len(list_of_rows))

if __name__ == '__main__':
    app.run(debug=True)
