from flask.ext.wtf import Form
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, NoneOf, Email
from wtforms.widgets import TextArea


class SignupForm(Form):
    phone_providers = [('default', '-Please Choose Your Provider-'),
                       ('alltell', 'Alltell Wireless'),
                       ('att', 'AT&T'),
                       ('boost', 'Boost Mobile'),
                       ('cricket', 'Cricket'),
                       ('metropcs', 'Metro PCS'),
                       ('projectfi', 'Project Fi'),
                       ('sprint','Sprint'),
                       ('straighttalk', 'Straight Talk'),
                       ('tmobile', 'T-Mobile'),
                       ('uscellular', 'U.S. Cellular'),
                       ('verizon', 'Verizon Wireless'),
                       ('virgin', 'Virgin Mobile'),
                       ('other', 'Other Provider')]

    #phone = StringField('phone', validators=[Regexp('9 digits or 10 if the first is 1')])
    lname = StringField('lname', validators=[DataRequired(message='Please enter your last name.')])
    fname = StringField('fname', validators=[DataRequired(message='Please enter your first name.')])
    phone = StringField('phone', validators=[DataRequired(message='A valid phone number is required.')])
    provider = SelectField('provider', validators=[NoneOf(('default',), message='Please select a wireless provider.') ],
                           choices=phone_providers)


class UnsubscribeForm(Form):
    # TODO Add validator messages
    #phone = StringField('phone', validators=[Regexp('9 digits or 10 if the first is 1')])
    lname = StringField('lname', validators=[DataRequired()])
    fname = StringField('fname', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])


class BugReportForm(Form):
    categories = [('default', '--'),
                  ('www', 'Website Issues'),
                  ('signup', 'Signup/Unsubscribe Issues'),
                  ('sms', 'Text Message Issues'),
                  ('provider', 'Mobile Service Provider Not Listed'),
                  ('feature', 'Feature Request'),
                  ('other', 'Other Issue')]

    name = StringField('name')
    email = StringField('email')
    subject = SelectField('category',
                          validators=[NoneOf(('default',), message='Please select a category.')],
                          choices=categories)
    message = StringField('message',
                          validators=[DataRequired(message="Please enter a message.")],
                          widget=TextArea())

class ConfCodeForm(Form):
    confcode = StringField('confcode', validators=[DataRequired(message="Please enter your code.")])