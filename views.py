# Views
import sqlite3
import colander
import deform
from deform.widget import TextAreaWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import get_renderer
from pyramid.view import view_config

DATABASE = './ssakdook.db'

# Form Class
class CommandSchema(colander.MappingSchema):
    command = colander.SchemaNode(colander.String(), widget=TextAreaWidget())
    description = colander.SchemaNode(colander.String(),  widget=TextAreaWidget())
    cooltime = colander.SchemaNode(colander.String(), widget=TextAreaWidget())

# Global Layout
def site_layout():
    renderer = get_renderer("template/global_layout.pt")
    layout = renderer.implementation().macros['layout']
    return layout

# First view, available at http://localhost:6543/
@view_config(route_name='home', renderer='template/home.pt')
def home(request):
    return {"layout": site_layout(), }

@view_config(route_name='command', renderer='template/commands.pt')
def command(request):
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT * FROM commands')
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

                values = (appstruct["command"], appstruct["description"], appstruct["cooltime"], )
                c.execute('INSERT OR IGNORE INTO commands (command, description, cooltime) VALUES(?, ?, ?)', values)
                con.commit()
                con.close()

                # Thank user and take him/her to the next page
                request.session.flash('Thank you for the submission.')

                # Redirect to the page shows after succesful form submission
                return HTTPFound("/command/list/1")
            except deform.exception.ValidationFailure as e:
                # Render a form version where errors are visible next to the fields,
                # and the submitted values are posted back
                con.close()
                rendered_form = e.render()
    else:
        # Render a form with initial default values
        rendered_form = form.render()

    return {"layout": site_layout(), "rendered_form": rendered_form, }

@view_config(route_name='command_edit', renderer='template/edit_command.pt')
def command_edit(request):
    return {"layout": site_layout(), }

@view_config(route_name='timer', renderer='template/timers.pt')
def timer(request):
    return {"layout": site_layout(), }

@view_config(route_name='log', renderer='template/logs.pt')
def log(request):
    con = sqlite3.connect(DATABASE)
    c = con.cursor()

    c.execute('SELECT * FROM logs ORDER BY date DESC')
    fetch = c.fetchall()
    con.close()
    return {"layout": site_layout(), 'log': fetch}