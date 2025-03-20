from dataclasses import dataclass
from logging import Logger
from typing import Any, Callable
from functools import wraps


@dataclass(slots=True, frozen=True)
class Ok[T]:
    """
    Model for the success case of a function in this project.

    Attributes
    ----------
    out : T
        The data returned by the function.
    """

    out: T


@dataclass(slots=True, frozen=True)
class Err:
    """
    Model for the error case of a function in this project.

    Attributes
    ----------
    message : str
        A message describing the error.
    code : int
        A code that can be used to handle different error cases.
    error_type : str, optional
        A string describing the type of error that occurred.
    error_trace : str, optional
        A string describing the trace of the error that occurred.
    """

    message: str
    code: int
    error_type: str | None = None
    error_trace: str | None = None


type TResult[T] = Ok[T] | Err


def rmap[T, U](f: Callable[[T], U], result: TResult[T]) -> TResult[U]:
    """
    Map a function over a Result.

    Parameters
    ----------
    f : Callable[[T], U]
        The function to map over the Result.
    result : Result[T]
        The Result to map the function over.

    Returns
    -------
    Result[U]
        The Result with the function mapped over it.
    """

    match result:
        case Ok(out=data):
            return Ok(out=f(data))
        case Err(message=msg, code=code):
            return Err(message=msg, code=code)
        case _:
            raise ValueError("Unknown Result type.")


def rbind[T, U](f: Callable[[T], TResult[U]], result: TResult[T]) -> TResult[U]:
    """
    "result bind". Binds a function to a Result.

    Parameters
    ----------
    f : Callable[[T], Result[E]]
        The function to bind to the Result.
    result : Result[T]
        The Result to bind the function to.

    Returns
    -------
    Result[E]
        The Result with the function bound to it.
    """

    match result:
        case Ok(out=data):
            return f(data)
        case Err(message=msg, code=code):
            return Err(message=msg, code=code)
        case _:
            raise ValueError("Unknown Result type.")


def runwrap[T](result: TResult[T]) -> T:
    """
    Unwrap a Result.

    Parameters
    ----------
    result : Result[T]
        The Result to unwrap.

    Returns
    -------
    T
        The data inside the Result.

    Raises
    ------
    ValueError
        If the Result is an Err.
    """

    match result:
        case Ok(out=data):
            return data
        case Err(message=msg, code=code):
            raise ValueError(f"Error: {msg}")


def runwrap_or[T](result: TResult[T], default: T) -> T:
    """
    Unwrap a Result, returning a default value if the Result is an Err.

    Parameters
    ----------
    result : Result[T]
        The Result to unwrap.
    default : T
        The default value to return if the Result is an Err.

    Returns
    -------
    T
        The data inside the Result, or the default value if the Result is an Err.
    """

    match result:
        case Ok(out=data):
            return data
        case Err(message=msg, code=code):
            return default


def try_except_wrapper[T](logger: Logger) -> Callable[[Callable[..., T]], Callable[..., TResult[T]]]:
    """
    Decorator that wraps a function in a try-except block, logging any errors that occur. The wrapped function will then always return a Ok[T] or Err as output.

    """

    def decorator(func: Callable[..., T]) -> Callable[..., TResult[T]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> TResult[T]:
            try:
                # logger.debug(f"Calling function '{func.__name__}' with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)

                match result:
                    case Err(message=msg, code=code):
                        return result
                    case Ok():
                        # logger.debug(f"Function '{func.__name__}' executed successfully.")
                        return result
                    case _:
                        # logger.debug(f"Function '{func.__name__}' executed successfully.")
                        return Ok[T](out=result)

            except Exception as e:
                error_message_logger = f"An error occurred in function '{func.__name__}'. Detail:\n{e}"
                logger.error(error_message_logger)

                error_message_debug = f"The function that triggered the error was '{func.__name__}', called with... \n\t\targs: '[ {args} ]\n\t\tkwargs: [ {kwargs} ]'"
                logger.debug(error_message_debug)

                error_message_return = f"An error occurred in function '{func.__name__}'. Detail: {e}"

                return Err(message=error_message_return, code=-1)

        return wrapper

    return decorator


def runwrap_soft[T](result: TResult[T]) -> T | Err:
    """
    Unwrap a Result.

    Parameters
    ----------
    result : Result[T]
        The Result to unwrap.

    Returns
    -------
    T
        The data inside the Result.

    Raises
    ------
    ValueError
        If the Result is an Err.
    """

    match result:
        case Ok(out=data):
            return data
        case Err(message=msg, code=code):
            return Err(message=msg, code=code)


def funwrap[T](func: Callable[..., TResult[T]]) -> Callable[..., T | Err]:
    """
    Wrap a function that returns a Result in a function that returns the data inside the Result.
    """

    def wrapper(*args: Any, **kwargs: Any) -> T | Err:
        result = func(*args, **kwargs)
        match result:
            case Ok(out=data):
                return data
            case Err(message=msg, code=code):
                return Err(message=msg, code=code)
            case _:
                raise ValueError(f"Function '{func.__name__}' returned an unknown Result type, with value '{result}'.")

    return wrapper


def main_try_except_wrapper[T](logger: Logger) -> Callable[[Callable[..., T]], Callable[..., TResult[T]]]:
    """
    Decorator that wraps a function in a try-except block, logging any errors that occur. The wrapped function will then always return a Ok[T] or Err as output.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., TResult[T]]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> TResult[T]:
            try:
                result = func(*args, **kwargs)

                match result:
                    case Err(message=msg, code=code):
                        return result
                    case Ok():
                        return result
                    case _:
                        return Ok(out=result)

            except Exception as e:
                error_message_logger = f"'{func.__name__}':\n{e}"
                logger.error(error_message_logger)

                error_message_return = f"'{func.__name__}': {e}"
                return Err(message=error_message_return, code=-1)

        return wrapper

    return decorator


def light_error_handler[T](debug: bool = False) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that wraps a function in a try-except block, and returns a better error message if an exception is raised.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)

            except Exception as e:
                if not debug:
                    error_message = f"An error occurred in function '{func.__name__}'. {e.__class__.__name__}: {e}"

                else:
                    error_message = f"An error occured in function '{func.__name__}', called with...\n\targs: [[ {args} ]]\n\tkwargs: [[ {kwargs} ]]\n\n{e.__class__.__name__}: {e}"

                raise Exception(error_message)

        return wrapper

    return decorator
