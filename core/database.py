import sqlite3
import logging
from utils.config import DB_PATH  # ✅ Usa configuración centralizada

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def conectar_db():
    """Establece una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        logging.error(f"❌ Error al conectar con la base de datos: {e}")
        return None

def inicializar_db():
    """Crea la tabla de usuarios si no existe."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    rol TEXT NOT NULL
                )
            ''')
            conn.commit()
            logging.info("✅ Base de datos inicializada correctamente.")
        except sqlite3.Error as e:
            logging.error(f"❌ Error al inicializar la base de datos: {e}")
        finally:
            conn.close()

def agregar_usuario(username, password, email, dni, rol):
    """Agrega un usuario a la base de datos con email y DNI."""  
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (username, password, email, dni, rol) VALUES (?, ?, ?, ?, ?)",
                           (username, password, email, dni, rol))
            conn.commit()
            logging.info(f"✅ Usuario registrado: {username}")
            return True
        except sqlite3.IntegrityError:
            logging.warning(f"⚠️ Error: El usuario '{username}', email '{email}' o DNI '{dni}' ya existen.")
            return False
        except sqlite3.Error as e:
            logging.error(f"❌ Error al agregar usuario: {e}")
            return False
        finally:
            conn.close()

def obtener_usuario_por_email(email):
    """Obtiene un usuario por su correo electrónico."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por email '{email}': {e}")
            return None
        finally:
            conn.close()

def obtener_usuario_por_dni(dni):
    """Obtiene un usuario por su número de DNI."""  # ✅ Ahora está definida correctamente
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE dni = ?", (dni,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por DNI '{dni}': {e}")
            return None
        finally:
            conn.close()
def obtener_usuario_por_username(username):
    """Obtiene un usuario por su nombre de usuario."""  # ✅ Ahora está definida correctamente
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuario por username '{username}': {e}")
            return None
        finally:
            conn.close()
import sqlite3

def eliminar_usuario(user_id):
    try:
        conexion = sqlite3.connect("ordico.db")
        cursor = conexion.cursor()

        # Evitar eliminar un administrador
        cursor.execute("SELECT rol FROM usuarios WHERE id = ?", (user_id,))
        rol = cursor.fetchone()

        if rol and rol[0] == "admin":
            print("❌ No puedes eliminar un administrador.")
            return False

        # Eliminar solo si no tiene ventas asociadas
        cursor.execute("SELECT COUNT(*) FROM ventas WHERE usuario_id = ?", (user_id,))
        tiene_ventas = cursor.fetchone()[0]

        if tiene_ventas > 0:
            print("❌ No puedes eliminar un usuario con ventas asociadas.")
            return False

        # Proceder con la eliminación
        cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conexion.commit()

    except sqlite3.Error as e:
        print(f"❌ Error al eliminar usuario: {e}")
    
    finally:
        conexion.close()  # 🔹 Cierra la conexión aunque haya error

    print("✅ Usuario eliminado correctamente.")
    return True

def obtener_productos():
    """Obtiene la lista de productos desde la base de datos."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        conexion.close()
        
        return productos if productos else []  # Siempre devuelve una lista

    except sqlite3.Error as e:
        print(f"❌ Error al obtener productos: {e}")
        return []  # Devuelve lista vacía en caso de error
def agregar_producto(nombre, cantidad, precio):
    """Agrega un producto a la base de datos."""
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", (nombre, cantidad, precio))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.Error as e:
        print(f"❌ Error al agregar producto: {e}")
        return False

def actualizar_producto(id_producto, nuevo_precio):
    """Actualiza el precio de un producto dado su ID."""
    conn = conectar_db()    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE productos SET precio = ? WHERE id = ?", (nuevo_precio, id_producto))
            conn.commit()
            logging.info(f"✅ Precio actualizado para el producto con ID: {id_producto}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar precio para el producto con ID '{id_producto}': {e}")
            return False
        finally:
            conn.close()    
def eliminar_producto(id_producto):
    """Elimina un producto dado su ID."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
            conn.commit()
            logging.info(f"✅ Producto eliminado con ID: {id_producto}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al eliminar producto con ID '{id_producto}': {e}")
            return False
        finally:
            conn.close()

def actualizar_password(email, nueva_password):
    """Actualiza la contraseña de un usuario dado su correo electrónico."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET password = ? WHERE email = ?", (nueva_password, email))
            conn.commit()
            logging.info(f"✅ Contraseña actualizada para el usuario con email: {email}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar contraseña para '{email}': {e}")
            return False
        finally:
            conn.close()
def actualizar_rol_usuario(username, nuevo_rol):
    """Actualiza el rol de un usuario dado su nombre de usuario."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET rol = ? WHERE username = ?", (nuevo_rol, username))
            conn.commit()
            logging.info(f"✅ Rol actualizado para el usuario con username: {username}")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al actualizar rol para '{username}': {e}")
            return False
        finally:
            conn.close()
#funcion para ver cuantos usuarios hay
def obtener_usuarios():
    conn = conectar_db()    
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener usuarios: {e}")
            return None
        finally:
            conn.close()
def obtener_cantidad_usuarios():
    conn =sqlite3.connect(DB_PATH)
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            cantidad = cursor.fetchone()[0]
            return cantidad
        except sqlite3.Error as e:
            logging.error(f"❌ Error al obtener cantidad de usuarios: {e}")
            return 0
        finally:
            conn.close()

def eliminar_usuario(id_usuario):
    """Elimina un usuario de la base de datos según su ID."""
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
            conn.commit()
            logging.info(f"✅ Usuario con ID {id_usuario} eliminado correctamente.")
            return True
        except sqlite3.Error as e:
            logging.error(f"❌ Error al eliminar usuario con ID '{id_usuario}': {e}")
            return False
        finally:
            conn.close()
