from functools import wraps


def validate(pipe_func):
    """"
    description:
    take pipe_func for validate and return validated data or throw error

    :param pipe_func: func for validate

    :return: --> func decorator
    """

    def decorator(wrapped_func):
        """"
        description:
        decorator func which take wrapped_func and return wrapped func

        :param wrapped_func: main func who wrap our decorator

        :return: --> func wrapper
        """

        @wraps(wrapped_func)
        def wrapper(*args, **kwargs):
            """"
            description:
            wrapper func who has been return instead of wrapped func,
            got validated data or error from validate pipe func, and transmits to wrapped_func func
            after return the response

            :param args: all position arguments from wrapped func
            :param kwargs: all keyword arguments from wrapped func

            :return: --> response from wrapped_func
            """

            validated_data = pipe_func(*args, **kwargs)
            response = wrapped_func(**validated_data)

            return response

        return wrapper

    return decorator
