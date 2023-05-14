import uuid, app
from db.models import Environment
from danixfs import Danix

class Essentials():

    packages = ["fish", "vim", "nano", "micro", "git"]
       
class Languanges():

    class Python():

        packages = ["python3", "py3-pip"]

        def install(self, environment_name, template):
            filesystem_name = uuid.uuid4()

            environment_count = Environment.objects.filter(filesystem_name=filesystem_name).count()

            if environment_count == 0:
                Environment.objects.create(filesystem_name=filesystem_name, template=template, name=environment_name).save()

                joined_packages = self.packages + Essentials().packages

                Environment.set_active(filesystem_name)
                Danix.build_environment(joined_packages, filesystem_name)
            
    class CLike():

        packages = ["gcc", "g++", "clang", "rust cargo"]

        def install(self, environment_name, template):
            filesystem_name = uuid.uuid4()

            environment_count = Environment.objects.filter(filesystem_name=filesystem_name).count()

            if environment_count == 0:
                
                Environment.objects.create(filesystem_name=filesystem_name, template=template, name=environment_name).save()
                
                joined_packages = self.packages + Essentials().packages

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