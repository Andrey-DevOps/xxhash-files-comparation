import pathlib
import re
import paramiko

def run (yaml_config):
   hostname = yaml_config["config"][0]["credentials"]["hostname"]
   username = yaml_config["config"][0]["credentials"]["username"]
   password = yaml_config["config"][0]["credentials"]["password"]
   privateKeyAbsolutePath = yaml_config["config"][0]["credentials"]["privateKeyAbsolutePath"]
   port = yaml_config["config"][0]["credentials"]["port"]
   sourceAbsolutePath = yaml_config["config"][0]["sourceAbsolutePath"]

   privateKey = paramiko.RSAKey.from_private_key_file(privateKeyAbsolutePath)

   client = paramiko.SSHClient()
   client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
   client.connect(hostname=hostname,port=port,username=username,password=str(password),pkey=privateKey)
   def remote_dir_list(command):
      stdin, stdout, stderr = client.exec_command(command)
      dir_list= str((stdout.read().decode()))
      dir_list= list(filter(None,(list(dir_list.split("\n")))))
      return dir_list

   dir_list = remote_dir_list("find {0} -type d ".format(sourceAbsolutePath))

   def remote_files_checksum(command):
      stdin, stdout, stderr = client.exec_command(command)
      files_hash = str((stdout.read().decode())) # decode from bytes
      files_hash= list(filter(None, (list(files_hash.split("\n"))))) # convert multistring text into list
      for i in range(0, len(files_hash)): # parse and prettify our list
         files_hash[i] = list(files_hash[i].split(" ")) # split one string within arrey into list with two items: file and hash sum
         files_hash[i] = list(filter(None,files_hash[i])) # remove empty strings which was created because there are more then 1 space between two columns
         files_hash[i][1] = files_hash[i][1].replace(sourceAbsolutePath,"").strip("/")
      print(files_hash)
   files_hash = remote_files_checksum("find {0} -type f -exec md5sum {escape_md5sum_param} \;".format(sourceAbsolutePath,escape_md5sum_param="{}"))
   client.close()