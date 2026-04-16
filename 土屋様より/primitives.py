from typing import Optional, Protocol, Tuple, cast  # type: ignore
from varmain.primitiv import *  # type: ignore

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

Vector3d = Tuple[float, float, float]


# ---------------------------------------------------------------------------
# Protocol: describes the varmain shape-object interface
#
# Modifier functions (mutate the shape):
#   uniteWith, subtractFrom, intersectWith, erase
#   rotateX, rotateY, rotateZ, translate, setTransformationMatrix, setPoint
#
# Request functions (read-only):
#   parameters, transformationMatrix, numberOfPoints, pointAt, directionAt
# ---------------------------------------------------------------------------

class ShapeProtocol(Protocol):
    """Type-hint protocol for varmain shape objects returned by primitives.

    Usage example::

        o1: ShapeProtocol = CYLINDER(s, R=50.0, H=100.0)
        o1.rotateY(90).translate((25.0, 0, 0))
        o2: ShapeProtocol = BOX(s, L=50.0, W=50.0, H=20.0)
        o1.uniteWith(o2)
        o2.erase()
        s.setPoint((0, 0, 0), (-1, 0, 0))
    """

    # --- modifier functions ------------------------------------------------

    def uniteWith(self, other: "ShapeProtocol") -> "ShapeProtocol":
        """Unite this object with *other*. Result is stored in this object.

        *other* must be erased after the call::

            obj.uniteWith(other)
            other.erase()
        """
        ...

    def subtractFrom(self, other: "ShapeProtocol") -> "ShapeProtocol":
        """Subtract *other* from this object. Result is stored in this object.

        *other* must be erased after the call::

            obj.subtractFrom(other)
            other.erase()
        """
        ...

    def intersectWith(self, other: "ShapeProtocol") -> "ShapeProtocol":
        """Create an intersection of this object and *other*.

        *other* must be erased after the call::

            obj.intersectWith(other)
            other.erase()
        """
        ...

    def erase(self) -> None:
        """Remove this object from memory.

        Always call after uniteWith / subtractFrom / intersectWith.
        """
        ...

    def rotateX(self, angle: float) -> "ShapeProtocol":
        """Rotate around the X-axis by *angle* degrees."""
        ...

    def rotateY(self, angle: float) -> "ShapeProtocol":
        """Rotate around the Y-axis by *angle* degrees."""
        ...

    def rotateZ(self, angle: float) -> "ShapeProtocol":
        """Rotate around the Z-axis by *angle* degrees."""
        ...

    def translate(self, v: Vector3d) -> "ShapeProtocol":
        """Move by vector *v* = (x, y, z)."""
        ...

    def setTransformationMatrix(self, t) -> None:
        """Apply a transformation matrix *t* (mTransform)."""
        ...

    def setPoint(self, p: Vector3d, v: Vector3d, a: float = 0.0) -> None:
        """Append a connection point at position *p* with direction *v*.

        Args:
            p: Position as (x, y, z).
            v: Direction vector as (x, y, z).
            a: Optional rotation angle in degrees (for elliptical flanges).
        """
        ...

    # --- request functions -------------------------------------------------

    def parameters(self) -> dict:
        """Return the object's construction parameters as a dict.

        Example for TORISPHERICHEAD — height can be read as::

            vT = obj.parameters()
            h = float(vT["H"])
        """
        ...

    def transformationMatrix(self):
        """Return the object's current transformation matrix (mTransform)."""
        ...

    def numberOfPoints(self) -> int:
        """Return the number of connection points on this object."""
        ...

    def pointAt(self, n: int, inECS: int = 0):
        """Return the position of connection point *n* as mPoint.

        Args:
            n: 0-based index of the connection point.
            inECS: If 1, return in Entity Coordinate System (not WCS).
        """
        ...

    def directionAt(self, n: int, inECS: int = 0):
        """Return the direction at connection point *n* as mVector.

        Args:
            n: 0-based index of the connection point.
            inECS: If 1, return in Entity Coordinate System (not WCS).
        """
        ...


# ---------------------------------------------------------------------------
# Helper types
# ---------------------------------------------------------------------------

