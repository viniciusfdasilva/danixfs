import uuid, os, settings, app
from time import sleep

class Danix():

    @staticmethod
    def rm(filesystem_name):
        return os.system(f"rm {filesystem_name}")

    @staticmethod
    def snapshot(filesystem_name):
        return os.system(f"tar -czf /opt/danix/{filesystem_name}.tar.gz /opt/danix/{filesystem_name}")

    @staticmethod
    def stop(filesystem_name):
        
        print("Wait a minute: Stoping subsystem")
        resp = Danix.snapshot(filesystem_name)
        os.system(f"rm -r /opt/danix/{filesystem_name}")

        return resp

    @staticmethod
    def start(filesystem_name):

        print("Wait a minute: Starting subsystem")
        os.system(f"mkdir /opt/danix/{filesystem_name}")
        resp = os.system(f"tar -xf /opt/danix/{filesystem_name}.tar.gz -C /opt/danix/{filesystem_name} > /dev/null")
        os.system(f"rm -r /opt/danix/{filesystem_name}.tar.gz  > /dev/null")
        return resp

    @staticmethod
    def navigate(filesystem_uuid):

        return os.system(f"chroot /opt/danix/{filesystem_uuid}/danixfs sh /opt/danix/init.d/init.sh")

    @staticmethod
    def build_environment(packages, filesystem_uuid):
        filesystem = filesystem_uuid

        os.system(f"mkdir /tmp/{filesystem}")
        os.system(f"curl --silent -LO --output-dir /tmp/{filesystem} {settings.REPO_NAME}/{settings.ROOT_FS}")
        os.system(f"tar -xf /tmp/{filesystem}/{settings.ROOT_FS} -C /tmp/{filesystem}")
        os.system(f"rm /tmp/{filesystem}/{settings.ROOT_FS}")
        os.system(f"mv /tmp/{filesystem} /opt/danix/")


        print("\nPlease! Wait a moment!!")
        print("Building container:")
        print(f"Installing {len(packages)} packages\n")

        for package in packages:
            os.system(f"chroot /opt/danix/{filesystem}/danixfs apk add {package}")


        os.system(f"chroot /opt/danix/{filesystem}/danixfs apk add ruby")
        os.system(f"chroot /opt/danix/{filesystem}/danixfs gem install lolcat")
        
        print(f"Environment builded succesfully!")
        print("0 erros reported!")
        
        Danix.navigate(filesystem)