### pipelineUI ###
##------ below is pipeline UI part --------##
#############################################

import maya.cmds as cmds
import functools
import maya.mel as mel
import sys
import re
import pymel.core as pm
import os
import os.path



project_name = "my_pro"#default new project name,should be modified
chosen_dir = ""
dirID = "project_choose"
new_name =""
current_project = "none"
project_path = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"

#folder list to add into new project
add_on_list = ["cache/nCache/fluid","data","images","scenes/edits","renderData/fur/furShadowMap","scripts",
"renderData/shaders","renderData/fur/furFiles","renderData/fur/furEqualMap","movies","autosave","sound",
"Time Editor","renderData/iprImages","sourceimages/3dPaintTextures","cache/particles","sourceimages","clips",
"renderData/fur/furImages","renderData/depth","sceneAssembly","Time Editor/Clip Exports","cache/bifrost",
"renderData/fur/furAttrMap","assets"]

### ----- deleteUI -----###
### this is an extending function to deleteUI() ###
## specify the condition to delete ##
# input: name of window to delete #
###-------------------------------------------------------------##
def myDeleteUI(name,*pargs):
    if cmds.window(name,exists =True):
        cmds.deleteUI(name)
        
        
### ----- create_new ----- ###
## create new project ###
## input : none
## rtype : none
## ------------------------------------------------------------##
def create_new(*pargs):
        global new_name
        name = str(cmds.textField(new_name,query = True,text = True))
        def condition(name):#specify the new project name restriction
            if len(name)<8:
                return True
            return False
        if condition(name):
            cmds.sysFile("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name, md=True)
            pm.mel.setProject("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name)
            for newfolder in add_on_list:
                cmds.sysFile("/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name+"/"+newfolder, md=True)
        #file dialog
            cmds.fileDialog2(dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/"+name,ds = 1,fm=2)
             
            mainUI()
        #block for create good
            while cmds.window("good",exists = True):
                cmds.deleteUI("good")
            cmds.window("good",h=100,w=200)
            cmds.rowColumnLayout(numberOfRows=2)
            cmds.text(label = "your project %s has been chosen as working directory" %(name))
            def deleteWi(*pargs):
                cmds.deleteUI("new")
                cmds.deleteUI("good")
            cmds.button(label ="Ok",command = deleteWi)
            cmds.showWindow("good")
            
        
### ----- newProUI ----- ###
## this prompt a new Project UI ##
## Input : none
## rtype : none
## -----------------------------------------------------##
def newProUI(*parg):
    global chosen_dir,new_name
    if cmds.window("new",exists = True):
        cmds.deleteUI("new")       
    window = cmds.window("new",h=100,w=200)
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,155),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.text(label = "your new project name: ")
    new_name = cmds.textField(text = project_name)
    
    cmds.button(label = "OK",command = create_new)
    cmds.showWindow(window)


### ----- deleteProjectUI ----- ###
## UI for delete project ##
## project_name : str
## rtype : none    
## --------------------------------------------------------##
def deleteProjectUI(project_name, *pargs):
    print "2333"    
    
#browse a file dialog to choose working project (for existPro())  
def wkSpace(*pargs):
    chosen_lst = cmds.fileDialog2(ds = 1,fm = 2,dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/")
    try:     
        while chosen_lst[0].split('/')[:-1] != "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects".split('/'):

            chosen_lst = cmds.fileDialog2(ds = 1,fm = 2,dir = "/Users/ntdstaff/Library/Preferences/Autodesk/maya/2017/projects/")
        pm.mel.setProject(chosen_lst[0])
            
        if cmds.window("prompt", exists = True):
            cmds.deleteUI("prompt")
        cmds.window("prompt")
        cmds.rowColumnLayout( numberOfRows=4 )
        cmds.text(label = "You choose :", al = "left")
        cmds.text(label = chosen_lst[0],al = "center")
        cmds.text(label = "as your working project",al = "right")
        cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
        cmds.separator(h= 10)
        def exit(*parg):
            if cmds.window("exist", exists = True):
                cmds.deleteUI("exist")
            if cmds.window("prompt", exists = True):
                cmds.deleteUI("prompt")
            if cmds.window(dirID, exists = True):
                cmds.deleteUI(dirID)
        cmds.button(label = "Ok",command = exit)
        cmds.showWindow("prompt")  
    except TypeError:
        print "no folder is chosen"
###choose an existing project
def existPro(*pargs):
    global chosen_dir
    
        
    if cmds.window("exist", exists = True):
        cmds.deleteUI("exist")
    cmds.window("exist")
    cmds.rowColumnLayout( numberOfRows=2 )
    cmds.text(label = "Choose your working project")
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.separator(h= 10)
    cmds.button(label = "choose",command = wkSpace)
    cmds.showWindow("exist")

    
        
        
        
### choose a working project, (This is the first and main step)

def browseDir():
    while cmds.window(dirID,exists = True):
                cmds.deleteUI(dirID)
    
    window = cmds.window(dirID, h = 100, w =200)
    cmds.rowColumnLayout( numberOfRows=2 )
    cmds.text(label= "Choose your working project or create a new one")
    cmds.rowColumnLayout(numberOfColumns =3, columnWidth= [(1,75),(2,60),(3,60)], columnOffset = [(1,'right',3)])
    cmds.separator(h= 10)
    cmds.button(label = "choose",command = existPro)
    cmds.button(label = "create",command = newPro)
    

    cmds.showWindow( window)
    
       
#    Create a window with a some fields for entering text.
windowID = 'save'
def saveScene( fileName):
    cmds.file(rename = fileName)
    cmds.file(save=True )
    return 1
###
def myFileBrowser(*pargs):
    global windowID
    multipleFilters = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
    val = cmds.fileDialog2( ff=multipleFilters,ds =2,fm = 0)
    if val:
         print val
         saveScene(val[-1])
         if cmds.window(windowID, exists =True):
             cmds.deleteUI(windowID)



### ------aboutPipeline-----###
# this function gives users infomation about this pipeline #
###  pumped information, click "Close" to close the window  ###
## Input  : none
## rtype : none
###----------------------------------------###
def aboutPipeline(*pargs):
    if cmds.window("about", exists = True):
        cmds.deleteUI("about")
    infoWindow = cmds.window("about", w = 300, h =250)
    cmds.columnLayout(adjustableColumn=True)
    cmds.scrollField(ww=True,w=300,h=200,editable=False,text= "myPipeline\n\nmyPipeline is an open source, free, " +
							"and customizable pipeline in python source for production (in Autodesk Maya)." +
							"\n\nCreated by:\n Siyuan Qiu (4th year undergraduates from University of Toronto) \n "
							)

    cmds.button(label="Close", command=functools.partial(myDeleteUI,"about"))
    cmds.showWindow(infoWindow);



### ------mainUI------###
#mainUI create the main body of this pipeline user interface #
## input : none
## rtype : none
###--------------------------------------------------------------##
def mainUI():
    global current_project
    #this is a list of all projects
    projectList = openProjectData(project_path)
    
    #number of project
    projectNum = len(projectList)
    
    #open mainUI
    if cmds.window("mainUI", exists = True):
        cmds.deleteUI("mainUI")
    
    mainWindow = cmds.window("mainUI",w = 675,h = 450,mxb= 0,rtf =0, menuBar = True, title = "pipelineUI")
    ##
    #menubar
    assetMenuBarLayout = cmds.menuBarLayout(bgc = [0.3,0.3,0.5])
    ##menus
     ## Help
    cmds.menu(label = "Help")
    cmds.menuItem(label = "About pipeline", command = aboutPipeline)
     ## Tools
    cmds.menu(label = "Tools")
    cmds.menuItem(label = "Maya Reference Editor", command = cmds.ReferenceEditor)
    cmds.menuItem(label = "Maya Script Editor", command = cmds.ScriptEditor)
    ## end of menu
    
    
    ### main formlayout
    mainFormLayout = cmds.formLayout(numberOfDivisions = 100,bgc = [0.4,0.3,0.3])
    
    ## project list
    projectSeparator1 = cmds.separator(w = 675,bgc = [0.4,0.3,0.3])
    projectNameTxt  = cmds.text(label = "Project Name:", al = "right", w = 100)
    projectNameMenu = cmds.optionMenu( cc = projectSelected,bgc = [0.9,0.9,0.9])
    cmds.menuItem(label = "none")
    for i in range(projectNum):
            cmds.menuItem(label = projectList[i])
        # Create button
    projectCreateButton = cmds.button(label = "Create",command =  newProUI,h = 30,w =60,bgc = [0.8,0.4,0.4])
        # Delete button
    #print cmds.optionMenu(projectNameMenu)
    #projectDeleteButton = cmds.button(label = "Delete", command = functools.partial(deleteProjectUI, cmds.optionMenu(projectNameMenu,v=True) 
    
    
    ## formlayout
    cmds.formLayout(mainFormLayout,e =True,af =[(projectSeparator1,'top',10),
                                                (projectNameTxt,'left',10)], 
                                                
                                                ac = [(projectNameTxt,'top',10,projectSeparator1),
                                                (projectNameMenu,'top',5,projectSeparator1),
                                                (projectCreateButton,'top',5,projectSeparator1),
                                                (projectNameMenu,'left',5,projectNameTxt),
                                                (projectCreateButton,'left',5,projectNameMenu)])
    
    cmds.showWindow(mainWindow)
    
  
def projectSelected(chosen_item,*pargs):
    global current_project
    current_project = chosen_item
###
mainUI()
