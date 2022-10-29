from flask import Flask #utiliza el framework de flask
from flask import jsonify #nos permite trabajar con json un conversor de flask a json
from flask import request #recibir solicitudes y procesarlas
from flask_cors import CORS #es para de definir los origenes permitidos para los microservicios
import json #importando la libreria de json
from waitress import serve #desplegar y ejecutar los servicios en el localhost



#importando los controladores
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.ControladorMesa import  ControladorMesa

app = Flask(__name__) #creacion instancia del servidor
cors = CORS(app)       #configuracion del cors

miControladorCandidato = ControladorCandidato()
miControladorMesa = ControladorMesa()

#creacion de variable para mostrar rutas----------------------------------------------
#Rutas Candidatos
@app.route("/candidatos",methods =['POST'])
def crearCandidato():
    data = request.get_json() #enviando informacion
    dictUsuario = miControladorCandidato.create(data)
    return jsonify(dictUsuario) #convertir un dict a json

@app.route("/candidatos/<string:id>",methods =['GET'])
def getCandidato(id):
    dictCandidato = miControladorCandidato.mostrarCandidato(id)
    return jsonify(dictCandidato)

@app.route("/candidatos",methods =['GET'])
def getCandidatos():
    dictCandidatos = miControladorCandidato.mostrarCandidatos()
    return jsonify(dictCandidatos)

@app.route("/candidatos/<string:id>",methods =['PUT'])
def putCandidato(id):
    data = request.get_json() #obtener informacion que envian desde el body
    dictCandidato = miControladorCandidato.update(id,data)
    return jsonify(dictCandidato)

@app.route("/candidatos/<string:id>",methods =['DELETE'])
def deleteCandidato(id):
    dictCandidato = miControladorCandidato.delete(id)
    return jsonify(dictCandidato)
#end rutas estudiantes----------------------------------------------



#creacion de variable para mostrar rutas----------------------------------------------
#Rutas Mesas
@app.route("/mesas",methods =['POST'])
def crearMesa():
    data = request.get_json() #enviando informacion
    dictMesa = miControladorMesa.create(data)
    return jsonify(dictMesa) #convertir un dict a json

@app.route("/mesas/<string:id>",methods =['GET'])
def getMesa(id):
    dictMesa = miControladorMesa.mostrarMesa(id)
    return jsonify(dictMesa)

@app.route("/mesas",methods =['GET'])
def getMesas():
    dictMesas = miControladorMesa.mostrarMesas()
    return jsonify(dictMesas)

@app.route("/mesas/<string:id>",methods =['PUT'])
def putMesa(id):
    data = request.get_json() #obtener informacion que envian desde el body
    dictMesa = miControladorMesa.update(id,data)
    return jsonify(dictMesa)

@app.route("/mesas/<string:id>",methods =['DELETE'])
def deleteMesa(id):
    dictMesa = miControladorMesa.delete(id)
    return jsonify(dictMesa)
#end Rutas Mesas----------------------------------------------


#creacion de variable para mostrar rutas----------------------------------------------
#Rutas Partido
@app.route("/departamentos",methods=['POST'])
def CrearDepartamento():
    datos = request.get_json()
    respuesta = miControladorDepartamento.crear(datos)
    return jsonify(respuesta)

@app.route("/departamentos",methods=['GET'])
def ObtenerDepartamentos():
    respuesta = miControladorDepartamento.mostrarDepartamentos()
    return jsonify(respuesta)

@app.route("/departamentos/<string:id>", methods=['GET'])
def ObtenerDepartamento(id):
    respuesta = miControladorDepartamento.mostrarDepartamento(id)
    return jsonify(respuesta)

@app.route("/departamentos/<string:id>", methods=['PUT'])
def ActualizarDepartamento(id):
    datos = request.get_json()
    respuesta = miControladorDepartamento.actualizar(id,datos)
    return jsonify(respuesta)

@app.route("/departamentos/<string:id>", methods = ['DELETE'])
def EliminarDepartamento(id):
    respuesta = miControladorDepartamento.eliminar(id)
    return jsonify(respuesta)

#Ruta de departamento con materia
@app.route("/materias/<string:id>/departamentos/<string:id_departamento>",methods=['PUT'])
def AsignarDepartamento(id, id_departamento):
    respuesta = miControladorMateria.asignarDepartamento(id,id_departamento)
    return jsonify(respuesta)
#end Rutas Partido----------------------------------------------


#las siguientes lineas se define la ruta y el microservicio donde se va a desplegar
@app.route("/",methods =['GET']) #creacion de rutas
def test():
    json={}
    json["mensaje"]="Servidor ejecutandose" #Para hacer un test y mostrar en el navegador
    return jsonify(json) #toma diccionarios a convertir en este caso json
    #luego se ejecuta la siguiente url en el navegador para ver el mensaje anterior http://127.0.0.1:9999/


#leer archivo config.json - cargando las configuraciones
def loadFileConfg():
    with open('config.json') as f:
        data = json.load(f)
    return data
if __name__=='__main__':
    dataConfig = loadFileConfg()
    print("Servidor corriendo en: " + "host: " + dataConfig["url-backend"] + " puerto: " + str(dataConfig["port"]))
    serve(app, host=dataConfig["url-backend"], port=dataConfig["port"])