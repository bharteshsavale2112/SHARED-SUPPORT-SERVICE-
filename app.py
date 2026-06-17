from flask import Flask, request, jsonify
111111111111111111111from flask_cors import CORS
import openpyxl
import os

app = Flask(__name__)
CORS(app)

# ==========================
# CONFIG
# ==========================

ADMIN_EMAIL = "admin@bajajauto.com"
ADMIN_PASSWORD = "Admin@123"

EXCEL_FILE = "bus_pass_requests.xlsx"

# ==========================
# CREATE EXCEL
# ==========================

if not os.path.exists(EXCEL_FILE):

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.title = "Bus Pass Requests"

    ws.append([
        "Employee Code",
        "Employee Name",
        "Department",
        "Mobile",
        "Shift",
        "Gender",
        "Route Number",
        "Pickup Location",
        "Drop Location",
        "Address"
    ])

    wb.save(EXCEL_FILE)

# ==========================
# LIVE BUS DATA
# ==========================

live_bus_data = {
    "route1": {
        "lat": 18.7506,
        "lng": 73.8772
    },
    "route2": {
        "lat": 18.6500,
        "lng": 73.8000
    }
}

# ==========================
# HOME
# ==========================

@app.route("/")
def home():
    return "Bajaj Auto Transport Backend Running"

# ==========================
# BUS PASS FORM
# ==========================

@app.route("/bus-pass", methods=["POST"])
def bus_pass():

    employeeCode = request.form.get("employeeCode")
    employeeName = request.form.get("employeeName")
    department = request.form.get("department")
    mobile = request.form.get("mobile")
    shift = request.form.get("shift")
    gender = request.form.get("gender")
    routeNumber = request.form.get("routeNumber")
    pickupLocation = request.form.get("pickupLocation")
    dropLocation = request.form.get("dropLocation")
    address = request.form.get("address")

    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb.active

    ws.append([
        employeeCode,
        employeeName,
        department,
        mobile,
        shift,
        gender,
        routeNumber,
        pickupLocation,
        dropLocation,
        address
    ])

    wb.save(EXCEL_FILE)

    return """
    <script>
    alert('Bus Pass Request Submitted Successfully');
    window.location.href='http://127.0.0.1:5500/buspass.html';
    </script>
    """

# ==========================
# ADMIN LOGIN
# ==========================

@app.route("/admin-login", methods=["POST"])
def admin_login():

    email = request.form.get("email")
    password = request.form.get("password")

    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:

        return """
        <script>
        alert('Login Successful');
        window.location.href='http://127.0.0.1:5500/index.html';
        </script>
        """

    return """
    <script>
    alert('Invalid Email Or Password');
    history.back();
    </script>
    """

# ==========================
# ADMIN FORGOT PASSWORD
# ==========================

@app.route("/admin-forgot-password", methods=["POST"])
def admin_forgot_password():

    email = request.form.get("email")

    if email.lower() == ADMIN_EMAIL.lower():

        return f"""
        <script>
        alert('Registered Email Found');
        alert('Current Password : {ADMIN_PASSWORD}');
        window.location.href='http://127.0.0.1:5500/adminlogin.html';
        </script>
        """

    return """
    <script>
    alert('Email Not Found');
    history.back();
    </script>
    """

# ==========================
# UPDATE BUS LOCATION
# ==========================

@app.route("/update-location", methods=["POST"])
def update_location():

    route_id = request.form.get("routeId")
    lat = request.form.get("lat")
    lng = request.form.get("lng")

    if route_id:

        live_bus_data[route_id] = {
            "lat": float(lat),
            "lng": float(lng)
        }

        return jsonify({
            "status": "success"
        })

    return jsonify({
        "status": "failed"
    })

# ==========================
# GET BUS LOCATION
# ==========================

@app.route("/get-location/<route_id>")
def get_location(route_id):

    if route_id in live_bus_data:
        return jsonify(live_bus_data[route_id])

    return jsonify({
        "lat": 18.7506,
        "lng": 73.8772
    })

# ==========================
# RUN APP
# ==========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )