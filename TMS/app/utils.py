
def format_response(success=True, message="", data=None, error_code=None, error_message=None, error_fields=None):
    return {
        "Success": success,
        "Message": message,
        "Error": {
            "code": error_code or "",
            "message": error_message or "",
            "fields": error_fields or []
        },
        "Data": data
    }
