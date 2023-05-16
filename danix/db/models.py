from django.db import models
import uuid
from danixfs import Danix
from datetime import datetime
from settings import SNAPSHOT_LIMIT
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
                print("Environment does not exist!")
                exit(1)
            else:
                if environment.first().status:

                    resp = Danix.navigate(filesystem_name)

                    if resp != 0:
                        print("Error!")
                        exit(1)
                else:
                    print("Error! The environment is spopped!")
                    exit(1)

        except ValidationError as error:
            print("Environment doenst not exist!")
            exit(1)

    @staticmethod
    def rm_environment(filesystem_name):
        try:
            environment = Environment.objects.filter(filesystem_name=filesystem_name)

            if environment.count() == 0:
                print("Environment does not exist!")
                exit(1)
            else:

                Danix.rm(filesystem_name)
                env = environment.first()
                env.delete()
                print(f"Environment removed successfully! - {filesystem_name}")
        except Exception:
            print("Environment does not exist!")
            exit(1)


    @staticmethod
    def start_environment(filesystem_name):

        environment = Environment.objects.filter(filesystem_name=filesystem_name)
        
        if environment.count() == 0:

            print("Environment does not exist!")
            exit(1)
        else:
            env = environment.first()
            env.status = True
            env.save()
            print("Environment started successfully!")
            exit(0)

    @staticmethod
    def set_active(filesystem_name):
        environment = Environment.objects.filter(filesystem_name=filesystem_name).first()

        environment.status = True
        environment.save()
    
    @staticmethod
    def stop_environment(filesystem_name):

        
        environment = Environment.objects.filter(filesystem_name=filesystem_name)

        if environment.count() == 0:
            print("Environment does not exist!")
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
        print("===============================================================================================================================================")
        print("|  ENVIRONMENT NAME  |  TEMPLATE  |       CREATED         |            SUBSYSTEM NAME            |     IMAGE     |      STATUS   |   SIZE     |")
        print("|=============================================================================================================================================|")

        if environments.count() > 0:
            for environment in environments:
                name = str(environment.name)
                status_icon = "🟢 Running" if environment.status else "🔴 Stopped"
                repeat = (11-len(name)) * '.'

                template = str(environment.template)

                repeat_template = (6-len(template)) * ' '

                size = Danix.get_size(environment.filesystem_name, None)
                print(f"|  {name[0:11]}{repeat}           {template}{repeat_template}          {environment.created}         {environment.filesystem_name}        Alpine        {status_icon}      {size}B   |")

        print("===============================================================================================================================================")


    class Meta:
        db_table = "environment"

class Snapshot(models.Model):

    snapshot_name  = models.UUIDField()
    environment_id = models.ForeignKey(Environment, null=True, on_delete=models.SET_NULL)
    created        = models.DateField(default=datetime.now())
    last           = models.BooleanField(default=True)
    
    @staticmethod
    def rm_snapshot(snapshot_name):
        try:
            snapshot = Snapshot.objects.filter(snapshot_name=snapshot_name)

            if snapshot.count() > 0:

                resp = Danix.remove_snapshot(snapshot_name)
                
                if resp == 0:
                    Snapshot.objects.get(snapshot_name=snapshot_name).delete()

                    print(f"Snapshot removed successfully - {snapshot_name}")
                else:
                    print("Error: Snapshot can not remove")
                    exit(1)
            else:
                print("Snapshot does not exist!")
                exit(1)

        except ValidationError:
            print("Snapshot does not exist!")
            exit(1)

    @staticmethod
    def back_snapshot(snapshot_name):
        try:
            snapshot = Snapshot.objects.filter(snapshot_name=snapshot_name)

            if snapshot.count() > 0:
                filesystem_name = Environment.objects.filter(id=snapshot.first().environment_id.id).first().filesystem_name

                resp = Danix.back_snapshot(filesystem_name, snapshot_name)

                if resp == 0:
                    print("Snapshot backed successfully")
                    exit(0)
                else:
                    print("Error: Snapshot can not back")
                    exit(1)
            else:
                print("Snapshot does not exist!")
                exit(1)
        except ValidationError:

            print("Snapshot does not exist!")
            exit(1)

    @staticmethod
    def create(subsystem_name):
        try:
            environment = Environment.objects.get(filesystem_name=subsystem_name)
           
            environment_id = environment.id
            snapshots      = Snapshot.objects.filter(environment_id=environment_id)

            if snapshots.count() >= int(SNAPSHOT_LIMIT):
                print("Snapshot limit exceeded! Please remove 1 snapshot to continue")
                exit(1)
            else:

                for snapshot in snapshots:

                    snapshot.last = False
                    snapshot.save()

                snapshot_name = uuid.uuid4()

                print('Wait a minute! Taking snapshot')
                snapshot = Snapshot.objects.create(snapshot_name=snapshot_name,environment_id=environment).save()
                resp = Danix.make_snapshot(subsystem_name, snapshot_name)

                if resp == 0:
                    print("Snapshot created successfully")
                    print(f"Snapshot name {snapshot_name}\n")
                    print(f"======================================")
                    print(f"Environment size: {Danix.get_size(subsystem_name, None)}B")
                    print(f"Snapshot size:    {Danix.get_size(subsystem_name, snapshot_name)}B")
                    print(f"======================================")
                    exit(0)
                else:

                    Snapshot.objects.get(snapshot_name=snapshot_name,environment_id=environment).delete()
                    print("Snapshot create error!")
                    exit(1)

        except Exception:
            print("Snapshot create error: Environment does not exist!")
            exit(1)

    @staticmethod
    def list_snapshots():

        snapshots = Snapshot.objects.all()

        print("===========================================================================================================================================")
        print("|            SNAPSHOT NAME             |          ENVIRONMENT NAME            |         CREATED       |     LAST SNAPSHOT     |    SIZE    |")
        print("|==========================================================================================================================================|")

        if snapshots.count() > 0:
            for snapshot in snapshots:

                name = str(snapshot.snapshot_name)
                lastsnapshot_icon = "🟢 Yes" if snapshot.last else "🟠 No "

                if snapshot.environment_id:
                    
                    
                    environment_name = Environment.objects.filter(id=snapshot.environment_id.id).first().filesystem_name
                    size = Danix.get_size(environment_name, name)
                else:
                    repeated = 14*' '
                    environment_name = f'Environment Removed 🔴{repeated}'
                    size = "---"
                
                print(f"| {name}     {environment_name}         {snapshot.created}              {lastsnapshot_icon}              {size}B   |")
        print("===========================================================================================================================================")

    class Meta:
        db_table = "snapshot"
# Create your models here.