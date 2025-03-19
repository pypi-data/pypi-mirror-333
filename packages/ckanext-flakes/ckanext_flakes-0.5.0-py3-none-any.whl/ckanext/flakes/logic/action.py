from __future__ import annotations

from collections import ChainMap

import ckan.plugins.toolkit as tk
from ckan import model
from ckan.logic import validate
from ckan.plugins import get_plugin

from ckanext.toolbelt.decorators import Collector

from ..model import Flake
from . import schema

action, get_actions = Collector("flakes").split()


@action
@validate(schema.flake_create)
def flake_create(context, data_dict):
    """Create a flake.

    Args:
        name (str, optional): name of the flake
        data (dict): flake's data
        parent_id (str, optional): ID of flake to extend
        author_id (str, optional): author ID(can be set only by sysadmin)
        extras (dict): flake's extra details

    """
    tk.check_access("flakes_flake_create", context, data_dict)

    author_id = data_dict.pop("author_id", tk.missing)

    if author_id is not None:
        if author_id is tk.missing:
            author_id = context["user"]

        author = model.User.get(author_id)
        if not author:
            raise tk.NotAuthorized()

        author_id = author.id

    sess = context["session"]

    if "parent_id" in data_dict:
        parent = sess.query(Flake).filter_by(id=data_dict["parent_id"]).one_or_none()

        if not parent:
            raise tk.ObjectNotFound()

        if parent.author_id != author_id:
            raise tk.ValidationError({"parent_id": ["Must be owned by the same user"]})

    if (
        "name" in data_dict
        and Flake.by_name(data_dict["name"], author_id).one_or_none()
    ):
        raise tk.ValidationError({"name": ["Must be unique"]})

    flake = Flake(author_id=author_id, **data_dict)
    sess.add(flake)
    sess.commit()

    return flake.dictize(context)


@action
@tk.side_effect_free
@validate(schema.flake_show)
def flake_show(context, data_dict):
    """Display existing flake.

    Args:
        id (str): ID of flake to display
        expand (bool, optional): Extend flake using data from the parent flakes
    """

    tk.check_access("flakes_flake_show", context, data_dict)

    sess = context["session"]
    flake: Flake = sess.query(Flake).filter_by(id=data_dict["id"]).one_or_none()
    if not flake:
        raise tk.ObjectNotFound()

    context["expand"] = data_dict["expand"]

    return flake.dictize(context)


@action
@tk.side_effect_free
@validate(schema.flake_list)
def flake_list(context, data_dict):
    """Display all flakes of the user.

    If `extras` dictionary passed, show only flakes that contains given extras. Example:

        first_flake = Flake(extras={"xxx": {"yyy": "hello"}})
        second_flake = Flake(extras={"xxx": {"yyy": "world"}})

        flake_list(context, {"extras": {"xxx": {"yyy": "hello"}})
        >>> first_flake

    Args:
        expand (bool, optional): Extend flake using data from the parent flakes
        extras (dict, optional): Show only flakes whose extras contains passed dict
    """

    tk.check_access("flakes_flake_list", context, data_dict)

    context["expand"] = data_dict["expand"]

    author_id = data_dict.get("author_id", tk.missing)

    if author_id is not None:
        if author_id is tk.missing:
            author_id = context["user"]

        user = context["model"].User.get(author_id)
        if not user:
            raise tk.ObjectNotFound("User not found")

        author_id = user.id

    if data_dict["extras"]:
        flakes = Flake.by_extra(data_dict["extras"], author_id)
    else:
        flakes = Flake.by_author(author_id)

    return [flake.dictize(context) for flake in flakes]


@action
@validate(schema.flake_update)
def flake_update(context, data_dict):
    """Update existing flake.

    Args:
        id (str): ID of flake to update
        data (dict): flake's data
        parent_id (str, optional): ID of flake to extend
        extras (dict): flake's extra details
    """

    tk.check_access("flakes_flake_update", context, data_dict)

    sess = context["session"]
    flake = sess.query(Flake).filter_by(id=data_dict["id"]).one_or_none()

    if not flake:
        raise tk.ObjectNotFound()

    for k, v in data_dict.items():
        setattr(flake, k, v)
    sess.commit()

    return flake.dictize(context)


