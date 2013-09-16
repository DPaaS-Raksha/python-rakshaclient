# Copyright (c) 2013 TrilioData, Inc.
# Copyright (C) 2013 Hewlett-Packard Development Company, L.P.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
BackupJobRuns interface (1.1 extension).
"""

import six
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode
    
from rakshaclient import base


class BackupJobRun(base.Resource):
    """A backup job run describes a back up task that was prepared or execueted"""
    def __repr__(self):
        return "<BackupJobRun: %s>" % self.id

    def restore(self):
        """Restore the backupjobrun """
        return self.manager.restore(self)

class BackupJobRunsManager(base.Manager):
    """Manage :class:`BackupJobRun` resources."""
    resource_class = BackupJobRun


    def get(self, backupjobrun_id):
        """Show details of a backup job run.

        :param backupjobrun_id: The ID of the backup job run to display.
        :rtype: :class:`BackupJobRun`
        """
        return self._get("/backupjobruns/%s" % backupjobrun_id, "backupjobrun")

    def list(self, detailed=True, search_opts=None):
        """Get a list of all backup job runs.

        :rtype: list of :class:`BackupJobRun`
        """
        if search_opts is None:
            search_opts = {}   
            
        qparams = {}

        for opt, val in six.iteritems(search_opts):
            if val:
                qparams[opt] = val

        query_string = "?%s" % urlencode(qparams) if qparams else ""

        detail = ""
        if detailed:
            detail = "/detail"

        return self._list("/backupjobruns%s%s" % (detail, query_string),
                          "backupjobruns")
                          
    def delete(self, backupjobrun_id):
        """Delete a backup job run.

        :param backupjobrun_id: The :class:`BackupJobRun` to delete.
        """
        self._delete("/backupjobruns/%s" % base.getid(backupjobrun_id))

    def restore(self, backupjobrun_id):
        """restores a backup job run.

        :param backupjobrun_id: The :class:`BackupJobRun` to restore.
        """
        self._restore("/backupjobruns/%s" % base.getid(backupjobrun_id))

