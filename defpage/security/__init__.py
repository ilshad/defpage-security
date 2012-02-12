from pyramid.config import Configurator
from pyramid.exceptions import NotFound
from pyramid.exceptions import Forbidden
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config
from defpage.lib.util import is_int
from defpage.security.sql import initialize_sql
from defpage.security.config import system_params
from defpage.security.policy import AuthenticationPolicy

def main(global_config, **settings):
    system_params.update(settings)
    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)
    session_factory = UnencryptedCookieSessionFactoryConfig("7oDVDSuJ")
    authentication_policy = AuthenticationPolicy()
    config = Configurator()

    config.setup_registry(settings=settings,
                          session_factory=session_factory,
                          authentication_policy=authentication_policy)

    config.add_subscriber("defpage.security.layout.renderer_add_globals",
                          "pyramid.events.BeforeRender")

    config.add_static_view("static", "defpage.security:static")

    config.add_view("defpage.security.views.signup", "signup",
                    renderer="defpage.security:templates/signup.pt")

    config.add_view("defpage.security.views.anonym_only_empty_view", "signup_code",
                    renderer="defpage.security:templates/signup_code.pt")

    config.add_view("defpage.security.views.signup_confirm", "signup_confirm",
                    renderer="defpage.security:templates/signup_confirm.pt")

    config.add_view("defpage.security.views.login", "login",
                    renderer="defpage.security:templates/login.pt")

    config.add_view("defpage.security.views.logout", "logout")


    config.add_view("defpage.security.views.default", "",
                    renderer="defpage.security:templates/default.pt")

    config.add_view("defpage.security.views.forbidden",
                    "", context=Forbidden,
                    renderer="defpage.security:templates/unauthorized.pt")

    config.add_view("defpage.security.views.unauthorized",
                    "", context=HTTPUnauthorized,
                    renderer="defpage.security:templates/unauthorized.pt")

    config.add_view("defpage.security.views.empty", "",
                    renderer="defpage.security:templates/notfound.pt",
                    context=NotFound)

    config.add_view("defpage.security.views.empty", "error",
                    renderer="defpage.security:templates/error.pt")

    config.add_route("sessions", "/sessions/{session_id}")
    config.add_view("defpage.security.views.sessions",
                    route_name="sessions",
                    renderer="json",
                    request_method="GET")

    config.add_route("account_overview", "/users/{name}",
                     custom_predicates=(is_int,))
    config.add_view("defpage.security.views.account_overview",
                    route_name="account_overview",
                    renderer="defpage.security:templates/account_overview.pt")

    config.add_route("account_delete", "/users/{name}/delete",
                     custom_predicates=(is_int,))
    config.add_view("defpage.security.views.account_delete",
                    route_name="account_delete")

    return config.make_wsgi_app()
