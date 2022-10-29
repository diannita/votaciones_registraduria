import pymongo
import certifi
from bson import DBRef #
from bson.objectid import ObjectId #es para identificar los documentos
from typing import TypeVar, Generic, List, get_origin, get_args #importacion de variables
import json

T = TypeVar('T') #Creacion de variables generica

class InterfaceRepositorio(Generic[T]): #creacion de una clase generica
    #__init__ - creacion del metodo del constructor
    def __init__(self):
        ca = certifi.where() #carga de los certificados
        dataConfig = self.loadFileConfig()
        cliente = pymongo.MongoClient(dataConfig["data-db-connection"], tlsCAFile = ca) #conexion de la base de datos - se llama desde el config.json
        self.baseDatos = cliente[dataConfig['name-db']] #buscando el nombre de la base de datos - desde archivo config.json
        theClass = get_args(self.__orig_bases__[0])
        self.coleccion = theClass[0].__name__.lower() #acceso a las colecciones de la BD

    #LoadFileConfig - cargando el archivo de configuracion - se realiza la conversion del archivo config.json a diccionario
    def loadFileConfig(self):
        with open("config.json") as f:
            datos = json.load(f)
        return datos

    #Save - Guardado de un ID de un objeto dentro de la base de datos atravez de la conexion de la coleccion de la BD.
    def save(self, item: T):
        laColeccion = self.baseDatos[self.coleccion]
        elId = ""
        item = self.transformRefs(item)

        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion = self.baseDatos[self.coleccion]
            delattr(item, "_id")
            item = item.__dict__
            updateItem = {"$set": item}
            x = laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId = _id.inserted_id.__str__()

        x = laColeccion.find_one({"_id": ObjectId(elId)})
        x["_id"] = x["_id"].__str__()
        return self.findById(elId)


    #delete - Busca el objeto con el ID del objeto y lo elimina
    def delete(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count": cuenta}

    #Update - actualizar el ID de un objecto - busca el objeto en la coleccion y lo actualiza
    def update(self, id, item:T):
        laColeccion = self.baseDatos[self.coleccion]
        _id = ObjectId(id)
        delattr(item, "_id")
        item = item.__dict__
        updateItem = {"$set": item}
        x = laColeccion.update_one({"_id": _id}, updateItem)
        return {"updated_count": x.matched_count}

    #findById - Realiza la busqueda dek registro que concuerda con la informacion en la respectiva coleccion de la BD
    def findById(self, id):
        laColeccion = self.baseDatos[self.coleccion]
        x = laColeccion.find_one({"_id": ObjectId(id)})
        x = self.getValuesDBRef(x)
        if x == None:
            x = {}
        else:
            x["_id"] = x["_id"].__str__()
        return x

    #findAll - Lista todos los registros que pertenecen a una coleccion
    def findAll(self):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find():
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    #Query - Permite llevar a cabo consultas con la sintaxis propia de mongoDB
    #https://www.mongodb.com/docs/manual/reference/method/js-collection/
    def query(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.find(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    #queryAggregation - Permite llevar a cabo consultas con la sintaxis propia de Mongo DB para la tareas de agregacion
    def queryAggregation(self, theQuery):
        laColeccion = self.baseDatos[self.coleccion]
        data = []
        for x in laColeccion.aggregate(theQuery):
            x["_id"] = x["_id"].__str__()
            x = self.transformObjectIds(x)
            x = self.getValuesDBRef(x)
            data.append(x)
        return data

    #getValuesDBRef - permite consultar la informacion de las refrencias que posee un objeto consultado, ya qye en caso contrario de no utilizarlo solo apareceria la estructura de la referencia
    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k], DBRef):
                laColeccion = self.baseDatos[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k] = valor
                x[k] = self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and len(x[k]) > 0:
                x[k] = self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict):
                x[k] = self.getValuesDBRef(x[k])
        return x

    #getValuesDBRefFromLIst - Actua de manera parecida al metodo 'getValuesDBRef' pero analizando los elementos en las listas mienras que el anterios solo era en objetos.
    def getValuesDBRefFromList(self, theList):
        newList = []
        laColeccion = self.baseDatos[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"] = value["_id"].__str__()
            newList.append(value)
        return newList

    #transformObjectLds - convierte la informacion de un ObjectId de un registro especifico de la coleccion a un string
    def transformObjectIds(self, x):
        for attribute in x.keys():
            if isinstance(x[attribute], ObjectId):
                x[attribute] = x[attribute].__str__()
            elif isinstance(x[attribute], list):
                x[attribute] = self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute] = self.transformObjectIds(x[attribute])
        return x

    # formatList - Funciona de forma parecida al metodo anteriormente explicado pero aplicado a listas, verifica cada elemento y lleva a cabo los procesos de conversion.
    def formatList(self, x):
        newList = []
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList) == 0:
            newList = x
        return newList

    #ransformRefs - Analiza los obejetos que llegan referenciados a un elemento y segun el tipo de objeto formatea la referencia que servira para enlazar un objeto con otro en la BD.
    def transformRefs(self, item):
        theDict = item.__dict__
        keys = list(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object") == 1:
                newObject = self.ObjectToDBRef(getattr(item, k))
                setattr(item, k, newObject)
        return item

    #ObjectToDBRef - Dado un objeto detecta la clase a la que pertenece y formatea el valor de una referencia 'DBRef; con su respectivo nombre de coleccion e identificador con el objetivo poder simular las relaciones
    #como si fuera una base de datos relacional.
    def ObjectToDBRef(self, item: T): #T means item generico
        nameCollection = item.__class__.__name__.lower()
        return DBRef(nameCollection, ObjectId(item._id))