class Point3d:
    """Simple 3-D point used for port position / direction arguments."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def set_port(s, point: Point3d, direction: Point3d) -> None:
    """Append a connection port on shape *s*.

    Thin wrapper around ``s.setPoint`` that accepts :class:`Point3d` objects
    instead of raw tuples.

    Args:
        s: The main shape object.
        point: Port position in 3-D space.
        direction: Port direction vector (unit vector pointing outward).

    Example::

        set_port(s, Point3d(0, 0, 0), Point3d(-1, 0, 0))  # inlet at origin
        set_port(s, Point3d(L, 0, 0), Point3d(1, 0, 0))   # outlet at x=L
    """
    s.setPoint(
        (point.x, point.y, point.z),
        (direction.x, direction.y, direction.z),
    )


def set_dimension(s, name: str, start: Point3d, end: Point3d) -> None:
    """Reserve a named dimension annotation from *start* to *end*.

    This is a placeholder; actual dimension display is handled by Plant 3D
    metadata (variants.xml / @param decorators), not by the geometry script.

    Args:
        s: The main shape object.
        name: Dimension identifier (matches a ``@param`` name).
        start: Dimension start point.
        end: Dimension end point.
    """
    pass


# ---------------------------------------------------------------------------
# Abstract base for wrapper classes (marker only)
# ---------------------------------------------------------------------------

class ShapeObject:
    """Marker base class for Plant 3D primitive wrappers.

    Each subclass overrides ``__new__`` to construct the underlying varmain
    shape and return it directly, so callers receive a native shape object
    (which satisfies :class:`ShapeProtocol`) rather than a Python wrapper.
    """
    pass


# ---------------------------------------------------------------------------
# Box primitives
# ---------------------------------------------------------------------------

class Box(ShapeObject):
    """Rectangular box (BOX).

    The varmain BOX base point is the center of gravity.  This wrapper
    translates the shape so that the **bottom face** aligns with z = 0.

    Args:
        s: Main shape object.
        l: Length (X-axis).
        w: Width (Y-axis).
        h: Height (Z-axis).

    Returns:
        varmain shape object (satisfies :class:`ShapeProtocol`).

    Example::

        body = Box(s, l=100.0, w=60.0, h=40.0)
    """

    def __new__(cls, s, l: float, w: float, h: float):
        shape = BOX(s, L=l, W=w, H=h)
        shape.translate((0, 0, h / 2))
        return shape  # varmain shape object


# ---------------------------------------------------------------------------
# Cylindrical / conical primitives
# ---------------------------------------------------------------------------

class Cylinder(ShapeObject):
    """Normal or elliptical cylinder (CYLINDER).

    The varmain CYLINDER base point is the **center of bottom**.  This wrapper
    translates the shape upward by h/2 so the geometric center is at z = h/2.

    Args:
        s: Main shape object.
        r: Radius (use r for circular; Plant 3D also supports R1/R2 for
           elliptical cylinders — call ``CYLINDER`` directly for that case).
        h: Height.
        o: Hole radius (0.0 = solid). Defaults to 0.0.

    Returns:
        varmain shape object.

    Example::

        pipe = Cylinder(s, r=57.15, h=200.0, o=50.0)  # hollow pipe
    """

    def __new__(cls, s, r: float, h: float, o: float = 0.0):
        shape = CYLINDER(s, R=r, H=h, O=o)
        shape.translate((0, 0, h / 2))
        return shape  # varmain shape object


class Cone(ShapeObject):
    """Cone or frustum (CONE).

    The varmain CONE base point is the **center of bottom**.  This wrapper
    translates the shape upward by h/2.

    Args:
        s: Main shape object.
        r1: Bottom radius.
        r2: Upper radius (0.0 → full cone; > 0.0 → frustum).
        h: Height.
        e: Eccentricity between upper and bottom centers. Defaults to 0.0.

    Returns:
        varmain shape object.

    Example::

        reducer = Cone(s, r1=60.0, r2=40.0, h=80.0)
    """

    def __new__(cls, s, r1: float, r2: float, h: float, e: float = 0.0):
        shape = CONE(s, R1=r1, R2=r2, H=h, E=e)
        shape.translate((0, 0, h / 2))
        return shape  # varmain shape object


# ---------------------------------------------------------------------------
# Elbow / arc primitives
# ---------------------------------------------------------------------------

class Elbow(ShapeObject):
    """Normal elbow (ARC3D).

    Base point: intersection of the thought centerlines through both ends.

    Args:
        s: Main shape object.
        d: Half-diameter (= outer radius of the pipe wall).
        r: Bend radius (centerline radius).
        a: Bend angle in degrees.

    Returns:
        varmain shape object.

    Example::

        elbow90 = Elbow(s, d=57.15, r=76.2, a=90.0)
    """

    def __new__(cls, s, d: float, r: float, a: float):
        return ARC3D(s, D=d, R=r, A=a)


class ReducedElbow(ShapeObject):
    """Reduced elbow (ARC3D2).

    Like :class:`Elbow` but allows different diameters at each end.

    Base point: intersection of the thought centerlines through both ends.

    Args:
        s: Main shape object.
        d: Half-diameter at port 0.
        r: Bend radius (centerline radius).
        a: Bend angle in degrees.
        d2: Half-diameter at port 1.  If ``None`` (default) *d* is used.

    Returns:
        varmain shape object.

    Example::

        reducer_elbow = ReducedElbow(s, d=57.15, r=76.2, a=90.0, d2=44.45)
    """

    def __new__(cls, s, d: float, r: float, a: float, d2: Optional[float] = None):
        if d2 is None:
            return ARC3D2(s, D=d, R=r, A=a)
        return ARC3D2(s, D=d, D2=d2, R=r, A=a)


class SegmentedElbow(ShapeObject):
    """Segmented elbow (ARC3DS).

    Base point: intersection of the thought centerlines through both ends.

    Args:
        s: Main shape object.
        d: Half-diameter.
        r: Bend radius (centerline radius).
        a: Bend angle in degrees.
        seg: Number of straight segments. Defaults to 3.

    Returns:
        varmain shape object.

    Example::

        seg_elbow = SegmentedElbow(s, d=57.15, r=152.4, a=90.0, seg=5)
    """

    def __new__(cls, s, d: float, r: float, a: float, seg: int = 3):
        return ARC3DS(s, D=d, R=r, A=a, S=seg)


# ---------------------------------------------------------------------------
# Head / dome primitives
# ---------------------------------------------------------------------------

class EllipsoidHead(ShapeObject):
    """Normalized ellipsoid head (ELLIPSOIDHEAD).

    Formed as an ellipse; b-axis = r (normalized).
    Base point: center of bottom.
    Use ``.parameters()`` to retrieve the computed height H.

    Args:
        s: Main shape object.
        r: Radius (a-axis).

    Returns:
        varmain shape object.

    Example::

        head = EllipsoidHead(s, r=300.0)
        h = float(head.parameters()["H"])
    """

    def __new__(cls, s, r: float):
        return ELLIPSOIDHEAD(s, R=r)


class EllipsoidHead2(ShapeObject):
    """Ellipsoid head with b = 0.5 * R (ELLIPSOIDHEAD2).

    More shallow than :class:`EllipsoidHead`.
    Base point: center of bottom.
    Use ``.parameters()`` to retrieve the computed height H.

    Args:
        s: Main shape object.
        r: Radius (a-axis; b-axis = 0.5 * r).

    Returns:
        varmain shape object.

    Example::

        head = EllipsoidHead2(s, r=300.0)
    """

    def __new__(cls, s, r: float):
        return ELLIPSOIDHEAD2(s, R=r)


class EllipsoidSegment(ShapeObject):
    """Ellipsoid body (football / rugby-ball shape) (ELLIPSOIDSEGMENT).

    Base point: center of gravity.

    Args:
        s: Main shape object.
        rx: Major (big) ellipsoid axis.
        ry: Minor (small) ellipsoid axis.
        a1: Complete rotation angle.
        a2: Start angle of rotation.
        a3: Start angle of ellipse arc.
        a4: End angle of ellipse arc.

    Returns:
        varmain shape object.
    """

    def __new__(
        cls,
        s,
        rx: float,
        ry: float,
        a1: float,
        a2: float,
        a3: float,
        a4: float,
    ):
        return ELLIPSOIDSEGMENT(s, RX=rx, RY=ry, A1=a1, A2=a2, A3=a3, A4=a4)


class HalfSphere(ShapeObject):
    """Half sphere (HALFSPHERE).

    Base point: center of the flat bottom face.

    Args:
        s: Main shape object.
        r: Radius.

    Returns:
        varmain shape object.

    Example::

        dome = HalfSphere(s, r=150.0)
    """

    def __new__(cls, s, r: float):
        return HALFSPHERE(s, R=r)


class TorisphericHead(ShapeObject):
    """Normalized torispheric head (TORISPHERICHEAD).

    Base point: center of bottom.
    Use ``.parameters()`` to retrieve the computed height H.

    Args:
        s: Main shape object.
        r: Radius.

    Returns:
        varmain shape object.

    Example::

        head = TorisphericHead(s, r=300.0)
        h = float(head.parameters()["H"])
        head.rotateY(90.0).translate((L - h, 0.0, 0.0))
    """

    def __new__(cls, s, r: float):
        return TORISPHERICHEAD(s, R=r)


class TorisphericHead2(ShapeObject):
    """Torispheric head with small radius = 25.00 (TORISPHERICHEAD2).

    Base point: center of bottom.
    Use ``.parameters()`` to retrieve the computed height H.

    Args:
        s: Main shape object.
        r: Radius.

    Returns:
        varmain shape object.
    """

    def __new__(cls, s, r: float):
        return TORISPHERICHEAD2(s, R=r)


class TorisphericHeadH(ShapeObject):
    """Normalized torispheric head with explicit height (TORISPHERICHEADH).

    Use when the head must fit within a fixed axial length.
    Base point: center of bottom.

    Args:
        s: Main shape object.
        r: Radius.
        h: Height (overrides the normalized default).

    Returns:
        varmain shape object.
    """

    def __new__(cls, s, r: float, h: float):
        return TORISPHERICHEADH(s, R=r, H=h)


# ---------------------------------------------------------------------------
# Miscellaneous solid primitives
# ---------------------------------------------------------------------------

class Pyramid(ShapeObject):
    """Pyramid or frustum of pyramid (PYRAMID).

    Base point: center of the bottom rectangle.

    Args:
        s: Main shape object.
        l: Length of the base rectangle.
        w: Width of the base rectangle.
        h: Frustum height.  If *ht* is not given this is the total height.
        ht: Total pyramid height (optional; used to create a frustum).

    Returns:
        varmain shape object.

    Example::

        # Full pyramid
        pyr = Pyramid(s, l=100.0, w=100.0, h=150.0)
        # Truncated pyramid (frustum)
        pyr = Pyramid(s, l=100.0, w=100.0, h=80.0, ht=150.0)
    """

    def __new__(cls, s, l: float, w: float, h: float, ht: Optional[float] = None):
        if ht is None:
            return PYRAMID(s, L=l, W=w, H=h)
        return PYRAMID(s, L=l, W=w, H=h, HT=ht)


class RoundRect(ShapeObject):
    """Transition from a rectangle to a circle (ROUNDRECT).

    Useful for square-to-round duct transitions.
    Base point: center of the rectangle (bottom face).

    Args:
        s: Main shape object.
        l: Length of the rectangle.
        w: Width of the rectangle.
        h: Height of the transition body.
        r2: Radius of the circle at the top.
        e: Eccentricity between upper and bottom centers. Defaults to 0.0.

    Returns:
        varmain shape object.

    Example::

        transition = RoundRect(s, l=200.0, w=150.0, h=100.0, r2=60.0)
    """

    def __new__(cls, s, l: float, w: float, h: float, r2: float, e: float = 0.0):
        return ROUNDRECT(s, L=l, W=w, H=h, R2=r2, E=e)


class SphereSegment(ShapeObject):
    """Sphere segment (SPHERESEGMENT).

    Base point: center of the lower part of the segment.

    Args:
        s: Main shape object.
        r: Sphere radius.
        p: Segment height (axial extent of the cut).
        q: Height where the segment starts, measured from the sphere center.

    Returns:
        varmain shape object.

    Example::

        cap = SphereSegment(s, r=200.0, p=50.0, q=0.0)
    """

    def __new__(cls, s, r: float, p: float, q: float):
        return SPHERESEGMENT(s, R=r, P=p, Q=q)


class Torus(ShapeObject):
    """Torus (TORUS).

    Base point: intersection of the thought centerlines through both ends.

    Args:
        s: Main shape object.
        r1: Outer radius (distance from torus center to tube center).
        r2: Inner radius (tube cross-section radius).

    Returns:
        varmain shape object.

    Example::

        ring = Torus(s, r1=100.0, r2=20.0)
    """

    def __new__(cls, s, r1: float, r2: float):
        return TORUS(s, R1=r1, R2=r2)
