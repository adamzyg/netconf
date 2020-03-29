
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


from ncclient import manager
from synchronizers.new_base.syncstep import SyncStep
from synchronizers.new_base.modelaccessor import NetconfApp
from xosconfig import Config
from multistructlog import create_logger

log = create_logger(Config().get('logging'))

class SyncNetconfApp(SyncStep):

    provides = [NetconfApp]
    observes = [NetconfApp]

    def __init__(self, *args, **kwargs):
        super(SyncNetconfApp, self).__init__(*args, **kwargs)

    def _query_server_capabilities(self, host, port, user, password, timeout=1000, hostkey_verify=False):
        log.info("query capabilities")
        capabilities = str()
        with manager.connect(host=host, port=port, username=user, password=password, timeout=timeout, hostkey_verify=hostkey_verify) as m:
            for cap in m.server_capabilities:
                capabilities += str(cap).strip() + " "
        return capabilities.strip()

    def sync_record(self, o):
        log.info("Sync'ing NetconfApp", model=o.tologdict())
        host = o.host
        port = o.port
        user = o.user
        password = o.password

        capabilities = self._query_server_capabilities(host, port, user, password)
        o.yang = capabilities
        log.info("query capabilities form %s, %s" % (host, capabilities))
        o.save()

    def delete_record(self, o):
        log.info("deleting object of NetconfApp", object=str(o), **o.tologdict())
        pass
