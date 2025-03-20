"""Reflex custom component Mafs."""

# For wrapping react guide, visit https://reflex.dev/docs/wrapping-react/overview/

import reflex as rx
from typing import List
# Some libraries you want to wrap may require dynamic imports.
# This is because they they may not be compatible with Server-Side Rendering (SSR).
# To handle this in Reflex, all you need to do is subclass `NoSSRComponent` instead.
# For example:
# from reflex.components.component import NoSSRComponent
# class Mafs(NoSSRComponent):
#     pass


class Mafs(rx.Component):
    """Mafs component."""

    # The React library to wrap.
    library = "mafs"

    # The React component tag.
    tag = "Mafs"

    # If the tag is the default export from the module, you must set is_default = True.
    # This is normally used when components don't have curly braces around them when importing.
    # is_default = True

    # If you are wrapping another components with the same tag as a component in your project
    # you can use aliases to differentiate between them and avoid naming conflicts.
    # alias = "OtherMafs"

    # The props of the React component.
    # Note: when Reflex compiles the component to Javascript,
    # `snake_case` property names are automatically formatted as `camelCase`.
    # The prop names may be defined in `camelCase` as well.
    # some_prop: rx.Var[str] = "some default value"
    # some_other_prop: rx.Var[int] = 1
    width: rx.Var[float | int]

    height: rx.Var[float | int]

    pan: rx.Var[bool]

    zoom: rx.Var[bool]

    view_box: rx.Var[dict[str, list[float | int]]]

    preserve_aspect_ratio: rx.Var[bool] = False

    padding: float = 20.0

    debug: rx.Var[bool] = None


    # By default Reflex will install the library you have specified in the library property.
    # However, sometimes you may need to install other libraries to use a component.
    # In this case you can use the lib_dependencies property to specify other libraries to install.
    # lib_dependencies: list[str] = []

    # Event triggers declaration if any.
    # Below is equivalent to merging `{ "on_change": lambda e: [e] }`
    # onto the default event triggers of parent/base Component.
    # The function defined for the `on_change` trigger maps event for the javascript
    # trigger to what will be passed to the backend event handler function.
    # on_change: rx.EventHandler[lambda e: [e]]

    # To add custom code to your component
    # def _get_custom_code(self) -> str:
    #     return "const customCode = 'customCode';"
    def add_imports(self):
        return {"": ["mafs/core.css"]}
    
class CoordinatesCartesian(Mafs):
    tag = "Coordinates.Cartesian"
    _valid_parents: List[str] = ["Mafs"]

    x_axis: rx.Var[dict]
    y_axis: rx.Var[dict]

class MovablePoint(Mafs):
    tag = "MovablePoint"

    point: rx.Var[list[float| int]] = [0.0, 0.0]

    on_move: rx.EventHandler[lambda e0: [e0]]

class Vector(Mafs):
    tag = "Vector"

    tail: rx.Var[list[float| int]]

    tip: rx.Var[list[float| int]]

    svg_line_props: rx.Var[dict]

    color: rx.Var[str]

class Polygon(Mafs):
    tag = "Polygon"

    points: rx.Var[list[list[float | int]]]
    # fill: rx.Var[str]
    # stroke: rx.Var[str]
    # strokeWidth: rx.Var[float | int]

mafs = Mafs.create
coordinates_cartesian = CoordinatesCartesian.create
movable_point = MovablePoint.create
vector = Vector.create
polygon = Polygon.create