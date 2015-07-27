import os
import time
import fb

# Podes conseguir un token en https://developers.facebook.com/tools/explorer
TOKEN = 'TuToken'


def read_projects():
    """ Abre el archivo projects.txt y devuelve un array
    con todos los proyectos. """
    out = []
    with open('projects.txt', 'r') as f:
        for line in f:
            # Si la linea no está comentada...
            if line[0:2] != '//': 
                # ...agregamos el nombre a la lista.
                name = line.split(':')[0]
                if line and name:
                    out.append(name)
    return out

def print_projects(projects):
    """ Imprime todos los elementos en el array de proyectos """
    print()
    for n in range(len(projects)):
        print("{0} - {1}".format(n, projects[n]))
    print()

def save_progress(project_name, time):
    """ Calcula el tiempo que el usuario trabajo en el proyecto,
    lo guarda en el archivo 'projects.txt' y devuelve los datos 
    necesarios para compartir en facebook """
    with open('projects.txt', 'r+') as f:
        content = f.read()
        content = content.split('\n')
        for i in range(len(content)):
            if project_name in content[i]:
                total_hours = int(content[i].split(':')[1].strip(' ')) + int(time)
                content[i] = "{0}: {1}".format(project_name, total_hours)
                line = i
        f.seek(0)
        f.write('\n'.join(content))
        print("Poyecto '{0}' guardado en la linea {1}. Horas totales: {2}".format(project_name, line, total_hours))
        return {'name': project_name, 
                'total': total_hours}

def share_facebook(data):
    """ Comparte el post en facebook """
    msg = 'Estube las ultimas {0} horas trabajando en el proyecto {1}.\n Llevo {2} horas trabajadas en este proyecto.'.format(data['hours'], data['name'], data['total'])
    facebook = fb.graph.api(TOKEN)
    facebook.publish(cat = 'feed', id = 'me', message = msg)
    facebook = None # Close facebook
    print('\n %' % msg)
    print('     Compartido! \n')

def main():
    exit = False
    print("Bienvenido a Facebook Simple Work Poster")
    print("\nTus proyectos son:")

    projects = read_projects()

    while not exit:
        print_projects(projects)
        project_selection = raw_input('En que proyecto vas a trabajar? (numero): ')
        project_name = projects[int(project_selection)]

        input = raw_input('Queres trabajar en "{0}" ? (Y/n): '.format(project_name)).strip().lower()
        if input == 'y' or input == 'yes':
            print("El contador acaba de empezar. A trabajar!")
            start_time = time.time()
            while not exit:
                input = raw_input('Cuando quieras parar escribí "stop" (no te preocupes, no voy a contar ese tiempo): ').strip().lower()
                if input == 'stop':
                    exit = True
                    elapsed_hours = int(time.strftime('%H', time.gmtime(time.time() - start_time)))
                    elapsed_minutes = int(time.strftime('%M', time.gmtime(time.time() - start_time)))
                    if elapsed_minutes >= 30:
                        elapsed_hours += 1
                    print("Estubiste {0} horas trabajando en este proyecto.".format(elapsed_hours))
                    input = raw_input('Queres salvar tu progreso? (Y/n): ').strip().lower()
                    if input == 'y' or input == 'yes':
                        facebook_data = save_progress(project_name, elapsed_hours)
                        input = raw_input('Queres compartir tu progreso en Facebook? (Y/n): ').strip().lower()
                        if input == 'y' or input == 'yes':
                            facebook_data['hours'] = elapsed_hours
                            share_facebook(facebook_data)
                            exit = True
                    elif input == 'n' or input == 'no':
                        print('Ok!')
                        exit = True
                    else:
                        print('Comando invalido.')
                else:
                    exit = False
        input = raw_input('Queres trabajar en otro proyecto? (Y/n): ').strip().lower()
        if input == 'n' or input == 'no':
            exit = True
        else:
            exit = False
    print("Nos vemos!")

if __name__ == '__main__':
    main()