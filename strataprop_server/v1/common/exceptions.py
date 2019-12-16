from flask_restful import HTTPException

class BadRequest(HTTPException):
    pass

class DuplicateEntry(HTTPException):
	pass

class DeviceNotFound(HTTPException):
	pass
	
class InvalidDeviceNameException(HTTPException):
	pass

class BadRequest(HTTPException):
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

class DeviceNotFree(HTTPException):
	pass
