from ftplib import FTP
from getpass import getpass

def FTPSubmit(archlocal):
    """ Esta funcion hace submit a un JCL.
    El parametro que recibe es la ruta completa del archivo a submitir"""
    
    print("Realizando conexion via FTP........")
    ftpip = input('Ingresa direccion IP...')
    ftp = FTP(ftpip)
    user = input('Ingresa usuario......')
    
    password = getpass('Ingresa el password para el usuario {0} en la ip {1}'.format(user,ftpip))
    ftp.login(user,password)
    print('Conexion realizada a ' + ftpip + ' con usuario ' + user)


    archremoto = archlocal
    localfile = open(archremoto,'rb')

   
    ftp.voidcmd('site filetype=jes')
    ftp.sendcmd('site jesstatus=all jesjobname=* jesowner=SITOJEB')
   
    #Las siguientes dos lineas muestran el spool existente para este owner
    print('Mostrando spool antes de dar submit...')
    ftp.dir()

    print('*'*20)
    
    
    ftp.storlines('STOR ' + archremoto, localfile)

    
    #La siguiente seccion muestra el spool actualizado...

    print('Mostrando spool actualizado.....')
    import time
    time.sleep(20)
    ftp.sendcmd('site jesstatus=all jesjobname=* jesowner=SITOJEB')
    ftp.dir()


    ftp.quit()
    localfile.close()
    jobname = buscaJobName(archlocal)
    
    print('Job submitido con nombre.... ',jobname)
    return jobname