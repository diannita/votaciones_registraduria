#los controladores se encargan de manipular los modelos donde se puede realizar el CRUD

from Modelos.Candidato import Candidato
from Repositorios.RepositorioCandidato import RepositorioCandidato
from Repositorios.RepositorioPartido import RepositorioPartido
from Modelos.Partido import Partido

class ControladorCandidato():
    #creacion de metodos
    #metodo init
    def __init__(self):
        self.repositorioCandidato = RepositorioCandidato()
        self.repositorioPartido = RepositorioPartido()
        print("creando controlador Candidato") #print informativo

    #metodos de la operacion del CRUD
    #metodo crear
    def create(self, candidatoDatos):
        print("crear un Candidato")
        #creando una variable donde se recibe la informacion
        crearCandidato = Candidato(candidatoDatos)
        return self.repositorioCandidato.save(crearCandidato)


    #metodo mostrar (unico - 1 estudiante)
    def mostrarCandidato(self, id):
        print("mostrando el Candidato con id: "+str(id)) # dejamos este mensaje como informativo
        elCandidato= Candidato(self.repositorioCandidato.findById(id))
        return elCandidato.__dict__


    #metodo mostrar todos los estudiantes
    def mostrarCandidatos(self):
        print("listar todos los Candidatos")
        return self.repositorioCandidato.findAll()


    #metodo eliminar
    def delete(self, id):
        print("se elimino el Candidato con id "+ str(id))
        return self.repositorioCandidato.delete(id)


    #metodo actualizar
    def update(self, id, candidatoDatos):
        print("se actualizo el candidato con id " + str(id))
        actualizarCandidato = Candidato(self.repositorioCandidato.findById(id))
        actualizarCandidato.cedula = candidatoDatos["cedula"]
        actualizarCandidato.nombre_resolucion = candidatoDatos["nombre_resolucion"]
        actualizarCandidato.nombre = candidatoDatos["nombre"]
        actualizarCandidato.apellido = candidatoDatos["apellido"]
        return self.repositorioCandidato.update(id, actualizarCandidato)


    #Relacion partido y candidato
    def asignarPartido(self, id, id_partido):
        candidatoActual = Candidato(self.repositorioCandidato.findById(id))
        partidoActual = Partido(self.repositorioPartido.findById(id_partido))
        candidatoActual.partido = partidoActual #crea un nuevo campo en MongoDB haciendo una referencia entre depart y materia
        return self.repositorioCandidato.save(candidatoActual)

