from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultados import Resultados
from bson import ObjectId

class RepositorioResultados(InterfaceRepositorio[Resultados]):
    def getListResultadosCandidato(self, id_candidato):
        query = {"Candidato.$id": ObjectId(id_candidato)}
        return self.query(query)
