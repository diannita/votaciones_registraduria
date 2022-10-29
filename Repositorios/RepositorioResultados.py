from Repositorios.InterfaceRepositorio import InterfaceRepositorio
from Modelos.Resultados import Resultados
from bson import ObjectId

class RepositorioResultados(InterfaceRepositorio[Resultados]):
    #Esta funcion nos muestra el listado de los candidatos que con cedulas inscritas por mesa
    def getListadoResultadoVotacion(self, id_mesa):
        theQuery = {"mesa.$id": ObjectId(id_mesa)}
        return self.query(theQuery)


    #Esta funcion nos muestra quien obtuvo la mayor numero de cedulas inscriptas en la mesa
    #Group - esta operacion de agregacion agrupara las mesas por id para buscar cada una en las mesas
    #mayor numero por mesa
    def getMayorNumeroPorMesa(self):
        query = {
            "$group": {
                "_id": "$mesa",
                "max": {
                    "$max": "$numero_mesa"
                },
                "doc": {
                    "$first": "$$ROOT"
                }
            }
        }
        pipeline = [query]
        return self.queryAggregation(pipeline)


    #buscar el promedio de la materias de todos los estudiantes
    def promedioNotasEnMateria(self, id_materia):
        query1 = {
                     "$match": {"materia.id": ObjectId(id_materia)}
                 },
        query2 = {
            "$group": {
                "_id": "$materia",
                "promedio": {
                    "$avg": "$nota_final"
                }
            }
        }
        pipeline = [query1, query2]
        return self.queryAggregation(pipeline)

