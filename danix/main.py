import argparse, os
import app
from utils import is_root
from templates import Languanges

from db.models import Environment, Snapshot

if not is_root():
    print("Please run this program with sudo!")
    exit(0)
    
parser = argparse.ArgumentParser(prog="Danix", add_help=True)

usages = parser.add_argument_group("usages")

usages.add_argument("-l", "--list",          action="store_true" , help="List all environments avaliable", required=False)
usages.add_argument("-sl", "--snapshotlist", action="store_true",  help="List all subsystems snapshots",   required=False)

usages.add_argument("-S", "--start",                help="Start system environment",        required=False)
usages.add_argument("-s", "--stop",                 help="Stop system environment",         required=False)
usages.add_argument("-r", "--rm",                   help="Remove system environment",       required=False)
usages.add_argument("-n", "--navigate",             help="Navigate inside the environment", required=False)

usages.add_argument("-sr", "--snapshotremove",      help="Remove snapshot", required=False)
usages.add_argument("-sc", "--snapshotcreate",      help="Create snapshot", required=False)
usages.add_argument("-sb", "--snapshotback",        help="Back snapshot",   required=False)

usages.add_argument("-o", "--option",   choices=["clike", "java", "python", "ruby"], required=False)

#fullstack_package = parser.add_argument_group("WebStack", "")

#fullstack_package.add_argument("-d","--db", type=str, required=False)
#fullstack_package.add_argument("-w", "--webserver", type=str, required=False)
#fullstack_package.add_argument("-f", "--framework", type=str, required=False)
#fullstack_package.add_argument("-e", "--env_name", type=str, required=False)

args = parser.parse_args()

languanges_and_softwares = {
                                "clike"  : Languanges.CLike(),
                                "java"   : Languanges.Java(),
                                "python" : Languanges.Python(),
                                #"ruby"   : Languanges.Ruby()
                            }

if args.option:

    name = input("Please enter environment name: ")
    languanges_and_softwares.get(args.option).install(name, args.option)

if args.navigate:
    Environment.navigate(args.navigate)

if args.start:
    Environment.start_environment(args.start)

if args.rm:
    Environment.rm_environment(args.rm)

if args.stop:
    Environment.stop_environment(args.stop)

if args.snapshotcreate:
    user_confirm = input("Type 'y' to continue: ")

    if user_confirm == 'y':
        Snapshot.create(args.snapshotcreate)
    print("[Danix]: System abort!")
    
if args.list:
    Environment.list_environments()

if args.snapshotlist:
    Snapshot.list_snapshots()

if args.snapshotback:
    user_confirm = input("Type 'y' to continue: ")

    if user_confirm == 'y':
        Snapshot.back_snapshot(args.snapshotback)
    print("[Danix]: System abort!")

if args.snapshotremove:
    user_confirm = input("Type y to continue: ")
    
    if user_confirm == 'y':
        Snapshot.rm_snapshot(args.snapshotremove)
    print("[Danix]: System abort!")