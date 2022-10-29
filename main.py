from flask import Flask #utiliza el framework de flask
from flask import jsonify #nos permite trabajar con json un conversor de flask a json
from flask import request #recibir solicitudes y procesarlas
from flask_cors import CORS #es para de definir los origenes permitidos para los microservicios
import json #importando la libreria de json
from waitress import serve #desplegar y ejecutar los servicios en el localhost



#importando los controladores
from Controladores.ControladorCandidato import ControladorCandidato


app = Flask(__name__) #creacion instancia del servidor
cors = CORS(app)       #configuracion del cors

miControladorCandidato = ControladorCandidato()

#creacion de variable para mostrar rutas----------------------------------------------
#Rutas estudiantes
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