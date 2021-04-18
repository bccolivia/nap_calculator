from flask_wtf import FlaskForm
from wtforms.fields.html5 import TimeField, IntegerRangeField
from wtforms.fields import SelectField, SubmitField, IntegerField, RadioField
from wtforms.validators import DataRequired
from datetime import datetime
from pytz import timezone    

class NapForm(FlaskForm):
    wake_window_length_value_min = IntegerField('Typical Wake Window (Min)', 
                                                validators=[DataRequired()],
                                                default=150,
                                               )
    wake_window_length_value_max = IntegerField('Typical Wake Window (Max)', 
                                                validators=[DataRequired()],
                                                default=180,
                                               )
    wake_window_length_label = RadioField('Wake Window Value',
                                           validators=[DataRequired()],
                                           default='minutes',
                                           choices=[('minutes', ' minutes'),
                                                    ('hours', ' hours')]
                                          )
    
    nap_length_value_min = IntegerField('Typical Nap Lengths (Min)', 
                                        validators=[DataRequired()],
                                        default=30,
                                       )
    nap_length_value_max = IntegerField('Typical Nap Lengths (Max)', 
                                        validators=[DataRequired()],
                                        default=90,
                                       )
    nap_length_label = RadioField('Nap Length Value',
                                           validators=[DataRequired()],
                                           default='minutes',
                                           choices=[('minutes', ' minutes'),
                                                    ('hours', ' hours')]
                                          )
    
    earliest_bedtime = TimeField('Earliest Bedtime (required)',
                                        validators=[DataRequired()],
                                        default=datetime.strptime('7:00PM', '%I:%M%p'),
                                       )
    latest_bedtime = TimeField('Latest Bedtime (required)',
                                        validators=[DataRequired()],
                                        default=datetime.strptime('8:30PM', '%I:%M%p'),
                                       )
    
    possible_num_naps = IntegerField('Max number of remaining naps, not including any ongoing naps (default = 2). The higher this number, the longer this script will take to run. : ', default=2)
    round_times_by = RadioField('Generate possibilities in increments of X minutes (default = 30). Generating in increments of 15 minutes will take longer than generating in increments of 30 minutes.',
                                           validators=[DataRequired()],
                                           choices=[('15 minutes', '15 minutes'),
                                                    ('30 minutes', '30 minutes')],
                                           default = '30 minutes',
                                          )
    
    last_nap_start_time = TimeField('When did the last nap start? (required)', validators=[DataRequired()])
    last_nap_still_ongoing = RadioField('Last nap still ongoing? (required)',
                                           validators=[DataRequired()],
                                           choices=[(True, 'Yes'),
                                                    (False, 'No')],
                                           )
    last_nap_end_time = TimeField('When did the last nap end? Skip this question if last nap is still ongoing',
                                  default = datetime.strptime('12:00AM', '%I:%M%p'),
                                 )
    
    submit = SubmitField('Calculate the naps!')