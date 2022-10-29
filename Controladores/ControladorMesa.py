from Modelos.Mesa import Mesa
from Repositorios.RepositorioMesa import RepositorioMesa

class ControladorMesa():
    def __init__(self):
        self.repositorioMesa = RepositorioMesa()
        print("creando controlador Mesa")

    # metodo crear
    def create(self, MesaDatos):
        print("crear una Mesa")
        crearMesa = Mesa(MesaDatos)
        return self.repositorioMesa.save(crearMesa)


    # metodo mostrar (unico - 1 materia)
    def mostrarMesa(self, id):
        print("mostrando una Mesa con id: "+str(id))
        mesaRegistrada = Mesa(self.repositorioMesa.findById(id))
        return mesaRegistrada.__dict__


    # metodo mostrar todos las materias
    def mostrarMesas(self):
        print("listar todos las Mesas")
        return self.repositorioMesa.findAll()


    # metodo eliminar
    def delete(self, id):
        print("se elimino la Mesa con id "+ str(id))
        return self.repositorioMesa.delete(id)


    # metodo actualizar
    def update(self, id, MesaDatos):
        print("se actualizo la Mesa con id " + str(id))
        actualizarMesa = Mesa(self.repositorioMesa.findById(id))
        actualizarMesa.numero = MesaDatos["numero"]
        actualizarMesa.cedulas_inscritas = MesaDatos["cedulas_inscritas"]
        return self.repositorioMesa.update(id, actualizarMesa)



