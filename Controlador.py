import sqlite3

def ComprobarUsuario(correo, password):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from Usuarios where CorreoUsuario = '" + correo + "' and Password = '" + password + "' and Estado = '1'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def ListaUsuarios(correo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select * from Usuarios where Estado = '1' and CorreoUsuario <>'" + correo + "'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def RegistrarUsuario(Usuario, correo, password, codigo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into Usuarios (NombreUsuario, CorreoUsuario, Password, Estado, CodigoActivacion) values ('"+ Usuario +"','" + correo + "','" + password + "','0','"+ codigo +"')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def ActivarUsuario(codigo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update Usuarios set estado = '1' where codigoactivacion = '" + codigo + "'"
    #consulta = "select * from Usuarios where CodigoActivacion = '" + codigo
    cursor.execute(consulta)
    db.commit()
    return 1

def RegistrarMensaje(asunto, mensaje, origen, destino):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "insert into Mensajeria (Asunto, Mensaje, Fecha, Hora, Origen, Destino, Estado) values ('"+ asunto +"','" + mensaje + "', DATE('now'), TIME('now'),'"+ origen +"','" + destino + "','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def Enviados(correo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.Asunto, m.Mensaje, m.Fecha, m.Hora, u.NombreUsuario from mensajeria m, usuarios u where u.CorreoUsuario = m.destino and m.origen = '"+ correo +"'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def Recibidos(correo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "select m.Asunto, m.Mensaje, m.Fecha, m.Hora, u.NombreUsuario from mensajeria m, usuarios u where u.CorreoUsuario = m.origen and m.destino = '"+ correo +"'"
    cursor.execute(consulta)
    resultado = cursor.fetchall()
    return resultado

def CambioPSW(password, correo):
    db = sqlite3.connect("Mensajes.s3db")
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    consulta = "update Usuarios set Password = '" + password + "' where CorreoUsuario = '" + correo + "'"
    cursor.execute(consulta)
    db.commit()
    return "1"