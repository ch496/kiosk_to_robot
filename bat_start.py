import os
import bat_start_files

workingDir = bat_start_files.bat_start_files.workingDir

def run_ROBOT_ON(executeFir_BUTTON_ROBOT_ON):
    # working Directory
    os.chdir(workingDir)
    # File Run
    os.system(executeFir_BUTTON_ROBOT_ON)

def run_ONE_EXECUTION(executeFir_BUTTON_ONE_EXECUTION):
    # working Directory
    os.chdir(workingDir)
    # File Run
    os.system(executeFir_BUTTON_ONE_EXECUTION)

def run_TWO_EXECUTION(executeFir_BUTTON_TWO_EXECUTION):
    # working Directory
    os.chdir(workingDir)
    # File Run
    os.system(executeFir_BUTTON_TWO_EXECUTION)

def run_ONE_HUNDRED_EXECUTION(executeFir_BUTTON_ONE_HUNDED_EXECUTION):
    # working Directory
    os.chdir(workingDir)
    # File Run
    os.system(executeFir_BUTTON_ONE_HUNDED_EXECUTION)