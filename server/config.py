import argparse 

if __name__ == "__main__" : 
    parser = argparse.ArgumentParser(description='Docker setup')   
    parser.add_argument('--name', help='Binary name') 
    parser.add_argument('--port', help='Port number')  
    args = parser.parse_args() 
    if args.name and args.port : 
        # config docker file 
        dockerfile = open("Dockerfile", "r").read() 
        dockerfile = dockerfile.replace("<bin>", args.name) 
        dockerfile = dockerfile.replace("<port>", args.port) 
        f = open("Dockerfile", "w")
        f.write(dockerfile) 
        f.close()

        # config run.sh 
        run_sh = open("run.sh", "r").read() 
        run_sh = run_sh.replace("<bin>", args.name) 
        f = open("run.sh", "w")
        f.write(run_sh) 
        f.close()

        # config service.conf 
        service_conf = open("service.conf", "r").read() 
        service_conf = service_conf.replace("<port>", args.port) 
        f = open("service.conf", "w")
        f.write(service_conf) 
        f.close() 

        # config build.sh 
        build_sh = open("build.sh", "r").read() 
        build_sh = build_sh.replace("<image_name>", args.name) 
        build_sh = build_sh.replace("<port>", args.port) 
        open("build.sh", "w").write(build_sh)

