class ExamException(Exception):
        pass

class CSVFile:
    def __init__(self,name=None):
        self.name = name

    


    def get_data(self):
    #================================================================
        # ERRORI SUL NOME DEL FILE
        
        #il nome del file non è una stringa
        if self.name == None:
            raise ExamException("nome file vuoto")

        if type(self.name) != str:
            raise ExamException("il nome del file non è una stringa")

    #-----------------------
        #il nome del file è vuoto
        if self.name == "":
            raise ExamException("il nome del file è vuoto")
    
    #======================================================================
#------------------------
    #il file non è stato trovato

        name = self.name
        try:
            file = open(name)
        except FileNotFoundError:
            raise ExamException("non è stato trovato il file")

#=======================================================================
        casa = open(name)
       #salto la prima riga
        for i in casa:
            if "date" in i:
                next(file)
            elif "passengers" in i:
                next(file)
            elif "dat" in i:
                next(file)
            elif "pass" in i:
                next(file)
            break
#========================================================================

#-----------------------------------------------------------------------
        
        chek = 0
        listadivalori = []
        listadielementi = []
#-----------------------------------------------------------
        for line in file:
#------------------------------------------------------------
    # Righe completamente sbagliate (quindi la salta)
            
            if ","  not in line:
                continue
            
            if not(any(chr.isdigit() for chr in line)):
                continue

            if "-" not in line:
                continue
            
            if line == "":
                continue

        #--------------------------------------
            x = line.split(",")
        #--------------------------------------

    #---------------------------------------------------------
            try :
                x[1] = int(x[1])
            except ValueError:
    #---------------------------------------------------------
        # Se riesce a leggere un valore sulla riga, lo accetta comunque
                if any(chr.isdigit() for chr in x[1][0:1]):
                    if any(chr.isdigit() for chr in x[1][1:2]):
                        if any(chr.isdigit() for chr in x[1][2:3]):
                            if any(chr.isdigit() for chr in x[1][3:4]):
                                x[1] = int(x[1][0:4])
                            else:
                                x[1] = int(x[1][0:3])
                        else :
                            x[1] = int(x[1][0:2]) 
                    else : 
                        x[1] = int(x[1][0:1])
                
                    
        #altrimenti lo trasforma in None , e viene elaborato comunque             
                else:        
                    x[1] = None
                #listadielementi.append(x)
                #listadivalori.append(x[1])
            else:
    #----------------------------------------------------------
        # se il valore è negativo nullo o vuoto  
                if x[1] <= 0 :
                    x[1] = None
    #--------------------------------------------------------------------

    #-----------------------------------------------------------------
        # errori con la data , verifico se ce roba prima della data
            h = []
            h.append(x[0].split("-"))

            #-----------
            h[0][0] = h[0][0][-4:len(h[0][0])]

#---------------------------------------------
            if len(h[0][0]) < 4:
                continue

            try:
                int(h[0][1])
            except ValueError:
                continue

            try:
                int(h[0][0])
            except ValueError:
                continue

            
#--------------------------------------------------

            x[0] = h[0][0]+"-"+h[0][1]
                
                 
                
        #----------------------------------------
            listadielementi.append(x)
            listadivalori.append(x[1])
        #----------------------------------------

        #--------------------------------------------------
            #sistemo l'ordine cronologico
            # primo elemento
            if chek == 0 :
                primaarray = []
                ln = line.split(",")
                primaarray.append(ln)
                

                prima = primaarray[0][0]
                p = []
                p.append(prima.split("-"))

                b = int(p[0][0][-4:len(p[0][0])])
                b2 = int(p[0][1])-1
                
            chek = 1
            
            kr =[]
            kr.append(x[0].split("-"))
            
            
#----------------------------------------------
           
            a2 = int(kr[0][1])

           
            a = int(kr[0][0])
            
            
#----------------------------------------------
            #print(b,b2,a,a2)

            if chek == 1:
                if a==b or a==b+1:
                    b = a
                    if a2==b2+1:
                        b2 = a2
                        if b2==12:
                            b2=0
                        
                    else:
                        raise ExamException("un mese non è in ordine",line)
                else:
                    raise ExamException("un' anno non è in ordine",line)
            

# ------------------------------------------------------------------------- 
        if len(listadielementi) < 2:
            raise ExamException("la lista è troppo corta")

        if listadivalori == []:
            raise ExamException("la lista di valori è completamente vuota")
        count = 0
        for i in listadivalori:
            if i == None:
                count += 1
        if count == len(listadivalori):
            raise ExamException("la lista di valori è completamente nulla")    
