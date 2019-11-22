import formshare.plugins as plugins
import formshare.plugins.utilities as u
from sqlalchemy import Table, Column, Unicode
from sqlalchemy.orm import mapper

from .views import MyPublicView, MyPrivateView, PrjStatus, SensiMap
from .processes.evaluateForm import validateForm
from .orm.extTask import ExtTask


class ext_climate(plugins.SingletonPlugin):
    plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ISchema)
    plugins.implements(plugins.IProject)
    plugins.implements(plugins.IDatabase)
    plugins.implements(plugins.IResource)
    plugins.implements(plugins.IForm)

    def before_mapping(self, config):
        # We don't add any routes before the host application
        return []

    def after_mapping(self, config):
        # We add here a new route /json that returns a JSON
        custom_map = []
        custom_map.append(
            u.add_route(
                "plugin_mypublicview", "/mypublicview", MyPublicView, "public.jinja2"
            )
        )

        custom_map.append(
            u.add_route(
                "plugin_myprivateview",
                "/user/{userid}/myprivateview",
                MyPrivateView,
                "private.jinja2",
            )
        )

        custom_map.append(
            u.add_route(
                "status",
                "/user/{userid}/status/{prj}",
                PrjStatus,
                "json",
            )
        )

        custom_map.append(
            u.add_route(
                "sensimap",
                "/user/{userid}/sensimap/{prj}/{div}",
                SensiMap,
                "json",
            )
        )

        return custom_map

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.add_templates_directory(config, "templates")
        u.add_static_view(config, "climate", "static")

    def update_schema(self, config):
        new_fields = [
            u.add_field_to_project_schema("is_climate", "Project is for climate")
        ]
        return new_fields

    def before_create(self, request, user, project_data):

        user_climate = request.registry.settings.get("climate.user", "")

        if user_climate == user:
            project_data["is_climate"] = 1
        else:
            project_data["is_climate"] = 0

        return project_data, True, ""

    def after_create(self, request, user, project_data):
        pass

    # Implements IDatabase
    def update_orm(self, metadata):
        t = Table(
            "extTask",
            metadata,
            Column("id_task", Unicode(120), primary_key=True),
            Column("project", Unicode(120)),
        )
        metadata.create_all()
        mapper(ExtTask, t)

    # Implements IResource
    def add_libraries(self, config):

        # We add here our new library using the resources directory of the plugin
        libraries = []
        libraries.append(u.add_library("myResource", "resources"))
        return libraries

    def add_js_resources(self, config):
        # You can add your JS resources here
        myJS = []
        myJS.append(u.add_js_resource("myResource", "sparkline", "js/sparkline/jquery.sparkline.min.js"))

        myJS.append(u.add_js_resource("myResource", "flot", "js/flot/jquery.flot.js"))
        myJS.append(u.add_js_resource("myResource", "flotTooltip", "js/flot/jquery.flot.tooltip.min.js"))
        myJS.append(u.add_js_resource("myResource", "flotSpline", "js/flot/jquery.flot.spline.js"))
        myJS.append(u.add_js_resource("myResource", "flotResize", "js/flot/jquery.flot.resize.js"))
        myJS.append(u.add_js_resource("myResource", "chosen", "js/chosen/chosen.jquery.js", None))
        myJS.append(u.add_js_resource("myResource", "chartjs", "js/chartJs/Chart.min.js", None))
        myJS.append(u.add_js_resource("myResource", "ligthbox", "js/ligthbox/lightbox.js", None))

        return myJS

    def add_css_resources(self, config):
        # You can add your CSS resources here
        myCSS = []
        # myCSS.append(u.addCSSResource('mylibrary', 'myCSSResource', 'relative/path/to/resources/myresource.css'))
        myCSS.append(u.add_css_resource('myResource', 'animate', 'css/animate.css'))
        myCSS.append(u.add_css_resource('myResource', 'bootstrap', 'css/bootstrap.css'))
        myCSS.append(u.add_css_resource('myResource', 'style', 'css/style.css'))
        myCSS.append(u.add_css_resource('myResource', 'font', 'css/font-awesome.css'))
        myCSS.append(u.add_css_resource('myResource', 'chosen', 'css/chosen/bootstrap-chosen.css', None))
        myCSS.append(u.add_css_resource('myResource', 'ligthbox', 'css/ligthbox/lightbox.css', None))
        return myCSS

    def after_form_checks(self, request, user, project, form, form_data, form_directory, survey_file, create_file,
                          insert_file, itemsets_csv):

        if request.registry.settings.get("climate.user", "") == user:
            return validateForm(create_file)
        else:
            return True, ""
