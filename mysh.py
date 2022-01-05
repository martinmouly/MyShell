# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 17:17:27 2021
@author: Martin
"""
import os
import sys
import subprocess

#this function implements the built-in commands: pwd, cd, exit
def builtin(cmd,out):

    if cmd=='exit':
    	os.write(out,b'Exiting shell...\n')
    	exit()
    	return True
    elif cmd=='pwd':
    	wd=os.getcwd()
    	os.write(out,f'Current working directory is {wd}\n'.encode('utf-8'))
    	return True
    elif cmd=='cd':
    	os.chdir(os.getenv("HOME"))
    	return True
    elif cmd[:3]=='cd ':
    	try:
    		os.chdir(cmd[3:])
    	except:
    		error(out)
    	return True
    return False
        

#this function executes the input on a subprocess
def execute(cmd,out):
	#in case of redirection
	if '>' in cmd:
		cmd=cmd.replace(">"," ")
		cmd_list=cmd.split()
		#the output file is at the last index of the cmd list
		output_file=cmd_list[len(cmd_list)-1]
		
		#the actual cmd is the all the input except the last one which is the file
		my_cmd=cmd_list[:len(cmd_list)-1]
		try:
			with open(output_file, "w") as outfile:
    				subprocess.run(my_cmd, stdout=outfile)
		except:
			error(out)
	else:
		cmd_list=cmd.split()
		try:
			subprocess.run(cmd_list)
		except:	
			error(out)
			
def batch(cmd):
	#open the output file, where results of commands (without redirection) will be printed
	outfile = os.open("batch_output", os.O_APPEND|os.O_CREAT|os.O_RDWR)
	
	#open batch file
	with open(cmd[1:len(cmd)-1], "r") as batchfile:
	
		#read each lines of batch file
		lines=batchfile.readlines()
		
		for line in lines:
			#write cmd on output file
			os.write(outfile,line.encode('utf-8'))
			
			#remove \n to execute cmd
			line=line[:len(line)-1]
			
			#remove white space at the start and end of command
			line=line.strip()
			
			#command execution, similar as in the interactive loop
			if builtin(line,outfile)==True:
				cmd=cmd
			else:
				if '>' in line:
					print(line)
					execute(line,outfile)
				else:
					cmd_list=line.split()
					try:
						subprocess.run(cmd_list,stdout=outfile)
					except:	
						error(outfile)
					
					
				
	
def error(out):
	err = "An error has occurred\n"
	os.write(out, err.encode('utf-8'))

        
#interactive loop
while True:
    #input command
    cmd=input('mysh$ ')
    
    #remove white space at the start and end of command
    cmd=cmd.strip()
    
    #check if batch mode
    if cmd[0]=='[' and cmd[len(cmd)-1]==']':
    	batch(cmd)
    	
    #if not, check if command is a built-in command
    elif builtin(cmd,1)==True:
    	cmd=cmd
    	
    #if not, execute command on new process
    else:
    	execute(cmd,1)
    
    
    

