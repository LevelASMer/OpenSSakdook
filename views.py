# Views
import sqlite3
import colander
import deform
import time
from deform.widget import TextAreaWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

DATABASE = './ssakdook.db'

# Form Class
class SettingSchema(colander.MappingSchema):
    filter_word_enable = colander.SchemaNode(colander.Integer(), name="filter_word_enable")
    filter_url_enable = colander.SchemaNode(colander.Integer(), name="filter_url_enable")
    filter_emoticon_enable = colander.SchemaNode(colander.Integer(), name="filter_emoticon_enable")
    filter_symbol_enable = colander.SchemaNode(colander.Integer(), name="filter_symbol_enable")
    filter_repeat_enable = colander.SchemaNode(colander.Integer(), name="filter_repeat_enable")
    filter_color_enable = colander.SchemaNode(colander.Integer(), name="filter_color_enable")

class CommandSchema(colander.MappingSchema):
    command = colander.SchemaNode(colander.String(), widget=TextAreaWidget())
    description = colander.SchemaNode(colander.String(),  widget=TextAreaWidget())
    cooltime = colander.SchemaNode(colander.String(), widget=TextAreaWidget())

class DeleteSchema(colander.MappingSchema):
    pass

# Global Layout
def site_layout():
    renderer = get_renderer("template/global_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

# First view, available at http://localhost:6543/
@view_config(route_name='home', renderer='template/home.pt')
def home(request):
    schema = SettingSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())

                # Save form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], time.time(), )
                c.execute('INSERT OR IGNORE INTO commands (command, description, cooltime, latest_use) VALUES(?, ?, ?, ?)', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/command/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, }
    return {"layout": site_layout(), }

@view_config(route_name='command', renderer='template/commands.pt')
def command(request):
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT id, command, cooltime FROM commands ORDER BY command DESC')
    fetch = c.fetchall()
    con.close()
    return {"layout": site_layout(), 'command': fetch}

@view_config(route_name='command_add', renderer='template/add_command.pt')
def command_add(request):
    schema = CommandSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())

                # Save form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], time.time(), )
                c.execute('INSERT OR IGNORE INTO commands (command, description, cooltime, latest_use) VALUES(?, ?, ?, ?)', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/command/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, }

@view_config(route_name='command_edit', renderer='template/edit_command.pt')
def command_edit(request):
    id = request.matchdict['id']
    schema = CommandSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())

                # Save form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], id, )
                c.execute('UPDATE commands SET command=?, description=?, cooltime=? WHERE id=?', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/command/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    # Get data from database
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    values = (id, )
    c.execute('SELECT command, description, cooltime FROM commands WHERE id=?', values)
    fetch = c.fetchall()
    con.close()

    return {"layout": site_layout(), "rendered_form": rendered_form, "id": id, "command": fetch[0], }

@view_config(route_name='command_delete', renderer='template/delete_command.pt')
def command_delete(request):
    id = request.matchdict['id']
    schema = DeleteSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
                # Delete form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (id, )
                c.execute('DELETE FROM commands WHERE id=?', values)
                con.commit()
                con.close()

                request.session.flash('Goodbye.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/command/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, "id": id, }

@view_config(route_name='timer', renderer='template/timers.pt')
def timer(request):
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT id, name, cooltime FROM timers ORDER BY name DESC')
    fetch = c.fetchall()
    con.close()
    return {"layout": site_layout(), 'timer': fetch}

@view_config(route_name='timer_add', renderer='template/add_timer.pt')
def timer_add(request):
    schema = CommandSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())

                # Save form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], time.time(), )
                c.execute('INSERT OR IGNORE INTO timers (name, description, cooltime, latest_use) VALUES(?, ?, ?, ?)', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/timer/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, }

@view_config(route_name='timer_edit', renderer='template/edit_timer.pt')
def timer_edit(request):
    id = request.matchdict['id']
    schema = CommandSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())

                # Save form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], id, )
                c.execute('UPDATE timers SET name=?, description=?, cooltime=? WHERE id=?', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/timer/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    # Get data from database
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    values = (id, )
    c.execute('SELECT name, description, cooltime FROM timers WHERE id=?', values)
    fetch = c.fetchall()
    con.close()

    return {"layout": site_layout(), "rendered_form": rendered_form, "id": id, "timer": fetch[0], }

@view_config(route_name='timer_delete', renderer='template/delete_timer.pt')
def timer_delete(request):
    id = request.matchdict['id']
    schema = DeleteSchema().bind(request=request)

    # Create a styled button with some extra Bootstrap 3 CSS classes
    process_btn = deform.form.Button(name='process')
    form = deform.form.Form(schema, buttons=(process_btn,))

    # User submitted this form
    if request.method == "POST":
        if 'process' in request.POST:
            try:
                appstruct = form.validate(request.POST.items())
                # Delete form data from appstruct
                con = sqlite3.connect(DATABASE)
                c = con.cursor()

                values = (id, )
                c.execute('DELETE FROM timers WHERE id=?', values)
                con.commit()
                con.close()

                request.session.flash('Goodbye.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/timer/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, "id": id, }

@view_config(route_name='filter', renderer='template/filters.pt')
def filter(request):
    return {"layout": site_layout()}