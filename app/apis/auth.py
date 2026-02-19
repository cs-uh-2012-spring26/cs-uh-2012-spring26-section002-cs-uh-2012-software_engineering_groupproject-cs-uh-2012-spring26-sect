from flask_restx import Namespace, Resource, fields
from app.apis import MSG
from app.db.users import UserResource
from app.db.users import USERNAME, EMAIL, PASSWORD_HASH, PHONE, ROLE
from http import HTTPStatus
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token


api = Namespace("auth", description="Authentication endpoints")

_EXAMPLE_USER_1 = {
    USERNAME: "Jane Doe",
    EMAIL: "jane.doe@software.io",
    "password": "janedoe12345",
    PHONE: "+971500000000",
}

_EXAMPLE_USER_2 = {
    USERNAME: "John Doe",
    EMAIL: "john.doe@software.io",
    "password": "johndoe54321",
    PHONE: "+971500000001",
}

REGISTER_USER = api.model(
    "Register",
    {
        USERNAME: fields.String(required=True, example=_EXAMPLE_USER_1[USERNAME]),
        EMAIL: fields.String(required=True, example=_EXAMPLE_USER_1[EMAIL]),
        "password": fields.String(required=True, example=_EXAMPLE_USER_1["password"],
        PHONE: fields.String(required=True, example=_EXAMPLE_USER_1[PHONE]),
    },
)

LOGIN_USER = api.model(
    "Login",
    {
        USERNAME: fields.String(required=True, example=_EXAMPLE_USER_1[USERNAME]),
        "password": fields.String(required=True, example=_EXAMPLE_USER_1["password"]),
    },
)

TOKEN_MODEL = api.model(
    "TokenResponse",
    {
        "access_token": fields.String(example="JWT_TOKEN_HERE"),
    },
)

@api.route("/register")
class Register(Resource):
    @api.expect(REGISTER_MODEL, validate=True)
    @api.response(HTTPStatus.CREATED, "User registered")
    @api.response(HTTPStatus.BAD_REQUEST, "Username or email already exists")
    def post(self):
        username = request.json.get(USERNAME)
        email = request.json.get(EMAIL)
        password = request.json.get("password")
        phone = request.json.get(PHONE)
        user_res = UserResource()
        if user_res.get_by_username(username) or user_res.get_by_email(email):
            return {MSG: "Username or email already exists"}, HTTPStatus.BAD_REQUEST
        password_hash = generate_password_hash(password)
        user_id = user_res.create_user(username, email, password_hash, phone, role="member")

        return {MSG: f"User created with id: {user_id}"}, HTTPStatus.CREATED

@api.route("/login")
class Login(Resource):
    @api.expect(LOGIN_MODEL, validate=True)
    @api.response(HTTPStatus.OK, "Login successful", TOKEN_MODEL)
    @api.response(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
    def post(self):
        username = request.json.get(USERNAME)
        password = request.json.get("password")

        user_res = UserResource()
        user = user_res.get_by_username(username)
        if user is None:
            return {MSG: "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

        if not check_password_hash(user[PASSWORD_HASH], password):
            return {MSG: "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

        access_token = create_access_token(identity=str(user["_id"]))
        return {"access_token": access_token}, HTTPStatus.OK
#    @api.doc(
#        params={
#            "name": "Filter student list by student name (partial matches allowed)",
#            "seniority": "Filter student list by student seniority (Exact seniority match)",
#        }
#    )
#    @api.response(
#        HTTPStatus.OK,
#        "Success",
#        api.model(
#            "All Students",
#            {
#                MSG: fields.List(
#                    fields.Nested(STUDENT_CREATE_FLDS),
#                    example=[_EXAMPLE_STUDENT_1, _EXAMPLE_STUDENT_2],
#                )
#            },
#        ),
#    )
#    def get(self):
#        name = request.args.get("name")
#        seniority = request.args.get("seniority")
#        student_resource = StudentResource()
#        student_list = student_resource.get_students(name, seniority)
#        return {MSG: student_list}, HTTPStatus.OK

#    @api.expect(STUDENT_CREATE_FLDS)
#    @api.response(
#        HTTPStatus.OK,
#        "Success",
#        api.model(
#            "Create Student",
#            {MSG: fields.String("Student created with id: XXXXXXXXXXXXXXXXXXXXXXXX")},
#        ),
#    )
#    @api.response(
#        HTTPStatus.NOT_ACCEPTABLE,
#        "Invalid Request",
#        api.model(
#            "Create Student: Bad Request",
#            {MSG: fields.String("Invalid value provided for one of the fields")},
#        ),
#    )
#    def post(self):
#        assert isinstance(request.json, dict)
#        name = request.json.get(NAME)
#        email = request.json.get(EMAIL)
#        seniority = request.json.get(SENIORITY)
#        if not (
#            isinstance(name, str)
#            and len(name) > 0
#            and isinstance(email, str)
#            and len(email) > 0
#            and isinstance(seniority, str)
#            and seniority.lower() in ["first-year", "sophomore", "junior", "senior"]
#        ):
#            return {
#                MSG: "Invalid value provided for one of the fields"
#            }, HTTPStatus.NOT_ACCEPTABLE
#        student_resource = StudentResource()
#        student_id = student_resource.create_student(name, email, seniority)
#        return {MSG: f"Student created with id: {student_id}"}, HTTPStatus.OK
#
#
#@api.route("/<email>")
#@api.param("email", "Student email to use for lookup")
#@api.response(
#    HTTPStatus.NOT_FOUND,
#    "Student Not Found",
#    api.model("Student: Not Found", {MSG: fields.String("Student not found")}),
#)
#class Student(Resource):
#    @api.doc("Get a specific student, identified by email")
#    @api.response(HTTPStatus.OK, "Success", STUDENT_CREATE_FLDS)
#    def get(self, email):
#        student_resource = StudentResource()
#        student = student_resource.get_student_by_email(email)
#
#        if student is None:
#            return {MSG: "Student not found"}, HTTPStatus.NOT_FOUND
#
#        return {MSG: student}, HTTPStatus.OK
#
#    @api.expect(STUDENT_CREATE_FLDS)
#    @api.doc("Update a specific student, identified by email")
#    @api.response(
#        HTTPStatus.OK,
#        "Success",
#        api.model("Update Student", {MSG: fields.String("Student updated")}),
#    )
#    @api.response(
#        HTTPStatus.NOT_ACCEPTABLE,
#        "Student Update Information Not Acceptable",
#        api.model(
#            "Update Student: Not Acceptable",
#            {MSG: fields.String("Invalid value provided for one of the fields")},
#        ),
#    )
#    def put(self, email):
#        assert isinstance(request.json, dict)
#        name = request.json.get(NAME)
#        seniority = request.json.get(SENIORITY)
#        new_email = request.json.get(EMAIL)
#        if not (
#            isinstance(name, str)
#            and len(name) > 0
#            and isinstance(new_email, str)
#            and len(new_email) > 0
#            and isinstance(seniority, str)
#            and seniority.lower() in ["first-year", "sophomore", "junior", "senior"]
#        ):
#            return {
#                MSG: "Invalid value provided for one of the fields"
#            }, HTTPStatus.NOT_ACCEPTABLE
#
#        student_resource = StudentResource()
#        updated_student = student_resource.update_student(
#            email, name, new_email, seniority
#        )
#
#        if updated_student is None:
#            return {MSG: "Student not found"}, HTTPStatus.NOT_FOUND
#
#        return {MSG: "Student updated"}, HTTPStatus.OK
