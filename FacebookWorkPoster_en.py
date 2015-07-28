#!/usr/bin/env python
import os
import time
import fb

# You can get a token on https://developers.facebook.com/tools/explorer
TOKEN = 'YourToken'

def read_projects():
    """ Open the project files and return an list with 
    all the projects """
    blacklist = ['//', ':']
    with open('projects.txt', 'r') as f:
        return [line.split(':')[0] for line in f if not line.startswith(blacklist) and line != '']

def print_projects(projects):
    """ Print all the elements in the projects list """
    print()
    for index, project in enumerate(projects):
        print("{0} - {1}".format(n, project))
    print()

def save_progress(project_name, time):
    """ Adds the time the user have worked on the project
    and returns the values needed for sharing with facebook """
    blacklist = ['//', ':']
    with open('projects.txt', 'r+') as f:
        content = f.readlines()
        for index, line in enumerate(content):
            if not line.startswith(blacklist) and project_name in content:
                total_hours = int(content[i].split(':')[1].strip(' ')) + time
                content[i] = "{0}: {1}".format(project_name, total_hours)
                line = i
        f.seek(0)
        f.write('\n'.join(content))
        print("Project '{0}' saved in line {1}. Total hours: {2}".format(project_name, line, total_hours))
        return {'name': project_name, 
                'total': total_hours}

def share_facebook(data):
    """ Share the post on facebook """
    msg = 'I\'ve been working in the {1} project for the last {0} hours.\n I worked {2} hours in this project!'.format(data['hours'], data['name'], data['total'])
    facebook = fb.graph.api(TOKEN)
    facebook.publish(cat = 'feed', id = 'me', message = msg)
    print('\n %' % msg)
    print('     Shared! \n')

def main():
    exit = False
    print("Welcome to Facebook Simple Work Poster")
    print("\nYour projects are:")

    projects = read_projects()

    while not exit:
        print_projects(projects)
        project_selection = raw_input('In with project are you going to work? (number): ')
        project_name = projects[int(project_selection)]

        input = raw_input('Do you want to work on "{0}" ? (Y/n): '.format(project_name)).strip().lower()
        if input == 'y' or input == 'yes':
            print("The counter has started! Get to work now!")
            start_time = time.time()
            while not exit:
                input = raw_input('When you want to stop just write stop (don\'t worry, i won\'t count that time): ').strip().lower()
                if input == 'stop':
                    exit = True
                    elapsed = time.gmtime(time.time() - start_time)
                    elapsed_hours = elapsed.tm_hour
                    elapsed_minutes = elapsed.tm_min
                    if elapsed_minutes >= 30:
                        elapsed_hours += 1
                    print("You have been working in this project {0} hours.".format(elapsed_hours))
                    input = raw_input('Do you want to save your progress? (Y/n): ').strip().lower()
                    if input == 'y' or input == 'yes':
                        facebook_data = save_progress(project_name, elapsed_hours)
                        input = raw_input('Want to share the progress on facebook? (Y/n): ').strip().lower()
                        if input == 'y' or input == 'yes':
                            facebook_data['hours'] = elapsed_hours
                            share_facebook(facebook_data)
                            exit = True
                    elif input == 'n' or input == 'no':
                        print('Ok!')
                        exit = True
                    else:
                        print('Command not valid.')
                else:
                    exit = False
        input = raw_input('Do you want to select another project? (Y/n): ').strip().lower()
        exit = (input == 'n' or input == 'no')
    print("Have a good day!")

if __name__ == '__main__':
    main()