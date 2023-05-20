from django.db import models
from django.db.models import Q
import uuid
import settings
from danixfs import Danix
from datetime import datetime
from settings import SNAPSHOT_LIMIT
from utils import separate, get_size_in_mb_or_gb, print_snapshot_list_header, print_footer, print_environment_list_header, is_unique_database_tuple, get_message, check_equal_sentence, check_not_equal_sentence
from django.core.exceptions import ValidationError

def get_queryset_filtered(model, sub_attribute):
    
    if model == Environment:
        return model.objects.filter(filesystem_name__startswith=sub_attribute)
    
    return model.objects.filter(snapshot_name__startswith=sub_attribute)

class Environment(models.Model):
    filesystem_name = models.UUIDField()
    status          = models.BooleanField(default=True)
    name            = models.TextField()
    created         = models.DateField(default=datetime.now())
    template        = models.TextField(default="")
    

    @staticmethod
    def copy(path):

        environent_is_first , environment_uuid, environment_dir, host_directory = separate(path)

        if environment_uuid and environment_dir and host_directory:
            
            environment = get_queryset_filtered(Environment, environment_uuid)
            filesystem_name = environment.first().filesystem_name

            resp = Danix.copy(
                                environent_is_first, 
                                filesystem_name, 
                                environment_dir, 
                                host_directory
                            )

            if check_equal_sentence(resp, 0):
                get_message("🟢 Elements copied successfuly!", True, 0)        
            else:
                get_message("🔴 Copy error!", True, 1)
        else:
            if environent_is_first:
                get_message(f"🔴 Syntax error or element exist in {host_directory}!", True, 1)
            else:
                get_message(f"🔴 Syntax error or path not exist in subsystem!", True, 1)
    
    @staticmethod
    def navigate(filesystem_name):

        try:
            environment = get_queryset_filtered(Environment, filesystem_name)
            environments_count = environment.count()
            environment_first = environment.first()

            if check_equal_sentence(environments_count, 0):

                get_message(message=settings.ENV_NOT_FOUND, is_finishprogram=True, finish_status_code=1)
  
            expression = is_unique_database_tuple(environment) and environment_first.status
            
            if is_unique_database_tuple(environment) and environment_first.status:
                resp = Danix.navigate(environment_first.filesystem_name)
                
                if not check_not_equal_sentence(resp, 0):
                    
                    get_message(
                                    message=f"🔴 {settings.ENV_GENERIC_ERROR}", 
                                    is_finishprogram=True, 
                                    finish_status_code=1
                                )
        
            elif expression ^ (not environment_first.status):

                get_message(
                                message=f"🔴 {settings.ENV_STOPPED_ERROR}",
                                is_finishprogram=True, 
                                finish_status_code=1
                            )   

            else:
                get_message(
                                message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                                is_finishprogram=True, 
                                finish_status_code=1
                            )  
                
        except ValidationError:
            get_message(
                            message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        )  
       
        
    @staticmethod
    def rm_environment(filesystem_name):

        try:
            environment = get_queryset_filtered(Environment, filesystem_name)

            if is_unique_database_tuple(environment):

                environment_count = environment.count()
                environment =  environment.first()

                if check_equal_sentence(environment_count, 0):

                    get_message(
                                    message=f"🔴 {settings.ENV_NOT_FOUND}", 
                                    is_finishprogram=True, 
                                    finish_status_code=1
                                )  

                Danix.rm(environment.filesystem_name)
                environment.delete()

                get_message(
                                message=f"🟢 {settings.ENV_REMOVED} - {environment.filesystem_name}", 
                                is_finishprogram=False, 
                                finish_status_code=-1
                            ) 
            else:

                get_message(
                            message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        )  
                
        except Exception:
            get_message(
                            message=f"🔴 {settings.ENV_NOT_FOUND}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        ) 


    @staticmethod
    def start_environment(filesystem_name):

        environment = get_queryset_filtered(Environment, filesystem_name)

        if is_unique_database_tuple(environment):
            
            environment_counter = environment.count()
            environment = environment.first()

            if check_equal_sentence(environment_counter, 0):

                get_message(
                                message=f"🔴 {settings.ENV_NOT_FOUND}", 
                                is_finishprogram=True, 
                                finish_status_code=1
                            ) 

            environment.status = True
            environment.save()

            get_message(
                            message=f"🟢 {settings.ENV_STARTED}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        ) 
        else:
            get_message(
                            message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        )  
    @staticmethod
    def set_active(filesystem_name):

        environment = Environment.objects.filter(filesystem_name=filesystem_name).first()
        environment.status = True
        environment.save()
    
    @staticmethod
    def stop_environment(filesystem_name):
 
        environment = get_queryset_filtered(Environment, filesystem_name)
        
        if is_unique_database_tuple(environment):

            environment_counter = environment.count()
            environment = environment.first()

            if check_equal_sentence(environment_counter, 0):

                 get_message(message=f"🔴 {settings.ENV_NOT_FOUND}", is_finishprogram=True, finish_status_code=1) 

            environment.status = False
            environment.save()

            get_message(message=f"🟢 {settings.ENV_STOPPED}", is_finishprogram=True, finish_status_code=1) 

        else:
            get_message(
                            message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        )  
            
    @staticmethod
    def list_environments():

        environments = Environment.objects.all()
        environment_counter = environments.count()

        print_environment_list_header()

        if environment_counter > 0:

            for environment in environments:

                name = str(environment.name)

                status_icon = "🟢 Running" if environment.status else "🔴 Stopped"
                template = str(environment.template)

                size_str = str(Danix.get_size(environment.filesystem_name, None))

                size_str = get_size_in_mb_or_gb(size_str)
                
                print(f"|  {name[0:11]}{(11-len(name)) * '.'}           {template}{(6-len(template)) * ' '}          {environment.created}         {environment.filesystem_name}        Alpine        {status_icon}      {size_str}    |")

        print_footer()


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
            snapshot = get_queryset_filtered(Snapshot, snapshot_name)
            
            if is_unique_database_tuple(snapshot):

                snapshot_counter = snapshot.count()

                if snapshot_counter > 0:
                    
                    snapshot = snapshot.first()
                    resp = Danix.remove_snapshot(snapshot.snapshot_name)

                    if check_equal_sentence(resp, 0):
                        
                        Snapshot.objects.get(snapshot_name=snapshot.snapshot_name).delete()

                        get_message(
                                message=f"🟢 Snapshot removed successfully - {snapshot.snapshot_name}", 
                                is_finishprogram=False, 
                                finish_status_code=-1
                            )
                         
                    
                    else:
                        get_message(message="🔴 Error: Snapshot can not remove", is_finishprogram=True, finish_status_code=1) 
                else:
                    get_message(message="🔴 Snapshot does not exist!", is_finishprogram=True, finish_status_code=1) 
            
            else:
                get_message(
                            message=f"🔴 {settings.ENV_PATTERN_ERROR}", 
                            is_finishprogram=True, 
                            finish_status_code=1
                        ) 
                 
        except ValidationError:
            get_message(message="🔴 Snapshot does not exist!", is_finishprogram=True, finish_status_code=1)

    @staticmethod
    def back_snapshot(snapshot_name):
        try:
            snapshot = get_queryset_filtered(Snapshot, snapshot_name)
            snapshot_counter = snapshot.count()
            
            snapshot = snapshot.first()

            if snapshot_counter > 0:
                
                if snapshot.environment_id:
                    filesystem_name = Environment.objects.filter(id=snapshot.environment_id.id).first().filesystem_name

                    resp = Danix.back_snapshot(filesystem_name, snapshot.snapshot_name)

                    if check_equal_sentence(resp, 0):
                        get_message(message="🟢 Environment roll back successfully!", is_finishprogram=True, finish_status_code=0)
                    get_message(message="🔴 Error: Snapshot can not back", is_finishprogram=True, finish_status_code=1)

                get_message(message="🔴 Error: Environment was removed!", is_finishprogram=True, finish_status_code=1)

            get_message(message="🔴 Snapshot does not exist!", is_finishprogram=True, finish_status_code=1)

        except ValidationError:
            
            get_message(message="🔴 Snapshot does not exist!", is_finishprogram=True, finish_status_code=1)

    @staticmethod
    def create(subsystem_name):

        try:

            environment = get_queryset_filtered(Environment, subsystem_name)

            if is_unique_database_tuple(environment):

                environment = environment.first()

                environment_id = environment.id
                snapshots      = Snapshot.objects.filter(environment_id=environment_id)

                if snapshots.count() >= int(SNAPSHOT_LIMIT):
                    get_message(message="🟠 Snapshot limit exceeded! Please remove 1 snapshot to continue!", is_finishprogram=True, finish_status_code=1)
                else:

                    for snapshot in snapshots:

                        snapshot.last = False
                        snapshot.save()

                    snapshot_name = uuid.uuid4()

                    print('Wait a minute! Taking snapshot')

                    environment_queryset = Environment.objects.get(filesystem_name=environment.filesystem_name)

                    snapshot = Snapshot.objects.create(snapshot_name=snapshot_name, environment_id=environment_queryset).save()

                    resp = Danix.make_snapshot(environment.filesystem_name, snapshot_name)

                    if check_equal_sentence(resp, 0):
                        print("🟢 Snapshot created successfully")
                        print(f"Snapshot name {snapshot_name}\n")
                        print(f"======================================")
                        print(f"Environment size: {Danix.get_size(environment.filesystem_name, None)}B")
                        print(f"Snapshot size:    {Danix.get_size(environment.filesystem_name, snapshot_name)}B")
                        print(f"======================================")
                        exit(0)
                    else:

                        Snapshot.objects.get(snapshot_name=snapshot_name,environment_id=environment).delete()
                        print("🔴 Snapshot create error!")
                        exit(1)
            else:

                get_message(
                            message=settings.ENV_PATTERN_ERROR, 
                            is_finishprogram=True, 
                            finish_status_code=1
                        )  
                
        except Exception:
           get_message(message="🔴 Snapshot create error: Environment does not exist!", is_finishprogram=True, finish_status_code=1)

    @staticmethod
    def list_snapshots():

        snapshots = Snapshot.objects.all()

        print_snapshot_list_header()

        if snapshots.count() > 0:
            for snapshot in snapshots:

                name = str(snapshot.snapshot_name)
                lastsnapshot_icon = "🟢 Yes" if snapshot.last else "🟠 No "

                if snapshot.environment_id:
                    
                    environment_name = Environment.objects.filter(id=snapshot.environment_id.id).first().filesystem_name
                    size_str = str(Danix.get_size(environment_name, name))
                    
                    size_str = get_size_in_mb_or_gb(size_str)
              
                else:

                    environment_name = f'Environment Removed 🔴{14*" "}'
                    size_str = "-----"
                
                print(f"| {name}     {environment_name}         {snapshot.created}              {lastsnapshot_icon}              {size_str}      |")
       
        print_footer()

    class Meta:
        db_table = "snapshot"
# Create your models here.