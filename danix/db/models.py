from django.db import models
from danixfs import Danix
from datetime import datetime
from django.core.exceptions import ValidationError


class Environment(models.Model):
    filesystem_name = models.UUIDField()
    status         = models.BooleanField(default=True)
    name           = models.TextField()
    created        = models.DateField(default=datetime.now())
    template       = models.TextField(default="")

    @staticmethod
    def navigate(filesystem_name):

        try:
            environment = Environment.objects.filter(filesystem_name=filesystem_name)

            if environment.count() == 0:
                print("Environment doenst exist!")
                exit(1)
            else:
                resp = Danix.navigate(filesystem_name)

                if resp != 0:
                    print("Error!")
                    exit(1)
        except ValidationError as error:
            print("Environment doenst exist!")
            exit(1)

    @staticmethod
    def rm_environment(filesystem_name):

        environment = Environment.objects.filter(filesystem_name=filesystem_name)

        if environment.count() == 0:
            print("Environment doesnt exist!")
            exit(1)
        else:

            Danix.rm(filesystem_name)
            env = environment.first()
            env.delete()
            print("Environment removed successfully!")
            exit(0)


    @staticmethod
    def start_environment(filesystem_name):

        environment = Environment.objects.filter(filesystem_name=filesystem_name)
        
        if environment.count() == 0:

            print("Environment doesnt exist!")
            exit(1)
        else:
            resp = Danix.start(filesystem_name)
            if resp == 0:
                env = environment.first()
                env.status = True
                env.save()
                print("Environment started successfully!")
                exit(0)
            else:
                print("Starting error!")
                exit(1)

    @staticmethod
    def set_active(filesystem_name):
        environment = Environment.objects.filter(filesystem_name=filesystem_name).first()

        environment.status = True
        environment.save()
    
    @staticmethod
    def stop_environment(filesystem_name):

        resp = Danix.stop(filesystem_name)

        if resp == 0:
            environment = Environment.objects.filter(filesystem_name=filesystem_name)

            if environment.count() == 0:
                print("Environment doesnt exist!")
                exit(1)
            else:
                env = environment.first()

                env.status = False
                env.save()

                print("Environment stopped successfully!")
                exit(0)

    @staticmethod
    def list_environments():

        environments = Environment.objects.all()
        print("==================================================================================================================================")
        print("ENVIRONMENT NAME  |  TEMPLATE  |       CREATED         |            CONTAINER NAME            |     IMAGE     |      STATUS")
        print("==================================================================================================================================")

        if environments.count() > 0:
            for environment in environments:
                name = str(environment.name)
                status_icon = "🟢 Running" if environment.status else "🔴 Stopped"
                repeat = (11-len(name)) * '.'

                template = str(environment.template)

                repeat_template = (6-len(template)) * ' '

                print(f"{name[0:11]}{repeat}           {template}{repeat_template}          {environment.created}         {environment.filesystem_name}       Alpine        {status_icon}")

        print("==================================================================================================================================")


    class Meta:
        db_table = "environment"
# Create your models here.