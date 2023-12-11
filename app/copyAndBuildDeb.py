import sys
import pexpect
import subprocess
from pexpect import pxssh
import argparse

repo_name = "deb-build"
package_name = "pullbasedagent-test"
destination = "{}/usr/local/{}".format(repo_name, package_name)
control_file = "{}/DEBIAN/control".format(repo_name)
username = "ubuntu"
#password = "32lW~XL525Bd62a"


class DebPackageGenerator:
    def __init__(self, args):
        self.new_version = args.version
        if args.environment == "Development":
            self.env = "www.example.com"
            self.path = "{}@{}:/home/{}/app".format(username, self.env, username)
            self.repo = "testing"
            self.publish()
        elif args.environment == "Staging":
            self.env = "3.91.76.141"
            self.path = "{}@{}:/home/{}/packages".format(username, self.env, username)
            self.repo = "unstable"
            self.publish()
        elif args.environment == "Production":
            self.env = "www.example.com"
            self.path = "{}@{}:/home/{}/packages".format(username, self.env, username)
            self.repo = "stable"
            self.publish()
        else:
            print("You have entered an invalid option.")
            sys.exit(1)

    def remote_exec(self, package_name_deploy):
        try:
            ssh_obj = pxssh.pxssh()
            ssh_obj.login(self.env, username, password)
            ssh_obj.sendline('cd /home/ubuntu/packages')
            if "dev" in self.env:
                print("Adding repo in development.")
            elif "141" in self.env:
                print("Adding repo in staging.")
            else:
                print("Adding repo in production.")
            snap_ver = '{}{}-{}'.format(package_name, self.new_version, self.repo)
            ssh_obj.sendline('aptly repo add {} {}'.format(self.repo, package_name_deploy))
            ssh_obj.sendline('aptly snapshot create {} from repo {}'.format(snap_ver, self.repo))
            ssh_obj.sendline('aptly publish -passphrase=noc@1235 switch xenial {}'.format(snap_ver))
            ssh_obj.prompt()
            ssh_obj.sendline('exit')
            ssh_obj.logout()
        except pxssh.ExceptionPxssh as e:
            print("pxssh failed on login.")
            print(e)
        except pexpect.exceptions.TIMEOUT as e:
            print("pxssh timeout, you can ignore this.")
            print(e)

    def run_on_shell(self, cmd):
        res = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = res.communicate()
        return out

    def publish(self):
        self.run_on_shell('find . -name "*.pyc" -type f -delete')
        self.run_on_shell("mkdir -p {}".format(destination))
        self.run_on_shell("rsync -av --exclude='deb-build' --exclude='{}*' * {}".format(package_name, destination))
        self.run_on_shell('sed -i "s/Version:.*/Version: {}/g" {}/DEBIAN/control'.format(self.new_version, repo_name))

        package_name_deploy = '{}_{}.deb'.format(package_name, self.new_version)
        self.run_on_shell('dpkg-deb --build {} {}'.format(repo_name, package_name_deploy))
        self.run_on_shell('scp -i /home/sharathdb/Downloads/key.pem {} {}@{}:{}'.format(package_name_deploy, username, self.env, self.path))
        self.run_on_shell('rm -r {}/usr'.format(repo_name))
        self.remote_exec(package_name_deploy)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create debian package.')
    parser.add_argument('-v', '--version', metavar="version", required=True)
    parser.add_argument('-e', '--environment', metavar="environment", required=True)
    args = parser.parse_args()
    DebPackageGenerator(args)
