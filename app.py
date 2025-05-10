from flask import Flask,render_template,request,session,redirect,url_for,flash,current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

#Creamos el objeto app e instanciamos la clase Flask
app = Flask(__name__)
app.secret_key='ModaClick'

# Configuración SQLALCHEMY
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/bd_laika'
db=SQLAlchemy(app)

# Configuración Flask-Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Gestión de carga de inicio de sesión
@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

# DEFINIMOS LOS MODELOS USANDO CLASES 

# Usuarios model
class Usuarios(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False,unique=True)
    password = db.Column(db.String(20), nullable=False)
    rol = db.Column(db.String(30), nullable=False)

# Sucursales model
class Sucursales(db.Model):
    __tablename__ = 'sucursales'
    nombre_sucursal = db.Column(db.String(15), primary_key=True)
    numero_sala = db.Column(db.String(7), primary_key=True)
    capacidad = db.Column(db.Integer)
# Categorias model
class Categorias(db.Model):
    __tablename__ = 'categorias'
    nombre_categoria = db.Column(db.String(20), primary_key=True)
    nombre_sucursal = db.Column(db.String(15))
    presupuesto = db.Column(db.Numeric(12,2))
# Productos model
class Productos(db.Model):
    __tablename__ = 'productos'
    id_producto = db.Column(db.String(30), primary_key=True)
    descripcion = db.Column(db.String(50))
    nombre_categoria = db.Column(db.String(20), db.ForeignKey('categorias.nombre_categoria'))
    precio = db.Column(db.Integer)
    categorias = db.relationship('Categorias', backref=db.backref('producto', lazy=True))
# Empleados model
class Empleados(db.Model):
    __tablename__ = 'empleados'
    id_empleado = db.Column(db.String(30), primary_key=True)
    nombre_empleado = db.Column(db.String(50), nullable=False)
    nombre_categoria = db.Column(db.String(20), db.ForeignKey('categorias.nombre_categoria'))
    salario = db.Column(db.Numeric(10,2))
    categorias = db.relationship('Categorias', backref=db.backref('empleado', lazy=True))
