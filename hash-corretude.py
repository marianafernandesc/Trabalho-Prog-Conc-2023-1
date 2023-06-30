import hashlib
import os
#file = "1.html" # Location of the file (can be set a different way)

#print (file_hash.hexdigest()) # Get the hexadecimal digest of the hashs

hashesConcorrentes = {}
hashesSequenciais = {}

def compararSeqConc(novelPath):


    for nome_arquivo in os.listdir(novelPath):
        BLOCK_SIZE = 65536 # The size of each read from the file
        file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        value =nome_arquivo    
        nome_arquivo = f"{novelPath}/{nome_arquivo}"
        #nome_arquivo = f"daddy-i-dont-want-to-marry/63.html"
        with open(nome_arquivo, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
                hashesConcorrentes[value]=file_hash.hexdigest()

    for nome_arquivo in os.listdir(f"sequencial/{novelPath}"):
        BLOCK_SIZE = 65536 # The size of each read from the file
        #
        value = nome_arquivo
        #nome_arquivo = f"sequencial/daddy-i-dont-want-to-marry/63.html"
        nome_arquivo = f"sequencial/{novelPath}/{nome_arquivo}"
        file_hash = hashlib.sha256() # Create the hash object, can use something other than `.sha256()` if you wish
        with open(nome_arquivo, 'rb') as f: # Open the file to read it's bytes
            fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
            while len(fb) > 0: # While there is still data being read from the file
                file_hash.update(fb) # Update the hash
                fb = f.read(BLOCK_SIZE) # Read the next block from the file
                hashesSequenciais[value]=file_hash.hexdigest()




    #print(hashesConcorrentes)
    #print(hashesSequenciais)

    for chave, hashConc in sorted(hashesConcorrentes.items()):
        hashSeq = hashesSequenciais[chave]
        if(hashSeq != hashConc):
            print(chave)
            print(hashSeq)
            print(hashConc)


compararSeqConc("daddy-i-dont-want-to-marry")
compararSeqConc("death-is-the-only-ending-for-the-villain")
compararSeqConc("the-guidebook-for-villainesses")
compararSeqConc("the-exhausting-reality-of-novel-transmigration")