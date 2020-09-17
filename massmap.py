import subprocess, argparse, os, re
from getpass import getpass
port_default='80,443'
subnet_default="24"
path=str(os.getcwd())
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", help="IPv4 to masscan",type=str,required=True)
    parser.add_argument("-n", help="Name your output folder",type=str,required=True)
    parser.add_argument("-s", help="Subnet to scan\n /8, /16, /24, /32",type=str,default=subnet_default)
    args=parser.parse_args()
    out_name = args.n
    cmd = subprocess.run(['sudo','masscan','-p%s'%(port_default),'%s/%s'%(args.t,args.s),'-oG','%s/masscan_out.txt'%(path)], stdout=subprocess.PIPE)
    output(out_name)
    print("DONE! File stored in %s/%s.txt" % (path,out_name))
    cmd1 = subprocess.run(['rm','-rf','%s/masscan_out.txt'%path])
    cmd2 = subprocess.run(['./massmap.sh','%s.txt'%(out_name),'%s'%(out_name)])
    cmd3 = subprocess.run(['rm','-rf','%s/%s.txt'%(path,out_name)])

def remove_dups(x):
  return list(dict.fromkeys(x))

def output(out_name):
    new_lines=[]
    with open(path+"/masscan_out.txt") as f:
        lines = f.readlines()
        for k in lines:
            new_lines.append(k)
    lines=[]
    ez = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for k in new_lines:
        mo = ez.search(k)
        if mo:
            lines.append(mo.group())
    fin = remove_dups(lines)
    fin.sort()
    with open(path+"/"+out_name+".txt","w") as f:
        for i in fin:
            f.writelines(i+"\n")


if __name__=='__main__':
    main()
