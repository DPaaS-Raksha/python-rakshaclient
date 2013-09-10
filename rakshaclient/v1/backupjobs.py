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
BackupJobs Interface (1.1 extension).
"""

from rakshaclient import base


class BackupJob(base.Resource):
    """A backup job describes a back up task that takes a consistent backup of one or more VMs"""
    def __repr__(self):
        return "<BackupJob: %s>" % self.id

    def delete(self):
        """Delete this backup job."""
        return self.manager.delete(self)

    def execute(self):
        """Starts a job once """
        return self.manager.execute(self)

    def prepare(self):
        """Starts a job once """
        return self.manager.prepare(self)


class BackupJobManager(base.ManagerWithFind):
    """Manage :class:`BackupJob` resources."""
    resource_class = BackupJob

    def create(self, instance_id, vault_service=None,
               name=None, description=None):
        """Create a backup job.

        :param instance_id: The ID of the vm instance to backup.
        :param vault_service: The name of the backup vault service.
        :param name: The name of the backup job.
        :param description: The description of the backup job.
        :rtype: :class:`BackupJob`
        """
        body = {'backupjob': {'instance_id': instance_id,
                           'vault_service': vault_service,
                           'name': name,
                           'description': description}}
        return self._create('/backupjobs', body, 'backupjob')

    def get(self, backupjob_id):
        """Show details of a backup job.

        :param backupjob_id: The ID of the backup job to display.
        :rtype: :class:`BackupJob`
        """
        return self._get("/backupjobs/%s" % backupjob_id, "backupjob")

    def list(self, detailed=True):
        """Get a list of all backup jobs.

        :rtype: list of :class:`BackupJob`
        """
        if detailed is True:
            return self._list("/backupjobs/detail", "backupjobs")
        else:
            return self._list("/backupjobs", "backupjobs")

    def delete(self, backupjob_id):
        """Delete a backup job.

        :param backupjob_id: The :class:`BackupJob` to delete.
        """
        self._delete("/backupjobs/%s" % base.getid(backupjob_id))

    def execute(self, backupjob_id):
        """Executes a backup job.

        :param backupjob_id: The :class:`BackupJob` to execute.
        """
        self._execute("/backupjobs/%s" % base.getid(backupjob_id))

    def prepare(self, backupjob_id):
        """Executes a backup job.

        :param backupjob_id: The :class:`BackupJob` to execute.
        """
        self._execute("/backupjobs/%s?prepare=1" % base.getid(backupjob_id))
        
        
