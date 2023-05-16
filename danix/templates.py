import uuid, app
from db.models import Environment
from danixfs import Danix

class Essentials():

    packages = ["vim", "nano", "micro", "git"]
       
class Languanges():

    class Python():

        packages = ["python3", "py3-pip"]

        def install(self, environment_name, template):

            packages = input("")
            filesystem_name = uuid.uuid4()

            environment_count = Environment.objects.filter(filesystem_name=filesystem_name).count()

            if environment_count == 0:
                Environment.objects.create(filesystem_name=filesystem_name, template=template, name=environment_name).save()

                joined_packages = self.packages + Essentials().packages

                Environment.set_active(filesystem_name)
                Danix.build_environment(joined_packages, filesystem_name)
            
    class CLike():

        packages = ["gcc", "g++", "clang", "rust cargo"]

        def select_packages(self):

            essentials_packages = Essentials().packages

            i = 1

            for essential in essentials_packages:
                
                print(f'[{i}] - Package {essential}')
                i += 1

            print('Select essentials packages:')
            print('Example: 1 2 3 to install vim, nano, and git')
            essentials_packages_selected = input()

            list_essentials_packages = []

            for pos in essentials_packages_selected.split(" "):
                list_essentials_packages.append(essentials_packages[int(pos)-1])

            i = 1

            for package in self.packages:
                print(f"[{i}] - Package {package}")
                i += 1

            print('Select essentials packages:')
            print('Example: 1 2 to install gcc, g++')
            clike_packages_selected = input()

            list_clike_packages = []

            for pos in clike_packages_selected.split(" "):
                list_clike_packages.append(self.packages[int(pos)-1])

            return list_essentials_packages + list_clike_packages
        
        

        def install(self, environment_name, template):
            filesystem_name = uuid.uuid4()

            environment_count = Environment.objects.filter(filesystem_name=filesystem_name).count()

            if environment_count == 0:
                
                Environment.objects.create(filesystem_name=filesystem_name, template=template, name=environment_name).save()
                
                joined_packages = self.select_packages()

                Environment.set_active(filesystem_name)
                Danix.build_environment(joined_packages, filesystem_name)

    class Java():

        packages = ["openjdk8", "openjdk11", "openjdk17"]

        def install(self, environment_name, template):
            filesystem_name = uuid.uuid4()

            environment_count = Environment.objects.filter(filesystem_name=filesystem_name).count()

            if environment_count == 0:

                Environment.objects.create(filesystem_name=filesystem_name, template=template, name=environment_name).save()

                joined_packages = self.packages + Essentials().packages

                Environment.set_active(filesystem_name)
                Danix.build_environment(joined_packages, filesystem_name)