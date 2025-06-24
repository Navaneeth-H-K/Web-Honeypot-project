import argparse
import ssh_honeypot
import web_honeypot

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-a','--address',type=str, required=True)
    parser.add_argument('-p','--port',type=int, required=True)
    parser.add_argument('-u','--username',type=str)
    parser.add_argument('-pw','--password',type=str)
    parser.add_argument('-s','--ssh',action="store_true")
    parser.add_argument('-w','--http',action="store_true")

    args=parser.parse_args()

    try:
        if args.ssh:
            print("[-]SSH Loading")
            ssh_honeypot.honey(args.address,args.port,args.username,args.password)

            if args.username==False:
                args.username=None
            if args.password==False:
                args.password=None

        elif args.http:
            print("[-]Web Loading")
            if args.username==False:
                args.username="admin"
            if args.password==False:
                args.password="password"
            print("Port:",args.port,end="")
            print("Username:",args.username,end="")
            print("Password:",args.password,end="\n")
            web_honeypot.initiate(args.port,args.username,args.password)
        else:
            print("[!]Choose the honeypot type --ssh/--http")
    except:
        print("\nHoneypot already Loaded\n\n\n\n")
