from Modelos.Partido import Partido
from Modelos.Mesa import Mesa
from Modelos.ResultadoPartido import ResultadoPartido
from Repositorios.RepositorioPartido import RepositorioPartido
from Repositorios.RepositorioMesa import RepositorioMesa
from Repositorios.RepositorioResultadoPartido import RepositorioResultadoPartido
from bson import ObjectId

class ControladorResultadoPartido():
    def __init__(self):
        print("Creando Controlado de Resultados Partido")
        self.repositorioResultadoPartido = RepositorioResultadoPartido()
        self.repositorioPartido = RepositorioPartido()
        self.repositorioMesa = RepositorioMesa()

    def createResultado(self, infoResultado, idM, idP):
        elresultado = ResultadoPartido(infoResultado)
        lamesa = Mesa(self.repositorioMesa.findById(idM))
        elpartido = Partido(self.repositorioPartido.findById(idP))
        elresultado.mesa = lamesa
        elresultado.partido = elpartido
        return self.repositorioResultadoPartido.save(elresultado)

    def showidResultado(self, id):
        resultado = ResultadoPartido(
            self.repositorioResultadoPartido.findById(id))
        return resultado.__dict__

    def showallResultado(self):
        return self.repositorioResultadoPartido.findAll()

    def updateResultado(self, idR, idM, idP, infoResultado):
        resultadoactual = ResultadoPartido(self.repositorioResultadoPartido.findById(idR))
        lamesa = Mesa(self.repositorioMesa.findById(idM))
        elpartido = Partido(self.repositorioPartido.findById(idP))
        resultadoactual.mesa = lamesa
        resultadoactual.partido = elpartido
        resultadoactual.numero_votos = infoResultado["numero_votos"]
        return self.repositorioResultadoPartido.save(resultadoactual)

    def deleteResultado(self, id):
        return self.repositorioResultadoPartido.delete(id)

    def listarResultadosCandidato(self, id):
        return self.repositorioResultadoPartido.getlistResultadosCandidato(id)