#!/usr/bin/env python3
import os
import sh

def create_project_from_git(git, projects_folder):
    clone = os.system('git clone ' + git + ' ' + projects_folder)
    return clone

# git = sh.git.bake(_cwd='/home/deepdark/projects/gdeles')
# print(git.status())
# # checkout and track a remote branch
# print(git.checkout('-b', 'somebranch'))
# # add a file
# print(git.add('somefile'))
# # commit
# print(git.commit(m='my commit message'))
# # now we are one commit ahead
# print(git.status())