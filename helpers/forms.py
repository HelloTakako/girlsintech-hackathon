from wtforms import Form,  StringField,  PasswordField, validators

class Registerform(Form):
    username = StringField('Username', [
        validators.Length(max=25),
        validators.DataRequired()])
    email = StringField('Email', [
        validators.Email(),
        validators.DataRequired()])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')])
    confirm = PasswordField('Confirm Password', [
        validators.DataRequired()
    ])
