import uuid, app
from db.models import Environment
from danixfs import Danix
from utils import check_equal_sentence
class Essentials():

    packages = ["build-base", "vim", "nano", "micro", "git"]
       

class Template():

    @staticmethod
    def install(packages, environment_name, template):

        filesystem_name = uuid.uuid4()

        environment_count = Environment.objects.filter(
                                    filesystem_name=filesystem_name
                            ).count()

        if check_equal_sentence(environment_count, 0):

            Environment.objects.create(
                    filesystem_name=filesystem_name, 
                    template=template, 
                    name=environment_name).save()

            joined_packages = Template.menu(packages)

            Environment.set_active(filesystem_name)
            Danix.build_environment(joined_packages, filesystem_name)



    @staticmethod
    def languange_menu(packages):
        i = 1

        for package in packages:
            print(f"[{i}] - Package {package}")
            i += 1

        print('Select essentials packages:')
        print(f'Example: 1 2 to install {packages[0]}, {packages[1]}')
        packages_selected = input()

        list_selected_packages = []

        for pos in packages_selected.split(" "):
            list_selected_packages.append(packages[int(pos)-1])

        return list_selected_packages


    @staticmethod
    def essentials_menu():
        essentials_packages = Essentials().packages

        i = 1

        for essential in essentials_packages:
            
            print(f'[{i}] - Package {essential}')
            i += 1

        print('Select essentials packages:')
        print(f'Example: 1 2 3 to install {essentials_packages[0]}, {essentials_packages[1]}, and {essentials_packages[2]}')
        essentials_packages_selected = input()

        list_essentials_packages = []

        for pos in essentials_packages_selected.split(" "):
            list_essentials_packages.append(essentials_packages[int(pos)-1])

        return list_essentials_packages
                
    @staticmethod
    def menu(packages):
        return Template.essentials_menu() + Template.languange_menu(packages)

class Languanges():
    class Python():

        packages = ["python3", "py3-pip"]

        def install(self, environment_name, template):

            Template.install(self.packages, environment_name, template)
            
    class CLike():

        packages = ["gcc", "g++", "clang", "rust cargo"]

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, template)

    class Java():

        packages = ["openjdk8", "openjdk11", "openjdk17"]

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, template)