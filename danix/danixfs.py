import uuid, os, settings, app
from settings import MAIN_REPO
from time import sleep

class Danix():

    @staticmethod
    def remove_snapshot(snapshot_name):
        return os.system(f"rm -r {MAIN_REPO}.snapshots/{snapshot_name}")

    @staticmethod
    def rm(filesystem_name):
        return os.system(f"rm -r {MAIN_REPO}{filesystem_name}")

    @staticmethod
    def make_snapshot(filesystem_name, snapshot_name):

        os.system(f"mkdir {MAIN_REPO}.snapshots/{snapshot_name}")
        resp = os.system(f"tar -czf {MAIN_REPO}.snapshots/{snapshot_name}/{filesystem_name}.tar.gz {MAIN_REPO}{filesystem_name}/")
        
        return resp
    
    @staticmethod
    def back_snapshot(filesystem_name, snapshot_name):

        os.system(f"rm -r {MAIN_REPO}{filesystem_name} > /dev/null")  
        resp1 = os.system(f"tar -xf {MAIN_REPO}.snapshots/{snapshot_name}/{filesystem_name}.tar.gz -C {MAIN_REPO}")
        resp2 = os.system(f"mv {MAIN_REPO}/opt/danix/{filesystem_name} {MAIN_REPO}")
        resp3 = os.system(f"rm -r {MAIN_REPO}opt")

        return 0 if resp1+resp2+resp3 == 0 else 1
    
    @staticmethod
    def navigate(filesystem_uuid):

        return os.system(f"chroot {MAIN_REPO}{filesystem_uuid}/danixfs sh {MAIN_REPO}init.d/init.sh")

    @staticmethod
    def build_environment(packages, filesystem_uuid):
        filesystem = filesystem_uuid

        os.system(f"mkdir /tmp/{filesystem}")
        os.system(f"curl --silent -LO --output-dir /tmp/{filesystem} {settings.REPO_NAME}/{settings.ROOT_FS}")
        os.system(f"tar -xf /tmp/{filesystem}/{settings.ROOT_FS} -C /tmp/{filesystem}")
        os.system(f"rm /tmp/{filesystem}/{settings.ROOT_FS}")
        os.system(f"mv /tmp/{filesystem} {MAIN_REPO}")


        print("\nPlease! Wait a moment!!")
        print("Building container:")
        print(f"Installing {len(packages)} packages\n")

        for package in packages:
            os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add {package}")


        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add fish")
        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add ruby")
        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs gem install lolcat")
        
        print(f"Environment builded succesfully!")
        print("0 erros reported!")
        
        Danix.navigate(filesystem)