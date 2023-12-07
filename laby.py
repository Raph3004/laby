#25/10/2023
#Tremblay,Raphaël_Christ,Ludovic
#Programme qui génères un labyrinthe

from random import random

 # créer une liste de n
def sequence(n):
    return list(range(n))

def testSequence():
    assert sequence(5) ==[0,1,2,3,4], 'sequence(5) incorrect'
    assert sequence(-2) ==[],         'sequence(-2) incorrect'



 # permet d'ajouter un élément
def ajouter(tab,x):
    if not contient(tab, x):
        tab.append(x)
    return tab

def testAjouter():
    assert ajouter([2,3,4],8) == [2, 3, 4, 8], 'ajouter([2,3,4],8) incorrect'
    assert ajouter([1,2,3],3) == [1,2,3],      'ajouter([1,2,3],3) incorrect'
        
    # confirme si x est dans la liste tab
def contient(tab,x):
    return x in tab

def testContient():
        assert contient([2,4,5],4) == True,  'contient([2,4,5],4) incorrect'
        assert contient([1,2,4],3) == False, 'contient ([1,2,4],3) incorrect'
    
 # retire x de la liste tab
def retirer(tab,x):
    if  contient(tab, x):
        tab.remove(x)
    return tab

def test_retirer():
    assert retirer([1,2,3,4,5,],3)==[1,2,4,5], 'retirer incorrect'
    assert retirer([2,4,6,8],1)==[2,4,6,8], 'retirer incorrect'
    assert retirer([1,1,1,2,4,5],1)==[2,4,5], 'retirer incorrect'
    assert retirer([],5)==[], 'retirer incorrect'

 # trouve les voisins de la cellule auquelle x,y appartient
def voisins(x, y, nx, ny):
    listVoisins = []

    if x > 0:
        listVoisins.append((x - 1) + y * nx)  # ouest

    if x < nx - 1:
        listVoisins.append((1 + x) + y * nx)  # est

    if y > 0:
        listVoisins.append(x + (y - 1) * nx)  # nord

    if y < ny - 1:
        listVoisins.append(x + (y + 1) * nx)  # sud

    return listVoisins

def testVoisins():
        assert voisins(0, 0, 3, 3) == [1, 3], 'voisins(0, 0, 3, 3) incorrect'
        assert voisins(2, 2, 3, 3) == [5, 8], 'voisins(2, 2, 3, 3) erreur'
        assert voisins(0, 2, 3, 3) == [1, 5], ' voisins(0, 2, 3, 3) incorrect'
        assert voisins(2, 0, 3, 3) == [3, 7], ' voisins(2, 0, 3, 3) incorrect'
        assert voisins(1, 0, 3, 3) == [0, 2, 4],'voisins(1, 0, 3, 3) incorrect'
        assert voisins(0,0,0,0) ==0, ' voisins(0,0,0,0) incorrect'
    
# cell1=cave
# cell2= voisin
# permet de déterminer la direction du mur que la cellule dans cave
# et le voisin partage

def murEntreVoisin(cell1,cell2,nx):
    if cell1==cell2+1:    #est
        return 1
    if cell1==cell2-1:    #ouest
        return 3
    if cell1==cell2+nx:    #sud
        return 2
    if cell1==cell2-nx:    #nord
        return 0
def testMurEntreVoisin():
    assert murEntreVoisin(5,6,3)==1 #mur vers l'est
    assert murEntreVoisin(6,5,3)==3 #mur vers l'ouest
    assert murEntreVoisin(3,6,3)==2 #mur vers sud
    assert murEntreVoisin(6,3,3)==0 #mur vers nord
    assert murEntreVoisin(1,8,3) is None #correspond a aucun mur
    
    #permet d'identifier si le mur est verti ou horizon
def murSupp(cell,direction,nx,ny):
    
    if direction==0:       
        return cell,0     #nord
    
    
    elif direction==1:    #est
        y = cell // nx
        return cell+y+1 ,1
    
    elif direction==3:    #ouest
        y = cell // nx
        return cell+y ,1
    
    elif direction==2:    #sud
        return cell+nx,0
def testMurSupp():
        assert murSupp(5,0,3,3) == (5,0) #enlève le mur du nord 
        assert murSupp(5,1,3,3) == (6,1) #enlève le mur de l'est
        assert murSupp(6,3,3,3) == (6,1) #enlève mur de l'ouest
        assert murSupp(5,2,3,3) == (8,0) #enlève mur du sud    



        
    # crée un labyrinthe aléatoire en fonction de la largeur,de la hauteur 
    # et de la dimension
    
def laby(nx, ny, dimension):
    blanc = "#FFF"
    noir = "#000"
    setScreenMode(nx * dimension+1, ny * dimension+1)
    b=nx*dimension+1
    z=ny*dimension+1
     # permet d'initialiser tout les pixels en blanc
    for x in range(nx*dimension+1):
        for y in range(ny*dimension+1):
            setPixel(x,y,blanc)
    
    
    horiz = sequence(nx * (ny + 1))
    
    verti = sequence((nx + 1) * ny)
  
    cave = [0]
    front = []
     # cell départ 
    front=voisins(0,0,nx,ny)
                
    while front:
        # choisi une cell aleatoire dans front
        cell = int(random() * len(front))
        cell=front[cell]
        x = cell % nx
        y = cell // nx
        
        listVoisins=voisins(x,y,nx,ny)
        # ajoute la cell voisine dans front si elle n'est pas dans cave/front
        for v in listVoisins:            
            if v not in front and v not in cave:
                ajouter(front,v)
                
        for v in listVoisins:
            index_aléatoire = int(random() * len(listVoisins))
            v = listVoisins[index_aléatoire]
            if v in cave:
                murDirection=murEntreVoisin(v,cell,nx)
                 
                mur,estVerticale= murSupp(cell,murDirection,nx,ny)
                # Retirer le mur de la grille en fonction de sa position
                # et de son orientation
                if estVerticale:
                    retirer(verti,mur)
                    
                else:
                    retirer(horiz,mur)
                retirer(front,cell)
                ajouter(cave,cell)
                break
                
    retirer(horiz,0)  # retire start
    dernierMur=horiz.pop()
    retirer(horiz,dernierMur) # retire fin
    
  
   # dessine les murs horizontale present dans la liste horiz
    for mur in horiz:
        x = mur % nx       
        y = mur// nx
       
        for i in range(dimension):           
            setPixel(x*dimension+i,y*dimension,noir)
   # dessine les murs verticale present dans la liste verti  
    for mur in verti:
              
        x = mur % (nx+1)    
        y = mur//(nx+1)
        
        for i in range(dimension):           
            setPixel(x*dimension,y*dimension+i,noir)
                                                                                                              
 

  
laby(10,9,20)
  