# Clientes model
class LineaProductos(db.Model):
    __tablename__ = 'lineaproductos'
    id_producto = db.Column(db.String(30), db.ForeignKey('productos.id_producto'), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    forma_pago = db.Column(db.String(20), primary_key=True) ##
    coleccion = db.Column(db.Integer, primary_key=True)
    nombre_sucursal = db.Column(db.String(15))
    numero_sala = db.Column(db.String(7))
    id_seccionhe = db.Column(db.String(4))
    productos = db.relationship('Productos', backref=db.backref('lineaproducto', lazy=True))
    sucursales = db.relationship('Sucursales', foreign_keys=[nombre_sucursal, numero_sala], 
                                primaryjoin="and_(LineaProductos.nombre_sucursal==Sucursales.nombre_sucursal, LineaProductos.numero_sala==Sucursales.numero_sala)")
# Ventas model
class Ventas(db.Model):
    __tablename__ = 'ventas'
    id_venta = db.Column(db.String(30), db.ForeignKey('empleados.id_empleado'), primary_key=True) #
    id_producto = db.Column(db.String(30), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    forma_pago = db.Column(db.String(20), primary_key=True) ##
    coleccion = db.Column(db.Integer, primary_key=True)
    empleados = db.relationship('Empleados', backref=db.backref('ventas', lazy=True)) ##
    lineaproductos = db.relationship('LineaProductos', foreign_keys=[id_producto, sec_id, forma_pago, coleccion], ##
                              primaryjoin="and_(Ventas.id_producto==LineaProductos.id_producto, Ventas.sec_id==LineaProductos.sec_id, Ventas.forma_pago==LineaProductos.forma_pago, Ventas.coleccion==LineaProductos.coleccion)")
# Clientes model
class Clientes(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.String(30), primary_key=True)
    nombre_cliente = db.Column(db.String(50), nullable=False)
    nombre_categoria = db.Column(db.String(20), db.ForeignKey('categorias.nombre_categoria'))
    estado = db.Column(db.Integer)
    categorias = db.relationship('Categorias', backref=db.backref('cliente', lazy=True))
# Pedidos model
class Pedidos(db.Model):
    __tablename__ = 'pedidos'
    id_cliente = db.Column(db.String(30), db.ForeignKey('clientes.id_cliente'), primary_key=True)
    id_producto = db.Column(db.String(30), primary_key=True)
    sec_id = db.Column(db.String(8), primary_key=True)
    forma_pago = db.Column(db.String(20), primary_key=True) ##
    coleccion = db.Column(db.Integer, primary_key=True)
    estado_pedido = db.Column(db.String(2))
    clientes = db.relationship('Clientes', backref=db.backref('pedidos', lazy=True))
    lineaproductos = db.relationship('LineaProductos', foreign_keys=[id_producto, sec_id, forma_pago, coleccion], ##
                              primaryjoin="and_(Pedidos.id_producto==LineaProductos.id_producto, Pedidos.sec_id==LineaProductos.sec_id, Pedidos.forma_pago==LineaProductos.forma_pago, Pedidos.coleccion==LineaProductos.coleccion)")
# Asesor model
class Asesor(db.Model):
    __tablename__ = 'asesor'
    idf_cliente = db.Column(db.String(30), db.ForeignKey('clientes.id_cliente'), primary_key=True)
    idf_empleado = db.Column(db.String(30), db.ForeignKey('empleados.id_empleado'))
    clientes = db.relationship('Clientes', backref=db.backref('asesor', uselist=False))
    empleados = db.relationship('Empleados', backref=db.backref('asesorias', lazy=True))
# Proveedores model
class Proveedores(db.Model):
    __tablename__ = 'proveedores'
    id_producto = db.Column(db.String(30), db.ForeignKey('productos.id_producto'), primary_key=True)
    id_proveedor = db.Column(db.String(30), db.ForeignKey('productos.id_producto'), primary_key=True)
    productos = db.relationship('Productos', foreign_keys=[id_producto], 
                             primaryjoin="Proveedores.id_producto==Productos.id_producto", 
                             backref=db.backref('proveedor', lazy=True))
    proveedor_producto = db.relationship('Productos', foreign_keys=[id_proveedor], 
                                    primaryjoin="Proveedores.id_proveedor==Productos.id_producto", 
                                    backref=db.backref('required_by', lazy=True))
# Seccion model
class SeccionHE(db.Model):
    __tablename__ = 'seccionhe'
    id_seccionhe = db.Column(db.String(4), primary_key=True)
    dia = db.Column(db.String(1), primary_key=True)
    inicio_he = db.Column(db.Time)
    fin_he = db.Column(db.Time)

####---------------------------------------------------------------------####
# Creamos las rutas para cada templates

# ruta por defecto para la pagina principal
@app.route('/')
def index():
    return render_template('index.html')

# ruta login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        rol = request.form['rol'].strip()

        usuarios = Usuarios.query.filter_by(email=email).first()

        if usuarios:
            if usuarios.password == password and usuarios.rol == rol:
                login_user(usuarios)
                flash('Ha iniciado sesión correctamente', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario, contraseña o rol incorrectos.', 'danger')
        else:
            flash('El usuario no existe.', 'danger')

    return render_template('login.html')

#ruta registro de nuevo usuario
@app.route('/registrar_usuario', methods=['GET', 'POST'])

def registrar_usuario():
    if request.method == "POST":
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        rol = request.form['rol'].strip()

        try:
            # Verificar si el usuario ya existe
            existe_usuario = Usuarios.query.filter_by(email=email).first()
            if existe_usuario:
                flash("El correo electrónico ya está registrado. Usa otro.", "danger")
                return redirect(url_for('registrar_usuario'))

            # Crear y guardar el nuevo usuario
            nuevo_usuario = Usuarios(email=email, password=password, rol=rol)
            db.session.add(nuevo_usuario)
            db.session.commit()

            flash("Usuario registrado con éxito!", "success")
            return redirect('/registrar_usuario')

        except SQLAlchemyError:
            db.session.rollback()  
            flash("Se produjo un error al registrar el usuario", "danger")

    return render_template('registro.html')


# ruta para el dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.rol == 'admin':
        return render_template('admin.html')
    elif current_user.rol == 'clientes':
        clientes = Clientes.query.filter_by(id_cliente=current_user.email).first()
        if clientes:
            courses_taken = Productos.query.all()  # Obtener todos los productos pero mantener el nombre courses_taken
            return render_template("clientes.html", clientes=clientes, courses_taken=courses_taken)
        else:
            return "Cliente not found", 404

# ruta para cierre de sesion
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cierre de sesión exitosamente!', 'info')

    return redirect(url_for('index'))

@app.route('/nosotros')
def  nosotros():
    return render_template("nosotros.html")  

@app.route('/tienda')
def  tienda():
    return render_template("categorias.html")  

@app.route('/admin')
@login_required
def  admin():
    return render_template("admin.html")

@app.route('/recuperacion', methods=['GET', 'POST'])
def recuperacion():
    if request.method == 'POST':
        email = request.form.get('email')
        
        if email:
            # Simular proceso de recuperación (enviar correo, generar token, etc.)
            flash('Se ha enviado un enlace de recuperación a tu correo.', 'success')
            return redirect(url_for('recuperacion'))  # Redirige a la misma página después de enviar
        
        flash('Por favor, ingresa un correo válido.', 'danger')
    
    return render_template('recuperacion.html')

@app.route('/clientes')
@login_required
def clientes():
    clientes = Clientes.query.filter_by(id_cliente=current_user.email).first()
    if clientes:
        courses_taken = Productos.query.all()  
        return render_template("clientes.html", clientes=clientes, courses_taken=courses_taken)
    else:
        return "Cliente no encontrado", 404

# RUTAS POR MODULO
    

@app.route('/lineaproducto')
@login_required
def  lineaproducto():
    lineaproducto = LineaProductos.query.order_by(LineaProductos.sec_id).all()
    sec = db.session.query(LineaProductos.sec_id).distinct().order_by(LineaProductos.sec_id).all()
    sec = [s[0] for s in sec]  
    return render_template("lineaproducto.html", lineaproducto=lineaproducto, sec=sec)


@app.route('/nueva_lineaproducto', methods=['GET', 'POST'])
@login_required
def nueva_lineaproducto():

    productos = Productos.query.distinct(Productos.id_producto).all()
    nombre_sucursal = db.session.query(Sucursales.nombre_sucursal).distinct().all()
    sala = db.session.query(Sucursales.numero_sala).distinct().all()

    if request.method == "POST":
        id=request.form['id']
        productos = request.form['productos']
        forma_pago = request.form['forma_pago']
        coleccion = request.form['coleccion']
        nombre_sucursal = request.form['nombre_sucursal']
        sala = request.form['sala']
        horario = request.form['horario']

        try:                                                           ##
            new_sec = LineaProductos(id_producto=productos,sec_id=id,forma_pago=forma_pago,coleccion=coleccion,nombre_sucursal=nombre_sucursal,numero_sala=sala,id_seccionhe=horario)
            db.session.add(new_sec)
            db.session.commit()
            flash("Adicción de linea de producto exitosa!", "success")
            return redirect('/lineaproducto')
        except SQLAlchemyError as e:
            db.session.rollback()  
            flash("Ocurrio un error mientra añadia", "danger")
            

    return render_template('nueva_lineaproducto.html', productos=productos,nombre_sucursal=nombre_sucursal,sala=sala)




@app.route('/nuevo_producto', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    categorias = Categorias.query.distinct(Categorias.nombre_categoria).all()  # Fetch categorias

    if request.method == 'POST':
        id_producto = request.form['id_producto']
        descripcion = request.form['descripcion']
        nombre_categoria = request.form['nombre_categoria']
        precio = request.form['precio']

        try:
            existe_producto = Productos.query.filter_by(id_producto=id_producto).first()
            if existe_producto:
                flash("El ID del producto ya existe. Elija uno diferente..", "danger")
                return redirect(url_for('nuevo_producto'))

            crea_producto = Productos(id_producto=id_producto, descripcion=descripcion, nombre_categoria=nombre_categoria, precio=precio)
            db.session.add(crea_producto)
            db.session.commit()
            flash("Producto añadido con éxito!", "success")
            return redirect(url_for('categorias'))

        except Exception as e:
            db.session.rollback()
            flash("Se produjo un error al agregar el producto: " + str(e), "danger")
            return redirect(url_for('nuevo_producto'))  # Redireccionar de nuevo a la página de agregar producto con el parámetro nombre_categoria

    return render_template('nuevo_producto.html', categorias=categorias)

@app.route('/categorias')
@login_required
def  categorias():
    return render_template("categorias.html")

@app.route('/sucursal')
@login_required
def  sucursal():
    sucursal=Sucursales.query.all()

    return render_template("sucursal.html",sucursal=sucursal)


@app.route('/empleado')
@login_required
def  empleado():
    empleado=Empleados.query.all()
    return render_template('empleado.html', empleado = empleado)


@app.route('/actualizar_empleado/<string:id_empleado>', methods=['GET', 'POST'])
@login_required
def actualizar_empleado(id_empleado):
    empleados = Empleados.query.get(id_empleado)
    nombre_categoria = Categorias.query.distinct(Categorias.nombre_categoria).all()

    if request.method == "POST":
        empleados.nombre_empleado = request.form['nombre_empleado']
        empleados.nombre_categoria = request.form['nombre_categoria']
        empleados.salario = request.form['salario']
        try:
            db.session.commit()
            flash("¡Perfil actualizado exitosamente!", "success")
            return redirect('/empleado')
        except SQLAlchemyError as e:
            db.session.rollback()  
            flash("Se produjo un error durante la actualización", "danger")

    return render_template('actualizar_empleado.html', empleados=empleados, categorias=nombre_categoria)



@app.route('/nuevo_empleado', methods=['GET', 'POST'])
@login_required
def nuevo_empleado():

    nombre_categoria = Categorias.query.distinct(Categorias.nombre_categoria).all()

    if request.method == "POST":
        id_empleado=request.form['id_empleado']
        nombre_empleado = request.form['nombre_empleado']
        nombre_categoria = request.form['nombre_categoria']
        salario = request.form['salario'] 

        try:
            existe_producto = Empleados.query.filter_by(id_empleado=id_empleado).first()
            if existe_producto:
                flash("El ID del empleado ya existe. Elija uno diferente.", "danger")
                return redirect(url_for('nuevo_empleado'))
            
            crea_empleado = Empleados(id_empleado=id_empleado, nombre_empleado=nombre_empleado, nombre_categoria=nombre_categoria, salario=salario) #empleado
            db.session.add(crea_empleado)
            db.session.commit()
            flash("Empleado añadido con éxito!", "success")
            return redirect('/empleado')
        except SQLAlchemyError as e:
            db.session.rollback()  
            flash("Se produjo un error al agregar", "danger")
            

    return render_template('nuevo_empleado.html', categorias=nombre_categoria)


@app.route('/eliminar_empleado/<string:id_empleado>', methods=['GET', 'POST'])
@login_required
def eliminar_empleado(id_empleado):
    empleados = Empleados.query.get(id_empleado)

    if empleados:
        db.session.delete(empleados)
        db.session.commit()
        flash("Empleado eliminado !", "warning")
        return redirect('/empleado')

    return redirect('/empleados')


"""______________________________Clientes___________________________"""
@app.route('/cliente')
@login_required
def  cliente():
    clientes=Clientes.query.all()
    return render_template("cliente.html", clientes = clientes)


@app.route('/actualizar_cliente/<string:id_cliente>', methods=['GET', 'POST'])
@login_required
def actualizar_cliente(id_cliente):
    clientes=Clientes.query.get(id_cliente)
    nombre_categoria = Categorias.query.distinct(Categorias.nombre_categoria).all()

    if request.method == "POST":
        clientes.nombre_cliente = request.form['nombre_cliente']
        clientes.nombre_categoria = request.form['nombre_categoria']
        clientes.estado = request.form['estado'] #---
        try:
            db.session.commit()
            flash("Perfil actualizado exitosamente!", "success")
            return redirect('/cliente')
        except SQLAlchemyError as e:
            db.session.rollback()  
            flash("Se produjo un error durante la actualización", "danger")

    return render_template('actualizar_cliente.html',clientes=clientes, categorias=nombre_categoria)


@app.route('/nuevo_cliente', methods=['GET', 'POST'])
@login_required
def nuevo_cliente():

    nombre_categoria = Categorias.query.distinct(Categorias.nombre_categoria).all()

    if request.method == "POST":
        id = request.form['id']
        nombre_cliente = request.form['nombre_cliente']
        nombre_categoria = request.form['nombre_categoria']

        try:
            existe_producto = Clientes.query.filter_by(id_cliente=id).first()
            if existe_producto:
                flash("El ID del empleado ya existe. Elija uno diferente.", "danger")
                return redirect(url_for('nuevo_cliente'))
            
            estado = request.form['estado']  # Esto obtiene "Activo" o "Inactivo" del formulario
            crea_cliente = Clientes(id_cliente=id, nombre_cliente=nombre_cliente, nombre_categoria=nombre_categoria, estado=estado) #---
            new_user=Usuarios(email=id,password=id,rol="clientes")
            db.session.add(crea_cliente)
            db.session.add(new_user)
            db.session.commit()
            flash("Cliente agregada con éxito!", "success")
            return redirect('/cliente')
        except SQLAlchemyError as e:
            db.session.rollback()  
            flash("Se produjo un error al agregar", "danger")
            

    return render_template('nuevo_cliente.html', categorias=nombre_categoria)


@app.route('/eliminar_cliente/<string:id_cliente>', methods=['GET', 'POST'])
@login_required
def eliminar_cliente(id_cliente):
    clientes = Clientes.query.get(id_cliente)
    usuarios = Usuarios.query.filter_by(email=id_cliente).first() 
    if clientes:
        db.session.delete(clientes)
        db.session.delete(usuarios)
        db.session.commit()
        flash("Cliente eliminado !", "warning")
        return redirect('/cliente')

    return redirect('/cliente')



##RUTAS POR CATEGORIA

# ruta Perros
@app.route('/perros')
def perros():
    query1 = text(""" 
        SELECT clientes.id_cliente, clientes.nombre_cliente
        FROM clientes
        WHERE clientes.nombre_categoria = 'Perros'
    """)
    query2 = text(""" 
        SELECT productos.id_producto, productos.descripcion, productos.precio
        FROM productos
        WHERE productos.nombre_categoria = 'Perros'
    """)
    query3 = text(""" 
        SELECT empleados.id_empleado, empleados.nombre_empleado
        FROM empleados
        WHERE empleados.nombre_categoria = 'Perros'
    """)
    nombre_categoria = Categorias.query.distinct(Categorias.nombre_categoria).all()

    try:
        cliente = db.session.execute(query1).fetchall()
        producto = db.session.execute(query2).fetchall()
        empleado = db.session.execute(query3).fetchall()

    except Exception as e:
        cliente = []  
        producto = []  
        empleado = []
        flash("Se produjo un error al obtener los datos", "danger")
   
    return render_template("perros.html", cliente=cliente, producto=producto, empleado=empleado, nombre_categoria=nombre_categoria)



# ruta Juguetes
@app.route('/juguetes')
def  ropa_interior():

    query1 = text("""
        SELECT clientes.id_cliente, clientes.nombre_cliente
        FROM clientes
        WHERE clientes.nombre_categoria = 'juguetes'
    """)
    query2 = text("""
        SELECT productos.id_producto, productos.descripcion, productos.precio
        FROM productos
        WHERE productos.nombre_categoria = 'juguetes'
    """)
    query3 = text("""
        SELECT empleados.id_empleado, empleados.nombre_empleado
        FROM empleados
        WHERE empleados.nombre_categoria = 'juguetes'
    """)

    try:
        cliente = db.session.execute(query1).fetchall()
        producto = db.session.execute(query2).fetchall()
        empleado = db.session.execute(query3).fetchall()

    except Exception as e:
        
        flash("Se produjo un error al obtener los datos", "danger")
        cliente = []  
        producto = []  
        empleado = []
    return render_template("juguetes.html", cliente=cliente, producto=producto, empleado=empleado)

# ruta Gatos
@app.route('/gatos')
def  jeans():
    query1 = text("""
        SELECT clientes.id_cliente, clientes.nombre_cliente
        FROM clientes
        WHERE clientes.nombre_categoria = 'gatos'
    """)
    query2 = text("""
        SELECT productos.id_producto, productos.descripcion, productos.precio
        FROM productos
        WHERE productos.nombre_categoria = 'gatos'
    """)
    query3 = text("""
        SELECT empleados.id_empleado, empleados.nombre_empleado
        FROM empleados
        WHERE empleados.nombre_categoria = 'gatos'
    """)

    try:
        cliente = db.session.execute(query1).fetchall()
        producto = db.session.execute(query2).fetchall()
        empleado = db.session.execute(query3).fetchall()

    except Exception as e:
        flash("Se produjo un error al obtener los datos", "danger")
        cliente = []  
        producto = []  
        empleado = []
    return render_template("gatos.html", cliente=cliente, producto=producto, empleado=empleado)

# ruta Accesorios
@app.route('/accesorios')
def  accesorios():
    query1 = text("""
        SELECT clientes.id_cliente, clientes.nombre_cliente
        FROM clientes
        WHERE clientes.nombre_categoria = 'Accesorios'
    """)
    query2 = text("""
        SELECT productos.id_producto, productos.descripcion, productos.precio
        FROM productos
        WHERE productos.nombre_categoria = 'Accesorios'
    """)
    query3 = text("""
        SELECT empleados.id_empleado, empleados.nombre_empleado
        FROM empleados
        WHERE empleados.nombre_categoria = 'Accesorios'
    """)

    try:
        cliente = db.session.execute(query1).fetchall()
        producto = db.session.execute(query2).fetchall()
        empleado = db.session.execute(query3).fetchall()

        print(cliente)
    except Exception as e:
        
        flash("Se produjo un error al obtener los datos", "danger")
        cliente = []  
        producto = []  
        empleado = [] 
    return render_template("accesorios.html", cliente=cliente, producto=producto, empleado=empleado)

# ruta Snacks
@app.route('/snacks')
def  camisas():
    query1 = text("""
        SELECT clientes.id_cliente, clientes.nombre_cliente
        FROM clientes
        WHERE clientes.nombre_categoria = 'snacks'
    """)
    query2 = text("""
        SELECT productos.id_producto, productos.descripcion, productos.precio
        FROM productos
        WHERE productos.nombre_categoria = 'snacks'
    """)
    query3 = text("""
        SELECT empleados.id_empleado, empleados.nombre_empleado
        FROM empleados
        WHERE empleados.nombre_categoria = 'snacks'
    """)

    try:
        cliente = db.session.execute(query1).fetchall()
        producto = db.session.execute(query2).fetchall()
        empleado = db.session.execute(query3).fetchall()

        print(cliente)
    except Exception as e:
        
        flash("Se produjo un error al obtener los datos", "danger")
        cliente = []  
        producto = []  
        empleado = []
    return render_template("snacks.html", cliente=cliente, producto=producto, empleado=empleado)


# Ejecutando el objeto Flask
if __name__ == '__main__':
    app.run(debug=True, port=5600)   