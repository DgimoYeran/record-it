# -*- coding: utf-8 -*-

from flask import (Blueprint, abort, current_app, flash, make_response,
                   redirect, render_template, url_for)
from flask_babel import _
from flask_login import current_user

from recordit.extensions import cache, db
from recordit.models import Course, Report, Role, User
from recordit.utils import redirect_back

front_bp = Blueprint('front', __name__)


@front_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))

    flash(_('Welcome~'), 'info')
    return render_template('front/index.html')


@front_bp.route('/about')
@cache.cached(timeout=60)
def about():
    role_teacher = Role.query.filter_by(name='Teacher').one()
    teacher_count = User.query.filter_by(role_id=role_teacher.id).count()
    role_student = Role.query.filter_by(name='Student').one()
    student_count = User.query.filter_by(role_id=role_student.id).count()

    course_count = Course.query.count()
    report_count = Report.query.count()

    flash(_('This is about page, make you know more about us.'), 'info')
    return render_template(
        'front/about.html', teacher_count=teacher_count, student_count=student_count,
        course_count=course_count, report_count=report_count)


@front_bp.route('/set-locale/<locale>')
def set_locale(locale):
    if locale not in current_app.config['LOCALES']:
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('locale', locale, max_age=60 * 60 * 24 * 7)

    if current_user.is_authenticated:
        current_user.locale = locale
        db.session.commit()

    flash(_('Setting updated.'), 'success')

    return response
