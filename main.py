from flask import Flask #utiliza el framework de flask
from flask import jsonify #nos permite trabajar con json un conversor de flask a json
from flask import request #recibir solicitudes y procesarlas
from flask_cors import CORS #es para de definir los origenes permitidos para los microservicios
import json #importando la libreria de json
from waitress import serve #desplegar y ejecutar los servicios en el localhost



#importando los controladores
from Controladores.ControladorCandidato import ControladorCandidato
from Controladores.ControladorMesa import  ControladorMesa
from Controladores.ControladorPartido import ControladorPartido
from Controladores.ControladorResultados import ControladorResultados
from Controladores.ControladorResultadoPartido import ControladorResultadoPartido

app = Flask(__name__) #creacion instancia del servidor
cors = CORS(app)       #configuracion del cors

miControladorCandidato = ControladorCandidato()
miControladorMesa = ControladorMesa()
miControladorPartido= ControladorPartido()
miControladorResultados = ControladorResultados()
miControladorResultadoPartido = ControladorResultadoPartido()

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
@app.route("/partidos",methods =['POST'])
def crearPartido():
    data = request.get_json() #enviando informacion
    dictPartido = miControladorPartido.create(data)
    return jsonify(dictPartido) #convertir un dict a json

@app.route("/partidos",methods=['GET'])
def ObtenerPartidos():
    respuesta = miControladorPartido.mostrarPartidos()
    return jsonify(respuesta)

@app.route("/partidos/<string:id>", methods=['GET'])
def ObtenerPartido(id):
    respuesta = miControladorPartido.mostrarPartido(id)
    return jsonify(respuesta)

@app.route("/partidos/<string:id>", methods=['PUT'])
def ActualizarDepartamento(id):
    datos = request.get_json()
    respuesta = miControladorPartido.update(id,datos)
    return jsonify(respuesta)

@app.route("/partidos/<string:id>", methods = ['DELETE'])
def EliminarPartido(id):
    respuesta = miControladorPartido.delete(id)
    return jsonify(respuesta)

#Ruta de candidatos con partido
@app.route("/candidatos/<string:id>/partidos/<string:id_partido>",methods=['PUT'])
def AsignarPartido(id, id_partido):
    respuesta = miControladorCandidato.asignarPartido(id,id_partido)
    return jsonify(respuesta)
#end Rutas Partido----------------------------------------------

#creacion de variable para mostrar rutas----------------------------------------------
#Rutas Resultados (Se realiza la creacion y manipulacion de los datos de resultados)
#Ruta de resultados mesa y candidato
@app.route("/resultados/candidatos/<string:id_candidato>/mesas/<string:id_mesa>",methods=['POST'])
def crearResultados(id_candidato,id_mesa):
    data = request.get_json()
    respuesta = miControladorResultados.create(data,id_candidato,id_mesa)
    return jsonify(respuesta)

@app.route("/resultados",methods=['GET'])
def mostrarInscripciones():
    respuesta = miControladorResultados.mostrarResultados()
    return jsonify(respuesta)

@app.route("/resultados/<string:id>",methods = ['GET'])
def mostrarResultados(id):
    respuesta = miControladorResultados.mostrarResultado(id)
    return jsonify(respuesta)

@app.route("/resultados/<string:id>/candidato/<string:id_candidato>/mesa/<string:id_mesa>",methods = ['PUT'])
def ActualizarResultados(id, id_candidato, id_mesa):
    data = request.get_json()
    respuesta = miControladorResultados.update(id, data, id_candidato, id_mesa)
    return jsonify(respuesta)

@app.route("/resultados/<string:id>",methods =['DELETE'])
def EliminarRespuesta(id):
    respuesta = miControladorResultados.delete(id)
    return jsonify(respuesta)



# -----------GET Reportes------------
# Candidatos inscritos
@app.route("/resultados/candidato/<string:id_candidato>", methods = ['GET'])
def inscritosEnCandidatos(id_candidato):
    json = miControladorResultados.listarResultadosCandidato(id_candidato)
    return jsonify(json)

# Resultado de partidos
@app.route("/resultadopartido", methods = ['GET'])
def getResultadoPartido():
    json = miControladorResultadoPartido.showallResultado()
    return jsonify(json)

# creacion de resultados partidos (mesas y partidos)
@app.route("/resultadopartido/mesa/<string:idMesa>/partido/<string:idPartido>", methods = ['POST'])
def crearResultadoMesaPartido(idMesa, idPartido):
    data = request.get_json()
    json = miControladorResultadoPartido.createResultado(data, idMesa, idPartido)
    return jsonify(json)



# Mirar los resultados de una mesa en particular
# @app.route("/resultados/mesa/<string:id_mesa>", methods=["GET"])
# def inscritosEnMesa(id_mesa):
#     json = miControladorResultados.getListarCandidatosMesa(id_mesa)
#     return jsonify(json)
#
# #Buscar un candidato en todas las mesas
# @app.route("/resultados/mesas/<string:id_candidato>", methods=["GET"])
# def inscritoEnMesas(id_candidato):
#     json = miControladorResultados.getListarMesasDeInscritoCandidato(id_candidato)
#     return jsonify(json)
#
# #Buscar la cedula
# @app.route("/resultados/documento", methods=["GET"])
# def getMaxDocument():
#     json = miControladorResultados.getMayorCedula()
#     return jsonify(json)


#End Inscripcion----------------------------------------------


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