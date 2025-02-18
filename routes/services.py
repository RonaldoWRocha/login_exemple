from flask import Blueprint, render_template

services = Blueprint('services', __name__)

@services.route('/services')
def services_page():
    return render_template('services/services.html')