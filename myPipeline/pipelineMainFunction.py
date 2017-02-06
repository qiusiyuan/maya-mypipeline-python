### pipelineMainFunction ###
import os
import os.path

### ----- openProjectData ------###
## this function return a list of projects used pipeline ##
## Input: None
## rtype: List<String>
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
def delete_project(project_path, project_name, *pargs):
    for root, dirs, files in os.walk(project_path + project_name, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))