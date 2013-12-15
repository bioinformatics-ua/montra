from emif.settings import jerboa_collection
from pymongo.errors import OperationFailure


json_data = {
    'name': 'mongo3',
    'teste': 5,
    'cenas': 'coiso2'
}

try:
    # Create MONGO record
    data_example = jerboa_collection.insert(json_data)
    # get last inserted record
    print jerboa_collection.find_one()
    print "Sucesso!"
except OperationFailure:
    print "Erro!"