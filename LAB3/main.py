from platform import node
from client import *
from tree import Tree



if sys.platform == 'win32' and sys.version_info >= (3, 8):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
#function that reads a txt file and json/dict
#recives the file route and the encoding
def read_file(file,encoding="utf8"):
    reader = open(file, "r", encoding=encoding).read()
    return yaml.load(reader, Loader=yaml.FullLoader)

if __name__ == "__main__":
    #get the topo ande the users from files
    topo = read_file("topo.txt")
    names = read_file("users.txt")
    
    
    
    
    username = input("Username -> ")
    pswd = input("Password -> ")
    
    for key, value in names["config"].items():
        if username == value:
            nodo = key
            nodes = topo["config"][key]
            
    print(nodo,nodes)
    
    graph = Tree(topo, names).get_graph()