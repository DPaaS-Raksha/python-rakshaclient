# Copyright (c) 2013 TrilioData, Inc.
# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.
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

from __future__ import print_function

import argparse
import os
import sys
import time

from rakshaclient import exceptions
from rakshaclient import utils


def _poll_for_status(poll_fn, obj_id, action, final_ok_states,
                     poll_period=5, show_progress=True):
    """Block while an action is being performed, periodically printing
    progress.
    """
    def print_progress(progress):
        if show_progress:
            msg = ('\rInstance %(action)s... %(progress)s%% complete'
                   % dict(action=action, progress=progress))
        else:
            msg = '\rInstance %(action)s...' % dict(action=action)

        sys.stdout.write(msg)
        sys.stdout.flush()

    print()
    while True:
        obj = poll_fn(obj_id)
        status = obj.status.lower()
        progress = getattr(obj, 'progress', None) or 0
        if status in final_ok_states:
            print_progress(100)
            print("\nFinished")
            break
        elif status == "error":
            print("\nError %(action)s instance" % locals())
            break
        else:
            print_progress(progress)
            time.sleep(poll_period)


def _find_volume(cs, volume):
    """Get a volume by ID."""
    return utils.find_resource(cs.volumes, volume)


def _find_volume_snapshot(cs, snapshot):
    """Get a volume snapshot by ID."""
    return utils.find_resource(cs.volume_snapshots, snapshot)


def _find_backupjob(cs, backupjob_id):
    """Get a backup job by ID."""
    return utils.find_resource(cs.backupjobs, backupjob_id)

def _find_backupjobrun(cs, backupjobrun_id):
    """Get a backup job run by ID."""
    return utils.find_resource(cs.backupjobruns, backupjobrun_id)
    
def _print_volume(volume):
    utils.print_dict(volume._info)


def _print_volume_snapshot(snapshot):
    utils.print_dict(snapshot._info)


def _translate_keys(collection, convert):
    for item in collection:
        keys = item.__dict__.keys()
        for from_key, to_key in convert:
            if from_key in keys and to_key not in keys:
                setattr(item, to_key, item._info[from_key])


def _translate_volume_keys(collection):
    convert = [('displayName', 'display_name'), ('volumeType', 'volume_type')]
    _translate_keys(collection, convert)


def _translate_volume_snapshot_keys(collection):
    convert = [('displayName', 'display_name'), ('volumeId', 'volume_id')]
    _translate_keys(collection, convert)


def _extract_metadata(args):
    metadata = {}
    for metadatum in args.metadata:
        # unset doesn't require a val, so we have the if/else
        if '=' in metadatum:
            (key, value) = metadatum.split('=', 1)
        else:
            key = metadatum
            value = None

        metadata[key] = value
    return metadata



def _print_volume_type_list(vtypes):
    utils.print_list(vtypes, ['ID', 'Name'])


def _print_type_and_extra_specs_list(vtypes):
    formatters = {'extra_specs': _print_type_extra_specs}
    utils.print_list(vtypes, ['ID', 'Name', 'extra_specs'], formatters)


def do_endpoints(cs, args):
    """Discover endpoints that get returned from the authenticate services."""
    catalog = cs.client.service_catalog.catalog
    for e in catalog['access']['serviceCatalog']:
        utils.print_dict(e['endpoints'][0], e['name'])


def do_credentials(cs, args):
    """Show user credentials returned from auth."""
    catalog = cs.client.service_catalog.catalog
    utils.print_dict(catalog['access']['user'], "User Credentials")
    utils.print_dict(catalog['access']['token'], "Token")

_quota_resources = ['volumes', 'snapshots', 'gigabytes']


@utils.service_type('backupjobs')
def do_absolute_limits(cs, args):
    """Print a list of absolute limits for a user"""
    limits = cs.limits.get().absolute
    columns = ['Name', 'Value']
    utils.print_list(limits, columns)


@utils.service_type('backupjobs')
def do_rate_limits(cs, args):
    """Print a list of rate limits for a user"""
    limits = cs.limits.get().rate
    columns = ['Verb', 'URI', 'Value', 'Remain', 'Unit', 'Next_Available']
    utils.print_list(limits, columns)


