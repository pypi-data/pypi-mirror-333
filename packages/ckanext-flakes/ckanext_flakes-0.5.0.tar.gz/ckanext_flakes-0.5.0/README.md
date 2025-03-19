[![Tests](https://github.com/DataShades/ckanext-flakes/workflows/Tests/badge.svg)](https://github.com/DataShades/ckanext-flakes/actions/workflows/test.yml)

# ckanext-flakes

Tools for creating and managing independent chunks of data.

This extension provides a base entity for storing arbitrary data. It can be
used in a number of cases, especially, if you don't want yet to create a brand
new model, database migrations and tables, but you have no other options.

`ckanext-flakes` gives you a set of actions for creating and managing small
dictionary-like objects(anything, that can be serialized into JSON). If you are
using it and want to add an extra action, feel free to create a PR or an issue
with your suggestion.

## Structure

* [Examples](#examples)
* [Example plugins](#example-plugins)
* [Requirements](#definition)
* [Installation](#installation)
* [Configuration](#configuration)
* [Interfaces](#interfaces)
* [API](#api)
  * [`flakes_flake_create`](#flakes_flake_create)
  * [`flakes_flake_show`](#flakes_flake_show)
  * [`flakes_flake_list`](#flakes_flake_list)
  * [`flakes_flake_update`](#flakes_flake_update)
  * [`flakes_flake_override`](#flakes_flake_override)
  * [`flakes_flake_delete`](#flakes_flake_delete)
  * [`flakes_flake_lookup`](#flakes_flake_lookup)
  * [`flakes_flake_validate`](#flakes_flake_validate)
  * [`flakes_data_validate`](#flakes_data_validate)
  * [`flakes_data_example`](#flakes_data_example)
  * [`flakes_flake_materialize`](#flakes_flake_materialize)
  * [`flakes_flake_combine`](#flakes_flake_combine)
  * [`flakes_flake_merge`](#flakes_flake_merge)
  * [`flakes_data_patch`](#flakes_data_patch)
  * [`flakes_extras_patch`](#flakes_extras_patch)

## Examples

### Create a collection of records

Scenario: user needs a todo list

Flakes created by any user are visible only to this user so flakes can be used
as a storage for private data.

Flakes can have `extras`, that plays a role of tags. `extras` represented by a
dictionary and whenever user lists his flakes, he has an option to see only
flakes that contains particular data inside extras.

```python
flake_create = tk.get_action("flakes_flake_create")
flake_list = tk.get_action("flakes_flake_create")

# create an urgent taks
flake_create(
    {"user": "john"},
    {"data": {"task": "feed the cat"}, "extras": {"when": "today", "type": "task"}}
)

# create a couple of tasks that can wait
flake_create(
    {"user": "john"},
    {"data": {"task": "buy food"}, "extras": {"when": "tomorrow", "type": "task"}}
)
flake_create(
    {"user": "john"},
    {"data": {"task": "update documentation"}, "extras": {"when": "tomorrow", "type": "task"}}
)

# list all the tasks
flake_list(
    {"user": "john"},
    {"extras": {"type": "task"}}
)

# list all the urgent tasks
flake_list(
    {"user": "john"},
    {"extras": {"type": "task", "when": "today"}}
)

# list all the tasks for tomorrow
flake_list(
    {"user": "john"},
    {"extras": {"type": "task", "when": "tomorrow"}}
)
```

### Save the value of the option individually for every user

Scenario: each user can set a theme of application and this theme will be applied only for the current user

Flakes are created for the user from the `context`. Flakes of the user A are
visible only to the user A, flakes of the user B exist in the different
namespace and are visible only to the user B.

Each flake **can** have a name. Name must be unique among the flakes of the
user. But different users can use the same names for their flakes, because
every user has its own namespace for flakes.

Flakes can be created either via `flakes_flake_create` action(accepts
**optional** name and raises exception if name is not unique) or
`flakes_flake_override`(requires a name and creates a new flake if name is not
taken or updates existing flake if name already used by some flake)

In order to get the flake use `flakes_flake_show` with the `id` of the flake or
`flakes_flake_lookup` with the `name`.

```python
# set a theme for John
tk.get_action("flakes_flake_override")(
    {"user": "john"},
    {"name": "application:theme", "data": {"theme": "dark"}}
)

# set a theme for Mary
tk.get_action("flakes_flake_override")(
    {"user": "mary"},
    {"name": "application:theme", "data": {"theme": "light"}}
)


# get the value from the flake
john_theme = tk.get_action("flakes_flake_lookup")(
    {"user": "john"},
    {"name": "application:theme"}
)["data"]["theme"]

mary_theme = tk.get_action("flakes_flake_lookup")(
    {"user": "mary"},
    {"name": "application:theme"}
)["data"]["theme"]

assert john_theme == "dark"
assert mary_theme == "light"
```

### Create and obtain global variable

Scenario: application requires global option, that can be changed in runtime

By default flakes are created in the "namespace" of the current user. Only the
author can see and modify his own flakes.

Global values should not be owned by someone, so here we need "unowned" flake -
the flake that is not connected to the particular user. Only sysadmin can
create such flakes, so we are going to use `ignore_auth=True` attribute of the
context.

We'll use `flakes_flake_override` action, that accepts a `name` of the flake
and either updates existing flakes with this name or creates a new one if this
name is free. In this way we'll avoid duplicates of the global flake.


```python
# create a flake
tk.get_action("flakes_flake_override")(
    {"ignore_auth": True}, # only syadmin allowed to create unowned flakes with empty author id
    {"name": "global:config:value", "data": {"value": 1}, "author_id": None}
)

# get the value from the flake
value = tk.get_action("flakes_flake_lookup")(
    {"ignore_auth": True},
    {"name": "global:config:value", "author_id": None}
)["data"]["value"]
```


## Example plugins

These plugins implement basic features that can be used as a real-life example
of `ckanext-flakes` usage.

### `flakes_rating`

User can rate a package via API action. Add
`ckanext.flakes_rating.show_package_widget = true` to the config and default
widget will be added to the sidebar on `dataset.read` page.

### `flakes_feedback`

User can leave a feedback for package via API action. Add
`ckanext.flakes_feedback.enable_views = true` to the config and default page
will be added to navigation tabs on `dataset.read` page.

## Requirements

Requires python v3.7 or greater. Python v2 support doesn't require much effort,
but it neither worth the time you'll spend on it.


Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.9          | yes         |
| 2.10         | yes         |


## Installation

To install ckanext-flakes:

1. Install it via **pip**:
   ```sh
   pip install ckanext-flakes
   ```
1. Add `flakes` to the `ckan.plugins` setting in your CKAN config file.
1. Run DB migrations:
   ```sh
   ckan db upgrade -p flakes
   ```

## Configuration

```ini
# Any user can create a new flake.
# (optional, default: true)
ckanext.flakes.creation.allowed = false

# Any user can validate flake or plain data.
# (optional, default: false)
ckanext.flakes.validation.allowed = true
```

## Interfaces

Provides `ckanext.flakes.interfaces.IFlakes` interface. Always use
`inherit=True` when implementing it, because it may change in the future.

Currently it provides the following hooks:

```python
class IFlakes(Interface):
    """Extend functionality of ckanext-flakes"""

    def get_flake_schemas(self) -> dict[str, dict[str, Any]]:
        """Register named validation schemas.

        Used by `flakes_flake_validate` and `flakes_data_validate` actions.

        Returns:
            Mapping of names and corresponding validation schemas.

        Example:
            def get_flake_schemas(self) -> dict[str, dict[str, Any]]:
                return {
                    "schema-that-requires-name": {"name": [not_missing]}
                }
        """
        return {}

    def get_flake_factories(self) -> dict[str, Callable[[dict[str, Any]], dict[str, Any]]]:
        """Register named example factories.

        Used by `flakes_data_example` action.

        Returns:
            Mapping of names and corresponding example factories.

        Example:
            def get_flake_factories(self) -> dict[str, dict[str, Any]]:
                def factory(payload: dict[str, Any]):
                    return {"field": "value"}

                return {
                    "test-factory": factory
                }
        """
        return {}
```


## API

### `flakes_flake_create`

Create a flake.

Args:

    name (str, optional): name of the flake
    data (dict): flake's data
    parent_id (str, optional): ID of flake to extend
    author_id (str, optional): author ID(can be set only by sysadmin)
    extras (dict): flake's extra details

### `flakes_flake_show`

Display existing flake

Args:

    id (str): ID of flake to display
    expand (bool, optional): Extend flake using data from the parent flakes


### `flakes_flake_list`

Display all flakes of the user.

If `extras` dictionary passed, show only flakes that contains given extras. Example:

    first_flake = Flake(extras={"xxx": {"yyy": "hello"}})
    second_flake = Flake(extras={"xxx": {"yyy": "world"}})

    flake_list(context, {"extras": {"xxx": {"yyy": "hello"}})
    >>> first_flake

Args:

    expand (bool, optional): Extend flake using data from the parent flakes
    extras (dict, optional): Show only flakes whose extras contains passed dict
    author_id (str, optional): author ID(can be set only by sysadmin)

### `flakes_flake_update`

Update existing flake

Args:

    id (str): ID of flake to update
    data (dict): flake's data
    parent_id (str, optional): ID of flake to extend
    extras (dict): flake's extra details

### `flakes_flake_override`

Update existing flake by name or create a new one.

Args:

    name (str): Name flake to override
    data (dict): template itself
    parent_id (str, optional): ID of flake to extend
    author_id (str, optional): author ID(can be set only by sysadmin if flake does not exist)
    extras (dict): flake's extra details

### `flakes_flake_delete`

Delete existing flake

Args:

    id (str): ID of flake to delete

### `flakes_flake_lookup`

Display flake using its name.

Args:

    name (str): Name of the flake
    expand (bool, optional): Extend flake using data from the parent flakes
    author_id (str, optional): author ID(can be set only by sysadmin)

### `flakes_flake_validate`

Validate existing flake

Schemas must be registered via `IFlakes` interface.

Args:

    id (str): ID of flake to validate
    expand (bool, optional): Extend flake using data from the parent flakes
    schema(str): validation schema for the flake's data


### `flakes_data_validate`

Validate arbitrary data against the named schema(registered via IFlakes).

Args:

    data (dict): data that needs to be validated
    schema(str): validation schema for the data

### `flakes_data_example`

Generate an example of the flake's data using named factory(registered via IFlakes).

Factories must be registered via `IFlakes` interface.

Args:

    factory(str): example factory
    data (dict, optional): payload for the example factory

### `flakes_flake_materialize`

Send flake's data to API action.

Args:

    id (str): ID of flake to materialize
    expand (bool, optional): Extend flake using data from the parent flakes
    remove (bool, optional): Remove flake after materialization
    action (str): API action to use for materialization

### `flakes_flake_combine`

Combine data from multiple flakes

`id` argument specifies all the flakes that must be combined. All of the flakes
must exist, otherwise `NotFound` error raised. IDs at the start of the list have
higher priority(override matching keys). IDs at the end of the list have lower
priority(can be shadowed by former flakes).

`expand` must be a `dict[str, bool]`. Keys are IDs of the flakes, values are
expand flags for the corresponding flake.

Args:

    id (list): IDs of flakes.
    expand (dict, optional): Extend flake using data from the parent flakes

### `flakes_flake_merge`

Combine multiple flakes and save the result.

Args:

    id (list): IDs of flakes.
    expand (dict, optional): Extend flake using data from the parent flakes
    remove (bool, optional): Remove flakes after the operation.
    destination (str, optional): Save data into the specified flake instead of a new one

### `flakes_data_patch`

Partially overrides data leaving other fields intact.

Args:

    id (str): ID of flake
    data (dict): patch for data


### `flakes_extras_patch`

Partially overrides extras leaving other fields intact.

Args:

    id (str): ID of flake
    extras (dict): patch for extras

## Developer installation

To install ckanext-flakes for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/DataShades/ckanext-flakes.git
    cd ckanext-flakes
    python setup.py develop


## Tests

To run the tests, do:

    pytest

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
