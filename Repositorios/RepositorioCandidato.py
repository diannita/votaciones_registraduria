#importando de clase padre
from Repositorios.InterfaceRepositorio import InterfaceRepositorio
#importando el modelo que necesitamos en este caso Estudiante
from Modelos.Candidato import Candidato

#clase hija
class RepositorioCandidato(InterfaceRepositorio[Candidato]): #objeto a tener en cuenta es el modelo candidato y/o objetos de tipo candidato
    #palabra reservada pass - sirve para mantener la clase vacia - no implementar nada
    pass