@action
@validate(schema.flake_override)
def flake_override(context, data_dict):
    """Update existing flake by name or create a new one.

    Args:
        name (str): Name flake to override
        data (dict): flakes data
        parent_id (str, optional): ID of flake to extend
        author_id (str, optional): author ID(can be set only by sysadmin if flake does not exist)
        extras (dict): flake's extra details
    """
    tk.check_access("flakes_flake_override", context, data_dict)
    try:
        flake = tk.get_action("flakes_flake_lookup")(context.copy(), data_dict)
    except tk.ObjectNotFound:
        action = tk.get_action("flakes_flake_create")
    else:
        action = tk.get_action("flakes_flake_update")
        data_dict["id"] = flake["id"]

    return action(context, data_dict)


@action
@validate(schema.flake_delete)
def flake_delete(context, data_dict):
    """Delete the flake.

    Args:
        id (str): ID of flake to delete
    """

    tk.check_access("flakes_flake_delete", context, data_dict)

    sess = context["session"]
    flake = sess.query(Flake).filter_by(id=data_dict["id"]).one_or_none()

    if not flake:
        raise tk.ObjectNotFound()

    sess.delete(flake)
    sess.commit()

    return flake.dictize(context)


@action
@tk.side_effect_free
@validate(schema.flake_lookup)
def flake_lookup(context, data_dict):
    """Display the flake using its name.

    Args:
        name (str): Name of the flake
        expand (bool, optional): Extend flake using data from the parent flakes
        author_id (str, optional): author ID(can be set only by sysadmin)

    """
    tk.check_access("flakes_flake_lookup", context, data_dict)

    author_id = data_dict.get("author_id", tk.missing)

    if author_id is not None:
        if author_id is tk.missing:
            author_id = context["user"]

        user = context["model"].User.get(author_id)
        if not user:
            raise tk.ObjectNotFound("User not found")

        author_id = user.id

    flake = Flake.by_name(data_dict["name"], author_id).one_or_none()

    if not flake:
        raise tk.ObjectNotFound("Flake not found")

    return flake.dictize(context)


@action
@tk.side_effect_free
@validate(schema.flake_validate)
def flake_validate(context, data_dict):
    """Validate existing flake.

    Schemas must be registered via `IFlakes` interface.

    Args:
        id (str): ID of flake to validate
        expand (bool, optional): Extend flake using data from the parent flakes
        schema(str): validation schema for the flake's data
    """

    tk.check_access("flakes_flake_validate", context, data_dict)
    flake = tk.get_action("flakes_flake_show")(context.copy(), data_dict)

    return tk.get_action("flakes_data_validate")(
        context,
        {
            "data": flake["data"],
            "expand": data_dict["expand"],
            "schema": data_dict["schema"],
        },
    )


@action
@tk.side_effect_free
@validate(schema.data_validate)
def data_validate(context, data_dict):
    """Validate arbitrary data against the named schema(registered via IFlakes).

    Factories must be registered via `IFlakes` interface.

    Args:
        data (dict): data that needs to be validated
        schema(str): validation schema for the data
    """

    tk.check_access("flakes_data_validate", context, data_dict)

    plugin = get_plugin("flakes")
    try:
        schema = plugin.resolve_flake_schema(data_dict["schema"])
    except KeyError:
        raise tk.ValidationError({"schema": ["Does not exist"]})
    data, errors = tk.navl_validate(data_dict["data"], schema, context)

    result = {
        "errors": errors,
    }
    if context.get("include_data"):
        result["data"] = data

    return result


@action
@tk.side_effect_free
@validate(schema.data_example)
def data_example(context, data_dict):
    """Generate an example of the flake's data using named factory(registered via IFlakes).

    Args:
        factory(str): example factory
        data (dict, optional): payload for the example factory
    """

    tk.check_access("flakes_example", context, data_dict)

    plugin = get_plugin("flakes")
    try:
        factory = plugin.resolve_example_factory(data_dict["factory"])
    except KeyError:
        raise tk.ValidationError({"factory": ["Does not exist"]})

    return {"data": factory(data_dict["data"])}


