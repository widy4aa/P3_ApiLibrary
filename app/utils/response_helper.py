"""
Utility helper untuk format response API
"""


def success_response(data=None, message='Success', status_code=200):
    """
    Format response sukses
    
    Args:
        data: Data yang akan dikembalikan
        message: Pesan sukses
        status_code: HTTP status code
    
    Returns:
        tuple: (response dict, status code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
    
    return response, status_code


def error_response(message='Error', errors=None, status_code=400):
    """
    Format response error
    
    Args:
        message: Pesan error
        errors: Dictionary error per field
        status_code: HTTP status code
    
    Returns:
        tuple: (response dict, status code)
    """
    response = {
        'success': False,
        'message': message
    }
    
    if errors:
        response['errors'] = errors
    
    return response, status_code


def not_found_response(resource='Resource'):
    """
    Format response 404 Not Found
    
    Args:
        resource: Nama resource yang tidak ditemukan
    
    Returns:
        tuple: (response dict, 404)
    """
    return error_response(
        message=f'{resource} tidak ditemukan',
        status_code=404
    )


def validation_error_response(errors):
    """
    Format response validation error
    
    Args:
        errors: Dictionary error per field
    
    Returns:
        tuple: (response dict, 400)
    """
    return error_response(
        message='Validasi gagal',
        errors=errors,
        status_code=400
    )


def server_error_response(message='Internal server error'):
    """
    Format response server error
    
    Args:
        message: Pesan error
    
    Returns:
        tuple: (response dict, 500)
    """
    return error_response(
        message=message,
        status_code=500
    )
