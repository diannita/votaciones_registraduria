from abc import ABCMeta #clase generica

#creando una clase padre para los demas modelos - modelo generica
class AbstractModelo(metaclass=ABCMeta):
    #creando un metodo
    def __init__(self,data):
        for key,value in data.items():
            setattr(self,key,value)




