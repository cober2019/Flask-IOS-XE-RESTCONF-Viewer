import os, subprocess
import json
import time
import xml.dom.minidom


yang_dir = None

def get_yang():
	
	global yang_dir

	files = []
	yang_dir = os.path.dirname(os.path.realpath(__file__)) + '/yangfiles'
	for yang_file in os.listdir(yang_dir):
		if yang_file.endswith(".yang"):
			files.append(yang_file)

	return files


def get_standard_tree(model):
	
	
	get_model = subprocess.run(["pyang", "-f", "tree", f"{yang_dir}/{model}"], capture_output=True)
	model_stdout = str(get_model.stdout, 'utf-8')
	
	return model_stdout


def get_dynamic_tree(model):

    os.chdir("/IOS-XE-RESTCONF-Viewer/app/Modules/yangfiles/")
    process = subprocess.Popen(['pyang', '-f', 'jstree',  '-o', '/IOS-XE-RESTCONF-Viewer/app/home/templates/jstree.html' , f'{model}'], shell=False)

    while process.poll() is None:
        time.sleep(1)

    return process.poll()


def get_yin(model):

    os.chdir("/IOS-XE-RESTCONF-Viewer/app/Modules/yangfiles/")
    process = subprocess.Popen(['pyang', '-f', 'yin',  '-o', 'yin.xml' , f'{model}'], shell=False)

    while process.poll() is None:
        time.sleep(1)
    
    yin_file = open('yin.xml')
        
    return yin_file.read()
