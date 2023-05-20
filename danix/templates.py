import uuid, app
from db.models import Environment
from danixfs import Danix
from utils import check_equal_sentence
class Essentials():

    packages = ["build-base", "vim","emacs","nano", "micro", "git"]
       

class Template():

    @staticmethod
    def install(packages, environment_name, config_commands, template):

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
            Danix.build_environment(joined_packages, config_commands, filesystem_name)


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

        try:

            for pos in packages_selected.split(" "):
                list_selected_packages.append(packages[int(pos)-1])

        except Exception:
            
            print("🔴 Invalid option: Please select a valid menu option!\n")
            Template.languange_menu(packages)

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

        try:

            for pos in essentials_packages_selected.split(" "):
                list_essentials_packages.append(essentials_packages[int(pos)-1])

        except Exception:
            print("🔴 Invalid option: Please select a valid menu option!\n")
            Template.essentials_menu()

        return list_essentials_packages
                
    @staticmethod
    def menu(packages):
        return Template.essentials_menu() + Template.languange_menu(packages)

class Languanges():
    class Python():

        packages = ["python3 py3-pip", "python3"]
        config_commands = []

        def install(self, environment_name, template):

            Template.install(self.packages, environment_name, self.config_commands, template)
            
    class CLike():

        packages = ["gcc", "g++", "clang", "rust cargo"]
        config_commands = []

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, self.config_commands, template)

    class Java():

        packages = ["openjdk8", "openjdk11", "openjdk17"]
        config_commands = []

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, self.config_commands,template)

    class Ruby():
        packages = ["ruby", "ruby-full"]
        config_commands = []

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, self.config_commands, template)


    class Lua():
        
        packages = ["lua5.4", "lua5.3", "lua5.2"]
        config_commands = []

        def install(self, environment_name, template):

            Template.install(self.packages, environment_name, self.config_commands, template)

    class Ada():

        packages = ["gcc gcc-gnat", "gcc", "gcc-gnat"]
        config_commands = []

        def install(self, environment_name, template):

            Template.install(self.packages, environment_name, self.config_commands, template)


    class Dotnet():

        package = ["dotnet7-sdk", "dotnet6-sdk"]
        config_commands = [
                            "apk add bash icu-libs krb5-libs libgcc libintl libssl1.1 libstdc++ zlib",
                            "export HOME=/home/"
                            "export USERPROFILE=root",
                           ]

        def install(self, environment_name, template):

            Template.install(self.package, environment_name,self.config_commands, template)    

    class Go():

        packages = ["go", "musl-dev go"]
        config_commands = []

        config_commands = [
            "export GOPATH=/root/go >/dev/null 2>&1",
            "export PATH=${GOPATH}/bin:/usr/local/go/bin:$PATH >/dev/null 2>&1",
            "export GOBIN=$GOROOT/bin >/dev/null 2>&1",
            "mkdir -p ${GOPATH}/src ${GOPATH}/bin >/dev/null 2>&1",
            "export GO111MODULE=on >/dev/null 2>&1",
            "export GOCACHE=/root/go/cache >/dev/null 2>&1"
        ]

        def install(self, environment_name, template):
            Template.install(self.packages, environment_name, self.config_commands, template)
        
