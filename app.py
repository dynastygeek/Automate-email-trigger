from flask import Flask, render_template, request, jsonify
import win32com.client as win32
import pythoncom
import webbrowser
import json
from threading import Timer
import os

app = Flask(__name__)

JSON_FILE_PATH = "employee_data.json"

if not os.path.exists(JSON_FILE_PATH):
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump([], f)

def save_to_json(data):
    with open(JSON_FILE_PATH, 'r') as f:
        existing_data = json.load(f)
    existing_data.append(data)
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(existing_data, f, indent=4)

@app.route("/")
def onboarding():
    return render_template('table.html')

@app.route("/submit-Onboarding", methods=["POST"])
def submit():
    data = {
        "firstname": request.form["firstname"],
        "lastname": request.form["lastname"],
        "email": request.form["email"],
        "department": request.form["department"],
        "phonenumber": request.form["phonenumber"],
        "position": request.form["position"],
        "doj": request.form["doj"],
        "address": f"{request.form['address1']}, {request.form['address2']}",
        "pincode": request.form["pincode"],
        "equipment": request.form["equipment"],
    }

    save_to_json(data)

    send_email(data["email"],data["firstname"],data["position"],data["department"],data["doj"])
    return jsonify({"message": "successfully saved"}), 200

def send_email(recipient_email,firstname,position,department,doj):
    try:
        pythoncom.CoInitialize()  # Initialize COM
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = 'Welcome to the Company!'
        mail.Body = (
            f"Dear {firstname},\n\n"
            f"Welcome to the company! We are excited to have you join as a {position} "
            f"in the department of {department} at CYIENT LIMITED"
            f"The Date of Joining for you will be {doj}\n\n\n"
            f"Best Regards,\nCyient HR"
        )
        mail.To = recipient_email
        mail.Send()
        print(f"Email sent to {recipient_email} successfully.")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        pythoncom.CoUninitialize()

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, open_browser).start()
    # app.run(use_reloader=False)
    app.run(debug=True)