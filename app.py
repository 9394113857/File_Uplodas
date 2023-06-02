from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

class ContactForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Process the form data
        username = form.username.data
        email = form.email.data
        phone = form.phone.data
        address = form.address.data
        message = form.message.data

        # Perform any necessary processing or validations

        return redirect(url_for('thankyou', name=username))

    return render_template('contact.html', form=form)

@app.route('/thankyou/<name>')
def thankyou(name):
    return render_template('thankyou.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)
