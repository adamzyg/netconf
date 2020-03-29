#!/usr/bin/env python

# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# show-instances.py
# Show the SimpleExampleServiceInstances and their ip addresses in a human-readable table.
# Syntax: show-instances.py <base_url> <username> <password>
#
# Example: show-instances.py http://192.168.42.253:30006 admin@opencord.org letmein

import sys
import time
import requests
from requests.auth import HTTPBasicAuth

DELAY=1

def main():
    if len(sys.argv)<4:
        print "Syntax: xos-instances.py <base_url> <username> <password>"
        sys.exit(-1)

    base_url = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    auth = HTTPBasicAuth(username, password)

    r = requests.get(base_url + "/xosapi/v1/simpleexampleservice/simpleexampleserviceinstances", auth=auth)

    if r.status_code != 200:
        print "Received error response", r.status_code
        print r.text
        sys.exit(-1)


    print "%-4s %-40s %-4s %-4s" % ("id", "Name", "Comp", "IP")
    for item in r.json()["items"]:
        name = item.get("name")
        compute_id = item["compute_instance_id"]
        if compute_id:
            r_compute = requests.get(base_url + "/xosapi/v1/kubernetes/kubernetesserviceinstances/%s" % compute_id, auth=auth)
            if r_compute.status_code != 200:
                print "Received error response when fetching compute instance", r_compute.status_code
                print r_compute.text
                sys.exit(-1)
            pod_ip = r_compute.json().get("pod_ip", "")
        else:
            pod_ip = ""
        print "%4s %-40s %4s %s" % (item["id"], name, compute_id, pod_ip)


if __name__=="__main__":
    main()
