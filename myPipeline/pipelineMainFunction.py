### pipelineMainFunction ###
import os
import os.path
import maya.cmds as cmds

### ----- openProjectData ------###
## this function return a list of projects used pipeline ##
## input: None
## rtype: List<String>
## Author : Qiu Siyuan
## ------------------------------------------------------------##
def openProjectData(project_path):
    projects_list = []
    for df in os.listdir(project_path):
        if os.path.isdir(project_path+df):
            projects_list.append(df)
    return projects_list

### ----- delete_project ----- ###
## delete project that given by name under projects folder ##
## input project_path : str
## input project_name : str
## rtypr : none
## Author : Qiu Siyuan
## ---------------------------------------------------------- ##
def delete_project(project_path, project_name, *pargs):
    for root, dirs, files in os.walk(project_path + project_name, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
            
### ----- save_selected ----- ###
## save currently selected item with given name in the folder(category) user choose ##
## input item_name : str
## input folder_path : str
## rtype : none
## Author : Qiu Siyuan
## -------------------------------------------------------------- ##
def save_selected( item_name,folder_path):
    cmds.file(folder_path+'/'+item_name, exportSelected = True,type = "mayaBinary")

### ----- save_scene ------ ###
## save the whole scene to the folder user choose ##
## input scene_name : str
## input folder_path : str
## rtype : none
## Author : Qiu Siyuan
## ----------------------------------------------------------------- ##
def save_scene(scene_name, folder_path):
    cmds.file(rename = folder_path + '/'+ scene_name)
    cmds.file(save = True, type = "mayaBinary")
    
##
    
