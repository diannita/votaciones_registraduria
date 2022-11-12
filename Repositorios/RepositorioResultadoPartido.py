from Modelos.ResultadoPartido import ResultadoPartido
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from bson import ObjectId

class RepositorioResultadoPartido(InterfaceRepositorio[ResultadoPartido]):
    def getlistResultadosPartido(self, id_partido):
        query = {"Partido.$id": ObjectId(id_partido)}
        return self.query(query)