@action
@validate(schema.flake_materialize)
def flake_materialize(context, data_dict):
    """Send flake's data to an API action.

    Args:
        id (str): ID of flake to materialize
        expand (bool, optional): Extend flake using data from the parent flakes
        remove (bool, optional): Remove flake after materialization
        action (str): API action to use for materialization
    """

    tk.check_access("flakes_flake_materialize", context, data_dict)

    flake = tk.get_action("flakes_flake_show")(
        context.copy(),
        {
            "id": data_dict["id"],
            "expand": data_dict["expand"],
        },
    )

    materialization = data_dict["action"](context.copy(), flake["data"])

    if data_dict["remove"]:
        tk.get_action("flakes_flake_delete")(context, {"id": data_dict["id"]})

    return materialization


@action
@tk.side_effect_free
@validate(schema.flake_combine)
def flake_combine(context, data_dict):
    """Combine data from multiple flakes

    `id` argument specifies all the flakes that must be combined. All of the
    flakes must exist, otherwise `NotFound` error raised. IDs at the start of
    the list have higher priority(override matching keys). IDs at the end of
    the list have lower priority(can be shadowed by former flakes).

    `expand` must be a `dict[str, bool]`. Keys are IDs of the flakes, values
    are expand flags for the corresponding flake.

    Args:
        id (list): IDs of flakes.
        expand (dict, optional): Extend flake using data from the parent flakes

    """

    tk.check_access("flakes_flake_combine", context, data_dict)

    show = tk.get_action("flakes_flake_show")
    flakes = (
        show(
            context.copy(),
            {"id": id_, "expand": data_dict["expand"].get(id_, False)},
        )
        for id_ in data_dict["id"]
    )

    result = ChainMap(*(flake["data"] for flake in flakes))

    return dict(result)


@action
@validate(schema.flake_merge)
def flake_merge(context, data_dict):
    """Combine multiple flakes and save the result.

    Args:
        id (list): IDs of flakes.
        expand (dict, optional): Extend flake using data from the parent flakes
        remove (bool, optional): Remove flakes after the operation.
        destination (str, optional): Save data into the specified flake instead
            of a new one
    """

    tk.check_access("flakes_flake_merge", context, data_dict)

    data = tk.get_action("flakes_flake_combine")(
        context.copy(),
        {
            "id": data_dict["id"],
            "expand": data_dict["expand"],
        },
    )

    payload = {"data": data}
    action = tk.get_action("flakes_flake_create")

    if "destination" in data_dict:
        action = tk.get_action("flakes_flake_update")
        payload["id"] = data_dict["destination"]

    result = action(context.copy(), payload)

    delete = tk.get_action("flakes_flake_delete")
    if data_dict["remove"]:
        for id_ in data_dict["id"]:
            if id_ == result["id"]:
                # we've merged data into this flake
                continue

            try:
                delete(context.copy(), {"id": id_})
            except tk.ObjectNotFound:
                # This flake was a child of another flake in queue and was
                # removed recursively
                pass

    return result


@action
@validate(schema.extras_patch)
def extras_patch(context, data_dict):
    """Partially overrides extras leaving other fields intact.

    Args:
        id (str): ID of flake
        extras (dict): patch for extras

    """
    tk.check_access("flakes_extras_patch", context, data_dict)

    flake = tk.get_action("flakes_flake_show")(context.copy(), data_dict)
    flake["extras"].update(data_dict["extras"])

    return tk.get_action("flakes_flake_update")(context, flake)


@action
@validate(schema.data_patch)
def data_patch(context, data_dict):
    """Partially overrides data leaving other fields intact.

    Args:
        id (str): ID of flake
        data (dict): patch for data

    """
    tk.check_access("flakes_data_patch", context, data_dict)

    flake = tk.get_action("flakes_flake_show")(context.copy(), data_dict)
    flake["data"].update(data_dict["data"])

    return tk.get_action("flakes_flake_update")(context, flake)
