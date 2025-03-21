from flask import jsonify

def get_status_category(status_code):
    """Returns a general status category based on the HTTP status code range."""
    if 100 <= status_code < 200:
        return "Informational"
    elif 200 <= status_code < 300:
        return "Success"
    elif 300 <= status_code < 400:
        return "Redirection"
    elif 400 <= status_code < 500:
        return "Client Error"
    elif 500 <= status_code < 600:
        return "Server Error"
    return "Unknown Status"


def generate_response(status_code : int = 200, 
                      trace_id : str = None, 
                      message : str = None, 
                      **kwargs):
    """
    Generates a structured HTTP response with an optional trace ID and additional data.

    Args:
    trace_id (str, optional): A unique identifier for tracing requests.
    status_code (int, optional): HTTP status code of the response. Default is 200.
    message (str, optional): Custom message to include in the response.
    **kwargs: Any additional key-value pairs to include in the response body.

    Returns:
        Dict: A JSON response with the status category, message, and additional fields.

    Example:
        ```python
        response = generate_response(
            trace_id="abc123",
            status_code=404,
            message="Resource not found",
            user="John Doe"
        )
        ```
        Expected JSON output:
        ```json
        {
            "status": "Client Error",
            "message": "Resource not found",
            "user": "John Doe"
        }
        ```
    """
    response_body = {
        "status": get_status_category(status_code)
    }

    # Include message only if provided
    if message:
        response_body["message"] = message

    # Add any additional user-provided parameters to the response body
    response_body.update(kwargs)

    response = jsonify(response_body)
    response.status_code = status_code

    if trace_id:
        # Attach trace ID to response headers
        response.headers["X-Trace-ID"] = trace_id

    return response
