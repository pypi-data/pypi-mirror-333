from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True, frozen=True)
class Some[T]:
    """
    Model for the success case of a function in this project.

    Attributes
    ----------
    value : T
        The data returned by the function.
    """

    value: T


@dataclass(slots=True, frozen=True)
class Nothing:
    """
    Model for the error case of a function in this project.

    Attributes
    ----------
    message : str
        A message describing the error.
    code : int
        A code that can be used to handle different error cases.
    """

    pass


type Maybe[T] = Some[T] | Nothing


def mmap[T, U](f: Callable[[T], U], maybe: Some[T] | Nothing) -> Some[U] | Nothing:
    """
    Map a function over a Maybe.

    Parameters
    ----------
    f : Callable[[T], U]
        The function to map over the Maybe.
    maybe : Maybe[T]
        The Maybe to map the function over.

    Returns
    -------
    Maybe[U]
    """
    match maybe:
        case Some(value=value):
            return Some(value=f(value))
        case Nothing():
            return maybe
        case _:
            raise ValueError("Invalid Maybe type.")


def mbind[T, U](f: Callable[[T], Some[U] | Nothing], maybe: Some[T] | Nothing) -> Some[U] | Nothing:
    """
    Bind a function over a Maybe.

    Parameters
    ----------
    f : Callable[[T], Some[U] | Nothing]
        The function to bind over the Maybe.
    maybe : Maybe[T]
        The Maybe to bind the function over.

    Returns
    -------
    Maybe[U]
    """
    match maybe:
        case Some(value):
            return f(value)
        case Nothing():
            return maybe
        case _:
            raise ValueError("Invalid Maybe type.")


def munwrap[T](maybe: Some[T] | Nothing) -> T:
    """
    Unwrap a Maybe.

    Parameters
    ----------
    maybe : Maybe[T]
        The Maybe to unwrap.

    Returns
    -------
    T
        The value of the Maybe.
    """
    match maybe:
        case Some(value):
            return value
        case Nothing():
            raise ValueError("Cannot unwrap a Nothing.")
        case _:
            raise ValueError("Invalid Maybe type.")


def munwrap_or[T](maybe: Some[T] | Nothing, default: T) -> T:
    """
    Unwrap a Maybe or return a default value.

    Parameters
    ----------
    maybe : Maybe[T]
        The Maybe to unwrap.
    default : T
        The default value to return if the Maybe is a Nothing.

    Returns
    -------
    T
        The value of the Maybe or the default value.
    """
    match maybe:
        case Some(value):
            return value
        case Nothing():
            return default
        case _:
            raise ValueError("Invalid Maybe type.")