#--------------------------------------------------------------------------                  


        #print(listadivalori)
        return listadielementi


#===========================================================================
#--------------------------------------------------------------------------

class CSVTimeSeriesFile(CSVFile):
    pass


time_series_file = CSVTimeSeriesFile("data.csv")
time_series = time_series_file.get_data()

#print(time_series)






#============================================================================0
#============================================================================0

def compute_avg_monthly_difference(time_series, first_year, last_year):
    #--------------------------------------------------------------
    # Nel caso il file si conclude in un mese non dicembre
    cot = time_series[-1][0]
    cot = cot.split("-")
    if int(cot[1]) != 12:
        time_series = time_series[0:-int(cot[1])]
    
    # Nel caso il file inizia non con gennaio

    sup = time_series[0][0]
    sup = sup.split("-")
    if int(sup[1]) != 1:
        time_series = time_series[13-int(sup[1]):len(time_series)]
    

        # TEST PER LE DATE DI  first_year e last_year
#======================================================================
    # l' anno finale iniziale deve essere una stringa

    if type(first_year) != str:
        raise ExamException("l'anno iniziale non è una stringa")

    if type(last_year) != str:
        raise ExamException("l'anno finale non è una stringa")

#---------------
    # vedo se la stringa si può trasformare in un intero

    try:
        int(first_year)
    except ValueError:
        raise ExamException("non puoi trasformare la stringa in un numero")

#---------------
    #l'anno iniziale o finale non si trovano a nel file

    flag = 0
    for i in time_series:
        if first_year in i[0]:
            flag = 1
    
    if flag==0:
        raise ExamException("l'anno iniziale non si trova all'interno della lista")


    flog = 0
    for i in time_series:
        if last_year in i[0]:
            flog = 1
    
    if flog==0:
        raise ExamException("l'anno finale non si trova all'interno della lista")

#------------------
    # l' anno iniziale finale sono stringhe vuote

    if first_year=="":
        raise ExamException("l'anno iniziale è una stringa vuota")

    if last_year=="":
        raise ExamException("l'anno finale è una stringa vuota")

#---------------
    #l'anno finale è più grande di quello iniziale

    if int(first_year)>=int(last_year):
        raise ExamException("troppi pochi anni o anni negativi")
    
#==================================================================


    #print(time_series)


# -----------------------------------------------------------------------
    # Creo un nuovo array che parte 
        #  gennaio di first_year  -> dicembre di last_year

    first = None
    last = None

    c = 0
    for i in time_series:
        if first_year in i[0]:
            first = c
            break
        else:
            c += 1
    d = 0
    for i in time_series:
        if last_year in i[0]:
            last = d
            break
        else:
            d += 1
    last += 12
    
    NuovaLista = time_series[first:last]  

#--------------------------------------------------------------------------

    #print(NuovaLista)
    #print()

#-------------------------------------------------------------------------
    # ANNI
    anni = int(last_year)-int(first_year)

    #print(anni)

#--------------------------------------------------------------------------
    #creo una lista di liste -> ogni lista 12 elementi, 

    valori=[]
    #valori.append(NuovaLista[0][0])
    for j in range(12):
        xx = 0
        pop = [NuovaLista[j+xx][1]]

        # anni = 2 = range(0,2) -> i va da 0 a 1 (2 escluso)
        for i in range(anni):         
            xx += 12
            pop.append(NuovaLista[j+xx][1])     
        valori.append(pop)  

#--------------------------------------------------------
    media = []
#-------------------------------------------------------
  # se abbiamo solo 2 anni  

    if anni+1==2:
        print(valori)
        for i in range(len(valori)):
            if None in valori[i]:
                media.append(0)
            else:
                media.append(abs(valori[i][0]-valori[i][1]))

#==================================================== 
  # se abbiamo più di 2 anni

    # elimino tutti i none da ogni lista
    if anni+1 > 2:
        for i in range(len(valori)):
            if None in valori[i]:
                sub = valori[i]
                valori[i] = []
                for j in sub:
                    if j != None:
                        valori[i].append(j)
                
      #---------------------------------------          
        #print(valori)

        
        for i in range(len(valori)):
            x = 0

          # se sono rimasti meno di 2 valori = 0
            if len(valori[i])<2:
                media.append(0)  

          # altrimenti mi fa la media dei valori risultanti       
            else:
                for j in range(len(valori[i])-1):
                    x = x + abs(valori[i][j]-valori[i][j+1])

                med = len(valori[i])-1 
                #print(med)  
                media.append(round(x/med,2))






    return media


        



#a = compute_avg_monthly_difference(time_series, "1949", "1950")
#print("-----------------------------------------")
#print(a)