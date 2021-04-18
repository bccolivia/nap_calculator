from flask import render_template, flash, redirect
from app import app
from app.forms import NapForm
from app.calculator import NapGenerator
import logging
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')
@app.route('/nap_calculator', methods=['GET', 'POST'])
def nap_parameters():
    form = NapForm()
    if form.validate_on_submit():
        nap_table, message = NapGenerator(
            wake_window_length_value_min = form.wake_window_length_value_min.data,
            wake_window_length_value_max = form.wake_window_length_value_max.data,
            wake_window_length_label = form.wake_window_length_label.data,
            nap_length_value_min = form.nap_length_value_min.data,
            nap_length_value_max = form.nap_length_value_max.data,
            nap_length_label = form.nap_length_label.data,
            earliest_bedtime = form.earliest_bedtime.data,
            latest_bedtime = form.latest_bedtime.data,
            last_nap_start_time = form.last_nap_start_time.data,
            last_nap_still_ongoing = form.last_nap_still_ongoing.data,
            possible_num_naps = form.possible_num_naps.data,
            round_times_by = form.round_times_by.data,
            last_nap_end_time = form.last_nap_end_time.data,
            )
        return render_template('nap_calculator.html', 
                               title='Nap Calculator', 
                               form=form, 
                               message=message, 
                               table=nap_table.to_html(
                                   classes=['data','table table-sm'],
                                   index=False)
                              )
    return render_template('nap_calculator.html', title='Nap Calculator', form=form)