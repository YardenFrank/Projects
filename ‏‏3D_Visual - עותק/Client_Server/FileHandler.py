from os import listdir, path, remove, rename


class FileHandler:
    def __init__(self, project_folder):
        self.project_folder = project_folder
        self.objects_folder = project_folder + 'Objects\\'
        self.assets_folder = project_folder + 'Assets\\'
        self.requests_path = project_folder + 'Requests.txt'
        self.positions_path = project_folder + 'Positions.txt'
        open(self.requests_path, 'w').close()

    def set_object(self, object_number, data):
        vertices, faces = data
        file_path = f'{self.objects_folder}object {object_number}.obj'

        with open(file_path, 'w') as object_file:
            for vertex in vertices:
                vertex = [str(value) for value in vertex]
                object_file.write(f'v {" ".join(vertex[:-1])}\n')
            for face in faces:
                face = [str(value + 1) for value in face]
                object_file.write(f'f {" ".join(face)}\n')

        with open(self.positions_path, 'a') as file:
            file.write('\n')

    def get_object(self, object_number=None, object_name=None):
        if object_number:
            file_path = self.objects_folder
            name = f'object {object_number}.obj'
        else:
            file_path = self.assets_folder
            name = object_name + '.obj'
        return self.retrieve_object(file_path + name)

    @staticmethod
    def retrieve_object(file_path):
        try:
            vertices, faces = [], []
            with open(file_path, 'r') as object_file:
                for line in object_file:
                    if line.startswith('v'):
                        vertices.append([float(i) for i in line.split()[1:]] + [1])
                    elif line.startswith('f'):
                        faces_ = line.split()[1:]
                        faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
            return vertices, faces
        except FileNotFoundError:
            return None

    def add_new_line(self):
        with open(self.requests_path, 'a') as requests_file:
            requests_file.write('\n ')

    def write_line_to_file(self, data, index, request=True):
        if request:
            file_path = self.requests_path
        else:
            file_path = self.positions_path

        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines[index] = ' '.join(str(element) for element in data) + '\n'
        with open(file_path, 'w') as file:
            file.writelines(lines)

    def get_request(self, index):
        with open(self.requests_path, 'r') as requests_file:
            lines = requests_file.readlines()
            request = list(lines[index].split(' '))
        return request

    def get_position(self, object_num):
        with open(self.positions_path, 'r') as positions_file:
            lines = positions_file.readlines()
            if object_num < len(lines):
                pos = list(lines[object_num].split())
                pos = [float(value) for value in pos]
                return pos
            return [0, 0, 0]

    def get_number_of_objects(self):
        return len(listdir(self.objects_folder))

    def erase_object(self, object_num):
        file_path = f'{self.objects_folder}object {object_num}.obj'
        if path.exists(file_path):
            remove(file_path)

        number_of_objects = self.get_number_of_objects() + 1
        object_num += 1
        while object_num <= number_of_objects:
            file_path = f'{self.objects_folder}object {object_num}.obj'
            if path.exists(file_path):
                rename(file_path, f'{self.objects_folder}object {object_num - 1}.obj')
            object_num += 1

        with open(self.positions_path, 'r') as pos_file:
            lines = pos_file.readlines()
            lines.pop(object_num - 1)
        with open(self.positions_path, 'w') as pos_file:
            pos_file.writelines(lines)