def _print_type_extra_specs(vol_type):
    try:
        return vol_type.get_keys()
    except exceptions.NotFound:
        return "N/A"


def _find_volume_type(cs, vtype):
    """Get a volume type by name or ID."""
    return utils.find_resource(cs.volume_types, vtype)


@utils.arg('instanceid', metavar='<vm instance id>',
           help='ID of the vm instance to backup.')
@utils.arg('--vault_service', metavar='<vault_service>',
           help='Optional Backup vault service id. (Default=None)',
           default=None)
@utils.arg('--display-name', metavar='<display-name>',
           help='Optional backup name. (Default=None)',
           default=None)
@utils.arg('--display-description', metavar='<display-description>',
           help='Optional backup description. (Default=None)',
           default=None)
@utils.service_type('backupjobs')
def do_backupjob_create(cs, args):
    """Creates a backup job."""
    cs.backupjobs.create(args.instanceid,
                      args.vault_service,
                      args.display_name,
                      args.display_description)


@utils.arg('backupjob_id', metavar='<backupjob_id>', help='ID of the backup job.')
@utils.service_type('backupjobs')
def do_backupjob_show(cs, args):
    """Show details about a backup job."""
    backupjob = _find_backupjob(cs, args.backupjob_id)
    info = dict()
    info.update(backupjob._info)

    if 'links' in info:
        info.pop('links')

    utils.print_dict(info)


@utils.service_type('backupjobs')
def do_backupjob_list(cs, args):
    """List all the backup jobs."""
    backupjobs = cs.backupjobs.list()
    columns = ['ID', 'Status', 'Name', 'Size', 'Object Count',
               'Vault Service']
    utils.print_list(backupjobs, columns)


@utils.arg('backupjob_id', metavar='<backupjob_id>',
           help='ID of the backup job to delete.')
@utils.service_type('backupjobs')
def do_backupjob_delete(cs, args):
    """Remove a backup job."""
    backupjob = _find_backupjob(cs, args.backupjob_id)
    backupjob.delete()

@utils.arg('backupjob_id', metavar='<backupjob_id>',
           help='ID of the backup job to execute.')
@utils.service_type('backupjobs')
def do_backupjob_execute(cs, args):
    """Executes a backup job."""
    backupjob = _find_backupjob(cs, args.backupjob_id)
    backupjob.execute()

@utils.arg('backupjob_id', metavar='<backupjob_id>',
           help='ID of the backup job to execute.')
@utils.service_type('backupjobs')
def do_backupjob_prepare(cs, args):
    """Prepares the backup up by doing a full backup."""
    backupjob = _find_backupjob(cs, args.backupjob_id)
    backupjob.prepare()

@utils.arg('backupjobrun_id', metavar='<backupjobrun_id>', help='ID of the backup job run.')
@utils.service_type('backupjobs')
def do_backupjobrun_show(cs, args):
    """Show details about a backup job run"""
    backupjobrun = _find_backupjobrun(cs, args.backupjobrun_id)
    info = dict()
    info.update(backupjobrun._info)

    if 'links' in info:
        info.pop('links')

    utils.print_dict(info)


@utils.service_type('backupjobs')
def do_backupjobrun_list(cs, args):
    """List all the backup jobs."""
    backupjobruns = cs.backupjobruns.list()
    columns = ['ID', 'Backup Job', 'Type','Status']
    utils.print_list(backupjobruns, columns)


@utils.arg('backupjobrun_id', metavar='<backupjobrun_id>',
           help='ID of the backup job run to delete.')
@utils.service_type('backupjobs')
def do_backupjobrun_delete(cs, args):
    """Remove a backup job run."""
    backupjobrun = _find_backupjobrun(cs, args.backupjobrun_id)
    backupjobrun.delete()
    
@utils.arg('backupjobrun_id', metavar='<backupjobrun_id>',
           help='ID of the backup job run to restore.')
@utils.service_type('backupjobs')
def do_backupjobrun_restore(cs, args):
    """Restore a backup job run."""
    backupjobrun = _find_backupjobrun(cs, args.backupjobrun_id)
    backupjobrun.restore()
