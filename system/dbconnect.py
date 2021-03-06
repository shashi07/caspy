import MySQLdb as mdb
import sys

def runquery(query) :
    
    try :
        con = d=mdb.connect('localhost','caspy','caspy','caspy')
        cur = con.cursor()
        print query
        cur.execute(query)
        a = cur.fetchall()
    except mdb.Error, e :
        a = -1
        print e
    finally :
        if con :
            con.commit()
            con.close()

    return a

def insertInDir(dname,pdname,user) :

    query = """select dir_id from dirs where dir_name = "%s" AND parent_dir ="%s" AND username = "%s";""" %(dname,pdname,user)
    a=runquery(query);
    print a;
    if(len(a) == 0 ) :
        query = """insert into dirs(dir_name,parent_dir,username) values ('%s','%s','%s');"""%(dname,pdname,user)
        runquery(query)
        query = """select dir_id from dirs where dir_name = "%s" AND parent_dir ="%s" AND username = "%s";""" %(dname,pdname,user)
        a=runquery(query);

    return a[0][0]


def insertInHashes(hashes,size):
    query = """select hash_id from hashes where hash = "%s";""" %(hashes,)
    a = runquery(query)

    if (len(a) == 0):
        query = """insert into hashes(hash,size) values ('%s','%d');"""%(hashes,size)
        runquery(query)
        query = """select hash_id from hashes where hash = "%s";""" %(hashes,)
        a=runquery(query)
    
    return a[0][0]

def insertInFiles(fileName,dir_id,no_of_blocks):
    
    query = """select f_id from filelist where filename = "%s" AND dir_id = "%d";""" %(fileName,dir_id)
    a = runquery(query)

    if (len(a) == 0):
        query = """insert into filelist(filename,no_of_blocks,dir_id) values ('%s','%d','%d');"""%(fileName,no_of_blocks,dir_id)
        runquery(query)
        query = """select f_id from filelist where filename = "%s" AND dir_id = "%d";""" %(fileName,dir_id)
        a = runquery(query)
    
    return a[0][0]

def insertInBlocks(block_no,f_id,hash_id):

    query = """insert into fileBlocks(block_no,f_id,hash_id) values ('%d','%d','%d');"""%(block_no,f_id,hash_id)
    a=runquery(query)
    if a== -1 :
        query = """delete from fileBlocks where block_no ='%d' and f_id='%d' """  % (block_no,f_id)
        runquery(query)

        query = """insert into fileBlocks(block_no,f_id,hash_id) values ('%d','%d','%d');"""%(block_no,f_id,hash_id)
        a=runquery(query)
    return 1


def checkHash(hashes):
    query = """select hash_id from hashes where hash = "%s";""" %(hashes,)
    a = runquery(query)

    if (len(a) == 0):
        return None 
    return a[0][0]

def checkFile(fname,dir_id):

    query = """select f_id from filelist where filename = "%s" AND dir_id = "%d";""" %(fname,dir_id)
    a = runquery(query)
    if (len(a) == 0):
        return None 
    return a[0][0]


def deleteBlocks(f_id):

    query = """delete from fileBocks where f_id = "%d";""" %(dir_id,)
    a = runquery(query)
    return 1

def selectAllBlocks(f_name,dname,pdname,user):

    query = """select dir_id from dirs where dir_name = "%s" AND parent_dir ="%s" AND username = "%s";""" %(dname,pdname,user)
    dir_id=runquery(query);
    if(len(dir_id) == 0 ) :
        return None
    print dir_id
    dir_id = dir_id[0][0]
    query = """select f_id from filelist where filename = "%s" AND dir_id = "%d";""" %(f_name,dir_id)
    f_id=runquery(query);
    if(len(f_id) == 0 ) :
        return None
    f_id = f_id[0][0]
    print f_id
    query = """select b.hash from fileBlocks a, hashes b where f_id = "%d" and a.hash_id = b.hash_id order by a.block_no;""" %(f_id,)
    a =runquery(query);
    
    filedata =""
    print a
    for i in a :
        for j in i :
            f = open("Files/"+j,"rb+")
            filedata = filedata + f.read()
            f.close()
    return filedata

def showfiles(dname,pdname,user):

    query = """select dir_id from dirs where dir_name = "%s" AND parent_dir ="%s" AND username = "%s";""" %(dname,pdname,user)
    dir_id=runquery(query);
    if(len(dir_id) == 0 ) :
        return None
    print dir_id
    dir_id = dir_id[0][0]
    query = """select f_id from filelist where dir_id = "%d";""" %(dir_id,)
    f_ids =runquery(query);
    if(len(f_ids) == 0 ) :
        return None
    
    print f_ids    
    return "\n".join(f_ids)
    #print a
    



