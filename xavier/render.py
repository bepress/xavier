from jinja2 import Environment, select_autoescape

jinja_env = Environment(
    autoescape=select_autoescape(['html', 'xml'])
)
