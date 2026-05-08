from decimal import Decimal

from botocore.exceptions import ClientError


def decode_error(err: ClientError):
    """Decode a client error message from AWS

    Args:
        err: The ClientError to parse out the error code and message if they are
        available.

    Returns:
        A tuple (code, message) where code is a string containing the error
        code, and message is a string containing the entire error message.
    """
    code, message = "Unknown", "Unknown"
    if "Error" in err.response:
        error = err.response["Error"]
        if "Code" in error:
            code = error["Code"]
        if "Message" in error:
            message = error["Message"]
    return code, message


def bad_param_response(bad_params):
    """Gets a response data object and status code when bad params are given.

    :return: A tuple contains a response data object and an HTTP 400 status
             code.
    """
    return (
        {
            "message": (
                f"Missing or invalid required query string parameters: "
                f"{bad_params}"
            )
        },
        400,
    )


def json_serialize_the_unserializable(val):
    """Serialize a value (e.g. Decimal) that is otherwise not json serializable.

    Right now this just handles Decimal, but can be updated as needed.

    The json library cannot serialize Decimal values, and floating point values
    coming back from dynamo are Decimal. So this shims them to floats.

    :param val: The value to serialize.
    :return: the serialized value.
    :raises: TypeError if even this function cannot serialize.
    """
    if isinstance(val, Decimal):
        # this results in a reduction of precision which can cause issues. In
        # our case (for now at least) it's ok, but we may want to consider other
        # mechanisms like string conversions or forcing some rounding.
        return float(val)
    raise TypeError(f"Value {val} of type {type(val)} is not json serializable")
