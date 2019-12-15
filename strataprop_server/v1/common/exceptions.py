from flask_restful import HTTPException

class UnKnownException(Exception):
    pass

class BadRequest(HTTPException):
    pass
class ServerConfigurationError(HTTPException):
    pass

class RequiredParametersMissingException(HTTPException):
    pass

class DuplicateEntry(HTTPException):
	pass

class EmployeeBasicInfoNotFoundException(HTTPException):
	pass

class InvalidEmployeeNameException(HTTPException):
	pass

class InvalidMobileNumber(HTTPException):
	pass

class InvalidEmail(HTTPException):
	pass

class EmployeeNotFound(HTTPException):
	pass

class DeviceNotFound(HTTPException):
	pass
class InvalidDeviceNameException(HTTPException):
	pass

