from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)

##CREAR bases de datos
app.config['SECRET_KEY'] = 'ale12345678ale'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bomberosvcp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


##CREAR TABLA EN LA BASE DE DATOS
with app.app_context():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(100), unique=True)
        password = db.Column(db.String(100))
        name = db.Column(db.String(1000))
        telefono = db.Column(db.String(15))
    #Line below only required once, when creating DB.
    db.create_all()

with app.app_context():
    class Cursantes(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        nombre = db.Column(db.String(100))
        apellido = db.Column(db.String(100))
        email = db.Column(db.String(100))
        empresa = db.Column(db.String(1000))
        telefono = db.Column(db.String(15))
    #Line below only required once, when creating DB.
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        hash_password = generate_password_hash(request.form.get("password"),
                                               method='pbkdf2:sha256',
                                               salt_length=6)
        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_password,
            telefono=request.form.get("telefono")
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("secrets"))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("usuario not found")
            return redirect(url_for('login'))

        elif not check_password_hash(user.password, password):
            flash("Contraseña incorrecta")
            return redirect(url_for('login'))
        else:

            login_user(user)
            return redirect(url_for("secrets"))
    return render_template("login.html")


@app.route('/unidades')
def unidades():
    return render_template("unidades.html")

@app.route('/secrets')
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/download/<filename>')
@login_required
def download(filename):
    return send_from_directory(directory="static", path=filename)


@app.route('/cursos', methods=["GET", "POST"])
def cursos():
    if request.method == "POST":

        nuevo_cursante = Cursantes(
            email=request.form.get("email"),
            nombre=request.form.get("name"),
            apellido=request.form.get("Last_name"),
            telefono=request.form.get("telefono"),
            empresa=request.form.get("empresa")
        )
        db.session.add(nuevo_cursante)
        db.session.commit()
        flash("Muchas Gracias por inscribirte en breve nos pondermos en contacto con usted")


        return redirect(url_for("cursos"))
    return render_template("cursos.html")


@app.route('/matafuegos')
def matafuegos():
    return render_template("matafuegos.html")


if __name__ == '__main__':
    app.run(debug=True)