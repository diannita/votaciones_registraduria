from Repositorios.RepositorioResultados import RepositorioResultados
from Repositorios.RepositorioCandidato import RepositorioCandidato
from Repositorios.RepositorioMesa import RepositorioMesa

from Modelos.Candidato import Candidato
from Modelos.Mesa import Mesa
from Modelos.Resultados import Resultados


class ControladorResultados():
    def __init__(self):
        print("Creando Controlado de Resultados")
        self.repositorioResultados = RepositorioResultados()
        self.repositorioMesa = RepositorioMesa()
        self.repositorioCandidato = RepositorioCandidato()

    def create(self, infoResultados, id_candidato, id_mesa):
        print("crear Inscripcion")
        crearResultados = Resultados(infoResultados)
        candidato = Candidato(self.repositorioCandidato.findById(id_candidato))
        mesa = Mesa(self.repositorioMesa.findById(id_mesa))
        crearResultados.candidato = candidato
        crearResultados.mesa = mesa
        return self.repositorioResultados.save(crearResultados)

    def mostrarResultado(self, id):
        print("Mostrando el Resultados con ID:"+str(id))
        elResultados = Resultados(self.repositorioResultados.findById(id))
        return elResultados.__dict__

    def mostrarResultados(self):
        print("Listar todos los Resultadoss")
        return self.repositorioResultados.findAll()

    def delete(self, id):
        print("Se elimino los Resultados con el id: "+str(id))
        return self.repositorioResultados.delete(id)

    def update(self, id, ResultadosDatos, id_candidato, id_mesa):
        print("Se Actualizo el Resultados con id: " + str(id))
        resultado = Resultados(self.repositorioResultados.findById(id))
        resultado.numeromesa = ResultadosDatos["numeromesa"]
        resultado.partido = ResultadosDatos["partido"]
        candidato = Candidato(self.repositorioCandidato.findById(id_candidato))
        mesa = Mesa(self.repositorioMesa.findById(id_mesa))
        resultado.candidato = candidato
        resultado.materia = mesa
        return self.repositorioResultados.save(resultado)

    def listarResultadosCandidato(self, id_candidato):
        return self.repositorioResultados.getListResultadosCandidato(id_candidato)

    def getListarCandidatosMesa(self, id_mesa):
        return self.repositorioResultado.getListadoCandidatosInscritosMesa(id_mesa)

    def getListarMesasDeInscritoCandidato(self, id_candidato):
        return self.repositorioResultado.getListadoMesasCandidatoInscrito(id_candidato)

    def getMayorCedula(self):
        return self.repositorioResultado.getNumeroCedulaMayorCandidato()