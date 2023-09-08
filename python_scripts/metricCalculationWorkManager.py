import os
import subprocess
import shutil
import zipfile
import sys

thispath = os.path.abspath(os.path.dirname(__file__))

def full_file_path(string):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), string)


def full_script_path(string, param=""):
    if len(param) == 0:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), string)
    else:
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), string) + " " + param

def run_command(cmd, outFile, errFile):
    print("running new command {}".format(" ".join(cmd)))
    fo = open(outFile, "w")
    fe = open(errFile, "w")
    p = subprocess.Popen(cmd,
                         stdout=fo,
                         stderr=fe,
                         universal_newlines=True
                         )
    
   # while (True):
   #     returncode = p.poll()  # returns None while subprocess is running
   #     outputLine = p.stdout.readline()
   #     errLine = p.stderr.readline()
   #     if outputLine:
   #         fo.write(outputLine)
   #     if errLine:
   #         fe.write(errLine)
   #     if returncode is not None:
   #         print("returncode is {}. ".format(returncode))
   #         break
    # read the remaining lines in the buffers
    #outputLines = p.stdout.readlines()
    #for outputLine in outputLines:
    #    fo.write(outputLine)
    #errLines = p.stderr.readlines()
    #for errLine in errLines:
    #    fo.write(errLine)
    #fo.close()
    #fe.close()

if __name__ == '__main__':
    num_process = 2

    if len(sys.argv) > 3:
        num_process = int(sys.argv[1])
        type_input=sys.argv[2]
        main_dir=sys.argv[3]
    else:
        print("Error: Please provide all arguments")
        quit()

    if(type_input=='z' or type_input=='d'):
        #main_dir="/scratch/mondego/local/farima/new_oreo/recall_related/recall_dataset"
        # main_dir="D:\\PhD\\Clone\\MlCC-New\\SourcererCC\\test_input"
        if(type_input=="z"):
            subdirs=[]
            for root, dirs, files in os.walk(main_dir):
                for file in files:
                    print(os.path.join(root, file))
                    if (zipfile.is_zipfile(os.path.join(root, file))):
                     subdirs.append(os.path.join(root, file))
        elif (type_input=="d"):
            subdirs = [f.path for f in os.scandir(main_dir) if f.is_dir()]
        num_dir_per_process=len(subdirs)//num_process
        num_last_file=num_dir_per_process+(len(subdirs)%num_process)

        outpath = sys.argv[4] if len(sys.argv) > 4 else ""
        outputdir = os.path.join(outpath, "output")
        if os.path.exists(outpath):
            shutil.rmtree(outpath)
        os.makedirs(outputdir)
    
        for i in range(num_process):
            file = open(f"{outputdir}/" + str(i + 1) + ".txt", "w")
            numWritten=0
            for j in range((i*num_dir_per_process),len(subdirs)):
                file.write(subdirs[j]+"\n")
                numWritten+=1
                if(numWritten==(num_dir_per_process) and i!=(num_process-1)):
                    break
            file.close()
        for file in os.listdir(f"{outputdir}/"):
            mode="zip"
            if type_input=="z":
                mode="zip"
            elif type_input=="d":
                mode="dir"
            
            # jarpath = os.path.abspath(os.path.join(thispath, "../java-parser/dist/metricCalculator.jar"))
            # command = " java -Xms4g -Xmx4g -jar {jarpath} {filename} {mode}".format(jarpath=jarpath,
            #     filename=f"{outputdir}/"+file,mode=mode)
            
            oldcwd = os.getcwd() if os.getcwd() !=  thispath else None
            try:
                if oldcwd: os.chdir(thispath)

                command = " java -Xms4g -Xmx4g -jar ../java-parser/dist/metricCalculator.jar {filename} {mode}".format(
                    filename=f"{outputdir}/"+file,mode=mode)
                command_params = command.split()
                run_command(
                    command_params, f"{outpath}/metric.out", f"{outpath}/metric.err")
            finally:
                if oldcwd: os.chdir(oldcwd)
