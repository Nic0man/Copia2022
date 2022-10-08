from flask import Flask, render_template, request
import hashlib
import Controlador
from datetime import datetime
import envioemail

app = Flask(__name__)
CorreoOrigen = ''

@app.route('/') 
def index(): 
    return render_template('index.html')

@app.route('/login') 
def log_in(): 
    return render_template('login.html')

@app.route('/principal', methods = ["GET","POST"]) 
def centerMail(): 
    #if request.method == "POST":
    usu = request.form["txtusuario"]
    passw = request.form["txtpass"]

    password = passw.encode()
    password = hashlib.sha384(password).hexdigest()
    #print(password)

    respuesta = Controlador.ComprobarUsuario(usu, password)

    global CorreoOrigen

    if len(respuesta) == 0:
        CorreoOrigen = ''
        #mensaje = "<center><h2>Error en la autenticación, verifique su usuario y contraseña</h2><br><a href = '/login'><button> Regresar </button></a><center>"
        mensaje = "Error en la autenticación, verifique su usuario y contraseña"
        return render_template("informacion.html", data = mensaje)
    else:
        CorreoOrigen = usu
        respuesta2 = Controlador.ListaUsuarios(usu)
        return render_template("principal.html", data = respuesta2)

@app.route('/Registrar', methods = ["GET","POST"]) 
def RegistroUsuario():
    usu = request.form["txtnombre"]
    correo = request.form["txtusuarioregistro"]
    passw = request.form["txtpassregistro"]

    password = passw.encode()
    password = hashlib.sha384(password).hexdigest()
   
    codigo = str(datetime.now())
    codigo2 = codigo.replace("-","")
    codigo2 = codigo2.replace(":","")
    codigo2 = codigo2.replace(".","")
    codigo2 = codigo2.replace(" ","")


    resultado = Controlador.RegistrarUsuario(usu, correo, password,codigo2) 
    asunto = "Codigo de Activacion"
    mensaje = "Sr(a) Usuario. \n\n Su codigo de activacion es:\n\n " + codigo2 + "\n\n Recuerde copiarlo y pegarlo para validar su cuenta"
    envioemail.enviar(correo, asunto, mensaje)


    #print(codigo2)
    mensaje = "Usuario registrado"
    return render_template("informacion.html",  data = mensaje)

@app.route('/ActivarUsuario', methods = ["GET","POST"]) 
def ActivarUsuario():
    Codigo = request.form["txtcodigo"]
    resultado = Controlador.ActivarUsuario(Codigo)

    if resultado == 0:
        mensaje = "Error en la autenticación, Verifique el codigo de error"
        return render_template("informacion.html", data = mensaje)
    else:
        mensaje = "Activación de usuario Exitosa"
        return render_template("informacion.html", data = mensaje)

@app.route("/enviarEE",methods=["GET","POST"])
def enviarEE():
    asunto=request.form["asunto"]
    mensaje=request.form["mensaje"]
    destino=request.form["destino"]

    Controlador.RegistrarMensaje(asunto, mensaje, CorreoOrigen,destino)
    
    asunto2="Nuevo Mensaje Recibido"
    mensaje2="Sr usuario ingrese a la plataforma para que pueda observar su nuevo mensaje.\n\n Muchas Gracias."
    envioemail.enviar(destino,asunto2,mensaje2)
    
    return "Email enviado satisfactoriamente..."

@app.route("/CorreosEnviados",methods=["GET","POST"])
def CorreoEnviado():
    respuesta = Controlador.Enviados(CorreoOrigen)

    return render_template("historial.html", listacorreos = respuesta)

@app.route("/CorreosRecibidos",methods=["GET","POST"])
def CorreosRecibidos():
    respuesta = Controlador.Recibidos(CorreoOrigen)

    return render_template("historial.html", listacorreos = respuesta)

@app.route("/ActualizarPSW",methods=["GET","POST"])
def ActualizarPSW():
    passw = request.form["password"]

    passw2 = passw.encode()
    passw2 = hashlib.sha384(passw2).hexdigest()

    Controlador.CambioPSW(passw2, CorreoOrigen)

    return "Contraseña Actualizada Correctamente"




