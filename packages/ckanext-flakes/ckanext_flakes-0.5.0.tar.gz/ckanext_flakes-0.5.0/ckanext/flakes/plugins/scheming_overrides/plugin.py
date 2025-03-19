from __future__ import annotations
from typing import Any
from ckan.logic import parse_params
from ckanext.scheming.plugins import _expand_schemas
from flask import Blueprint
from flask.views import MethodView
from ckan.common import CKANConfig
import sqlalchemy as sa
import ckan.plugins as p
from ckan import model
import ckan.plugins.toolkit as tk

from ckanext.flakes.model.flake import Flake
from ckanext.ap_main.interfaces import IAdminPanel
from ckanext.ap_main.types import SectionConfig, ConfigurationItem


class FlakesSchemingOverridesPlugin(p.SingletonPlugin):
    last_modification = None

    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(IAdminPanel, inherit=True)
    p.implements(p.IBlueprint)
    p.implements(p.IMiddleware, inherit=True)

    def update_config(self, config):
        tk.add_template_directory(config, "templates")

    def get_blueprint(self):
        return bp

    # IMiddleware
    def make_middleware(self, app: Any, config: CKANConfig):
        app.before_request(self._check_overrides)
        return app

    def register_config_sections(
        self, config_list: list[SectionConfig]
    ) -> list[SectionConfig]:
        """Extension will receive the list of section config objects."""
        return config_list + [
            SectionConfig(
                name=tk._("Scheming"),
                configs=[
                    ConfigurationItem(
                        name=tk._("Scheming overrides"),
                        info=tk._("Change dataset schemas"),
                        blueprint=(
                            "flakes_scheming_overrides.edit"
                            if p.plugin_loaded("editable_config")
                            else "ap_basic.config"
                        ),
                    )
                ],
            )
        ]

    def configure(self, config: CKANConfig) -> None:
        inspector = sa.inspect(model.Session.bind)
        if not inspector.has_table(Flake.__tablename__):
            return

        plugin = p.get_plugin("scheming_datasets")
        plugin._expanded_schemas = _expand_schemas(plugin._schemas)

        for name, schema in plugin._expanded_schemas.items():
            flakes = Flake.by_extra(
                {"flakes_scheming_overrides": {"schema": name}}, None
            ).order_by(Flake.modified_at.asc())

            removals = set()
            patches = {}
            additions = []

            for flake in flakes:
                fn = flake.data["field"]
                if flake.data["type"] == "remove":
                    removals.add(fn)

                elif flake.data["type"] == "patch":
                    patches[fn] = flake.data["patch"]

                elif flake.data["type"] == "add":
                    additions.append(dict(flake.data["definition"], field_name=fn))

                if not self.last_modification:
                    self.last_modification = flake.modified_at
                else:
                    self.last_modification = max(
                        flake.modified_at, self.last_modification
                    )

            schema["dataset_fields"] = [
                dict(f, **patches.get(f["field_name"], {}))
                for f in schema["dataset_fields"] + additions
                if f["field_name"] not in removals
            ]

    def _check_overrides(self):
        plugin = p.get_plugin("scheming_datasets")
        for name in plugin._expanded_schemas:
            flakes = Flake.by_extra(
                {"flakes_scheming_overrides": {"schema": name}}, None
            )
            if self.last_modification:
                flakes = flakes.filter(Flake.modified_at > self.last_modification)
            if flakes.count():
                break
        else:
            return
        p.plugins_update()


bp = Blueprint("flakes_scheming_overrides", "name")


class EditView(MethodView):
    def get(self):
        plugin = p.get_plugin("scheming_datasets")
        overrides = {}
        for name in plugin._expanded_schemas:
            flakes = Flake.by_extra(
                {"flakes_scheming_overrides": {"schema": name}}, None
            )
            for flake in flakes:
                overrides.setdefault(name, []).append(flake)

        return tk.render(
            "scheming_overrides/config.html",
            {
                "overrides": overrides,
                "schema_options": [
                    {"value": n, "text": n} for n in plugin._expanded_schemas
                ],
            },
        )

    def post(self):
        if "remove" in tk.request.form:
            tk.get_action("flakes_flake_delete")(
                {}, {"id": tk.request.form["flake_id"]}
            )
            p.plugins_update()

            return tk.redirect_to("flakes_scheming_overrides.edit")

        params = parse_params(tk.request.form)
        if not params:
            tk.h.flash_error("Field is missing")
            return tk.redirect_to("flakes_scheming_overrides.edit")

        flakes = Flake.by_extra(
            {
                "flakes_scheming_overrides": {
                    "schema": params["schema"],
                }
            },
            None,
        )
        for flake in flakes:
            if flake.data["field"] == params["field"]:
                tk.h.flash_error("Remove previous modification of the field")
                return tk.redirect_to("flakes_scheming_overrides.edit")

        if params["type"] == "remove":
            data = {"type": "remove", "field": params["field"]}
        elif params["type"] == "add":
            data = {
                "type": "add",
                "field": params["field"],
                "definition": {
                    "label": params.get("label"),
                    "required": tk.asbool(params.get("required")),
                    "help_text": params.get("help_text"),
                },
            }
        elif params["type"] == "patch":
            data = {
                "type": "patch",
                "field": params["field"],
                "patch": {
                    "label": params.get("label"),
                    "required": tk.asbool(params.get("required")),
                    "help_text": params.get("help_text"),
                },
            }

        else:
            tk.h.flash_error("Wrong type")
            return tk.redirect_to("flakes_scheming_overrides.edit")

        tk.get_action("flakes_flake_override")(
            {},
            {
                "author_id": None,
                "extras": {"flakes_scheming_overrides": {"schema": params["schema"]}},
                "name": f"scheming_overrides:{params['schema']}:{params['field']}",
                "data": data,
            },
        )
        return tk.redirect_to("flakes_scheming_overrides.edit")


bp.add_url_rule(
    "/admin-panel/config/flakes-scheming-overrides", view_func=EditView.as_view("edit")
)
