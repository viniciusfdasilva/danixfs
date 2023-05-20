import os, settings, app
from sh import du
from settings import MAIN_REPO
class Danix():

    @staticmethod
    def copy(environent_is_first, filesystem_name, environment_dir, host_directory):
        
        if environent_is_first:
            return os.system(f"cp -r {MAIN_REPO}{filesystem_name}/danixfs{environment_dir} {host_directory} >/dev/null 2>&1")
        else:
            return os.system(f"cp -r {host_directory} {MAIN_REPO}{filesystem_name}/danixfs{environment_dir} >/dev/null 2>&1")

    @staticmethod
    def remove_snapshot(snapshot_name):
        return os.system(f"rm -r {MAIN_REPO}.snapshots/{snapshot_name} >/dev/null 2>&1")

    @staticmethod
    def rm(filesystem_name):

        return os.system(f"rm -r {MAIN_REPO}{filesystem_name}")

    @staticmethod
    def get_size(environment_name, snapshot_name):
        try:

            if snapshot_name is None:
                return du(
                            f'{MAIN_REPO}{environment_name}/',f'-ch', 
                            f'--exclude={MAIN_REPO}{environment_name}/danixfs/proc/*', 
                            f'--exclude={MAIN_REPO}{environment_name}/danixfs/dev/*', 
                            f'--exclude={MAIN_REPO}{environment_name}/danixfs/sys/*'
                        ).split('\n')[-2].split('\t')[0]
            else:
                return du(f'{MAIN_REPO}.snapshots/{snapshot_name}/{environment_name}.tar.gz','-ch').split('\n')[-2].split('\t')[0]
        except Exception as e:
            print(e)
            return "00M"
        
    @staticmethod
    def make_snapshot(filesystem_name, snapshot_name):

        os.system(f"mkdir {MAIN_REPO}.snapshots/{snapshot_name} >/dev/null 2>&1")
        exclude_proc_dir = f"{MAIN_REPO}{filesystem_name}/danixfs/proc/*"
        exclude_sys_dir  = f"{MAIN_REPO}{filesystem_name}/danixfs/sys/*"
        exclude_dev_dir  = f"{MAIN_REPO}{filesystem_name}/danixfs/dev/*"

        resp = os.system(f"tar -czf {MAIN_REPO}.snapshots/{snapshot_name}/{filesystem_name}.tar.gz --exclude={exclude_proc_dir} --exclude={exclude_dev_dir} --exclude={exclude_sys_dir} {MAIN_REPO}{filesystem_name}/ >/dev/null 2>&1")
        
        return resp
    
    @staticmethod
    def back_snapshot(filesystem_name, snapshot_name):

        Danix.rm(filesystem_name)
        resp1 = os.system(f"tar -xf {MAIN_REPO}.snapshots/{snapshot_name}/{filesystem_name}.tar.gz -C {MAIN_REPO} >/dev/null 2>&1")
        resp2 = os.system(f"mv {MAIN_REPO}opt/danix/{filesystem_name} {MAIN_REPO}")
        resp3 = os.system(f"rm -r {MAIN_REPO}opt")

        return 0 if resp1+resp2+resp3 == 0 else 1
    
    @staticmethod
    def navigate(filesystem_uuid):
        return os.system(f"{MAIN_REPO}{filesystem_uuid}/danixfs/proot -r {MAIN_REPO}{filesystem_uuid}/danixfs/ -w / -0 -b /dev -b /sys -b /proc -b /run sh {MAIN_REPO}init.d/init.sh")

    @staticmethod
    def build_environment(packages, config_comands, filesystem_uuid):
        filesystem = filesystem_uuid

        os.system(f"mkdir /tmp/{filesystem}")
        os.system(f"curl --silent -LO --output-dir /tmp/{filesystem} {settings.REPO_NAME}/{settings.ROOT_FS}")
        os.system(f"tar -xf /tmp/{filesystem}/{settings.ROOT_FS} -C /tmp/{filesystem}")
        os.system(f"rm /tmp/{filesystem}/{settings.ROOT_FS}")
        os.system(f"mv /tmp/{filesystem} {MAIN_REPO}")

        print("\nPlease! Wait a moment!!")
        print("Building container:")
        print(f"Installing {len(packages)} packages\n")

        for command in config_comands:
            os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs {command}")

        for package in packages:
            os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add {package}")

        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add fish")
        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs apk add ruby")
        os.system(f"chroot {MAIN_REPO}{filesystem}/danixfs gem install lolcat")
        
        os.system(f"rm -r {MAIN_REPO}{filesystem}/danixfs/dev >/dev/null 2>&1")
        os.system(f"rm -r {MAIN_REPO}{filesystem}/danixfs/proc >/dev/null 2>&1")
        os.system(f"rm -r {MAIN_REPO}{filesystem}/danixfs/sys >/dev/null 2>&1")

        print(f"Environment builded succesfully!")
        print("0 erros reported!")
        
        Danix.navigate(filesystem)
