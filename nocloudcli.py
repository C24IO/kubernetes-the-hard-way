#!/usr/bin/env python

import subprocess
import argparse
import shlex
from xml.dom import minidom
import os
import uuid
import random

"""

parser = argparse.ArgumentParser(description='NoCloud Create KVM TestBed')

parser.add_argument('-c', '--create', help='Create testbed', required=True)
args = vars(parser.parse_args())

print(args)


command_string = "who"
command_to_execute = shlex.split(command_string)
print("\ncommand to execute" + str(command_to_execute) + "\n")

process = subprocess.Popen(command_to_execute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
with process.stdout:
    for line in iter(process.stdout.readline, b''):
        print(line.split()[0])

    returncode = process.wait()

"""
"""
Image location - wget -cv https://cloud-images.ubuntu.com/yakkety/current/yakkety-server-cloudimg-amd64.img

"""

def execute_command(command_string='ls'):

    #command_string = "who"

    print('Executing - ' + command_string)

    command_to_execute = shlex.split(command_string)

    print("\ncommand to execute" + str(command_to_execute) + "\n")

    process = subprocess.Popen(command_to_execute, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print stdout
    print stderr

    returncode = process.wait()
    print(returncode)


"""tesbed_vms = ['gateway', 'lbfe', 'controller', 'node0', 'node1', 'node2',
              'node3', 'node4', 'node5', 'node6', 'node7', 'node8', 'node9']"""

tesbed_vms = ['gateway', 'lbfe']

cloud_init_val_dict = {'node0': None}
cloud_init_file_dict = {'cloud-init':'template/cloud-init-user-data', 'cloud-init-new': None}

template_file_dict = {'template':'template/yakketty-64-c-init.xml', 'template-new': None}

for vm in tesbed_vms:

    print "Creating - %s" % vm

    cloud_init_val_dict['node0'] = vm
    cloud_init_file_dict['cloud-init-new'] = 'cloud-init-user-data' + '-' + vm
    template_file_dict['template-new'] = "yakkety-64-c-init-" + vm + ".xml"

    #sed "s/node0/$NODE/g" template/cloud-init-user-data > cloud-init-user-data-$NODE

    with open(cloud_init_file_dict['cloud-init']) as main:
        with open(cloud_init_file_dict['cloud-init-new'], 'w') as new_main:
            input_data = main.read()
            for key, value in cloud_init_val_dict.iteritems():
                input_data = input_data.replace(key, value)

            new_main.write(input_data)
    """
    command_string = "cloud-localds cloud-init-user-data-seed-" + vm + ".img " + "cloud-init-user-data-" + vm
    execute_command(command_string)
    command_string = "qemu-img convert yakkety-server-cloudimg-amd64.orig.img " + " yakkety-server-cloudimg-amd64-" + vm + ".raw"
    execute_command(command_string)
    command_string = "qemu-img resize -f raw yakkety-server-cloudimg-amd64-" + vm + ".raw +15G"
    execute_command(command_string)
    """

    xmldoc = minidom.parse(template_file_dict['template'])
    itemlist = xmldoc.getElementsByTagName('source')

    print(itemlist[0].attributes['file'].value)
    print(itemlist[1].attributes['file'].value)

    dir_path = os.path.dirname(os.path.realpath('cloud-init-user-data-seed-' + vm + '.img'))
    xmldoc.getElementsByTagName('source')[0].attributes['file'].value = dir_path + os.path.sep + 'cloud-init-user-data-seed-' + vm + '.img'
    dir_path = os.path.dirname(os.path.realpath('yakkety-server-cloudimg-amd64-'+ vm +'.raw'))
    xmldoc.getElementsByTagName('source')[1].attributes['file'].value = dir_path + os.path.sep + 'yakkety-server-cloudimg-amd64-'+ vm +'.raw'

    xmldoc.getElementsByTagName('uuid')[0].firstChild.nodeValue = uuid.uuid4()

    xmldoc.getElementsByTagName('mac')[0].attributes['address'].value = str("52:54:00:%s:%s:%s" % (format(random.randint(0, 16), '02x'), format(random.randint(0, 16), '02x'), format(random.randint(0, 16), '02x')))

    xmldoc.getElementsByTagName('name')[0].firstChild.nodeValue = 'yaketty-64-c-init-' + vm

    file_handle = open(template_file_dict['template-new'],"wb")
    xmldoc.writexml(file_handle)
    file_handle.close()
