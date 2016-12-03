import logging
import os
import paramiko
from OpenMesher.interfaces import IOpenMesherDeployPlugin
from OpenMesher.lib import nested_dict_merge


class SSHDeploy(IOpenMesherDeployPlugin):
    def setupargs(self, parser):
        parser.add_argument('--deploy-username', action='store', help='Username to use when deploying via SSH')
        parser.add_argument('--deploy-dir', action='store', help='Path to upload files')
        super(SSHDeploy, self).setupargs(parser)

    def deploy(self, packagePlugins=None, cliargs=None, stoponfailure=False):
        username = cliargs.deploy_username or 'root'
        deploydir = cliargs.deploy_dir or '/root/'
        logging.info('Assembling files for deployment...')

        deploy_dict = {}
        for plugin in packagePlugins:
            logging.debug('Processing files files from plugin %s...' % (plugin))
            deploy_dict = nested_dict_merge(deploy_dict, plugin.packages())

        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()

        for router in deploy_dict:
            logging.info('Connecting to %s...' % (router))

            local_file_path = deploy_dict[router]
            local_file_split = deploy_dict[router].split('/')
            local_file_name = local_file_split[len(local_file_split) - 1]

            fh = open(local_file_path)
            ssh.connect(router, username=username)
            sftp = ssh.open_sftp()
            remote_file_name = os.path.abspath('%s/%s' % (deploydir, local_file_name))
            logging.info('Deploying %s to %s...' % (local_file_name, remote_file_name))
            remote_file = sftp.file(remote_file_name, 'wb')
            remote_file.set_pipelined(True)
            logging.debug('Starting transfer of %s' % (local_file_name))
            remote_file.write(fh.read())
            logging.debug('Completed transfer of %s' % (local_file_name))
            sftp.close()
            logging.debug('Disconnected from %s' % (router))
            ssh.close()

    def canrestart(self):
        return False

    def canreboot(self):
        return False
