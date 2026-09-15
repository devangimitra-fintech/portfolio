from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)

#secret key
app.secret_key = "my_portfolio_secret_key"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "51103"

#create database
def create_database():
    conn = sqlite3.connect("contact.db")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            subject TEXT,
            message TEXT NOT NULL
        )
    """)

    conn.close()

#home page
@app.route("/")
def home():
    return render_template("index.html")


#contact form
@app.route("/contact", methods=["POST"])
def contact():

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    subject = request.form["subject"]
    message = request.form["message"]

    conn = sqlite3.connect("contact.db")

    conn.execute("""
        INSERT INTO contacts
        (name, email, phone, subject, message)
        VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, subject, message))

    conn.commit()
    conn.close()

    return """
    <script>
        alert("Message sent successfully!");
        window.location.href = "/#contact";
    </script>
    """



#admin login
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

            session["admin_logged_in"] = True

            return redirect(url_for("messages"))

        else:

            return render_template(
                "login.html",
                error="Invalid username or password"
            )

    return render_template("login.html")

# messages
@app.route("/messages")
def messages():

    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    conn = sqlite3.connect("contact.db")
    conn.row_factory = sqlite3.Row

    messages = conn.execute(
        "SELECT * FROM contacts ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return render_template("messages.html", messages=messages)


# logout
@app.route("/logout")
def logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("login"))

#run application
if __name__ == "__main__":
    create_database()
    app.run(debug=True)