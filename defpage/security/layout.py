from pyramid.renderers import get_renderer
from defpage.security.config import system_params

def renderer_add_globals(e):
    e["layout"] = get_renderer("defpage.security:templates/layout.pt").implementation()
    e["base_url"] = system_params.base_url
    e["static_url"] = system_params.static_url
