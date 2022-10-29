from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Partido import Partido

class ControladorPartido():
    def __init__(self):
        self.repositorioPartido = RepositorioPartido()
        print("Creando Controlado de Partido")

    def create(self, infoPartido):
        print("crear Partido")
        crearPartido = Partido(infoPartido)
        return self.repositorioPartido.save(crearPartido)

    def mostrarPartido(self, id):
        print("Mostrando el Partido con ID:"+str(id))
        elPartido = Partido(self.repositorioPartido.findById(id))
        return elPartido.__dict__

    def mostrarPartidos(self):
        print("Listar todos los Partidos")
        return self.repositorioPartido.findAll()

    def delete(self, id):
        print("Se elimino el Partido con el id: "+str(id))
        return self.repositorioPartido.delete(id)

    def update(self,id,PartidoDatos):
        print("Se Actualizo el Partido con id: "+str(id))
        partido = Partido(self.repositorioPartido.findById(id))
        partido.nombre = PartidoDatos["nombre"]
        return self.repositorioPartido.update(id, partido)