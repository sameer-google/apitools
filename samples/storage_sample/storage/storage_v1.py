#!/usr/bin/env python
"""CLI for storage, version v1."""

import code
import platform
import sys

import protorpc
from protorpc import message_types
from protorpc import messages

from google.apputils import appcommands
import gflags as flags

import apitools.base.py as apitools_base
import storage_v1_client as client_lib
import storage_v1_messages as messages


def _DeclareStorageFlags():
  """Declare global flags in an idempotent way."""
  if 'api_endpoint' in flags.FLAGS:
    return
  flags.DEFINE_string(
      'api_endpoint',
      u'https://www.googleapis.com/storage/v1/',
      'URL of the API endpoint to use.',
      short_name='storage_url')
  flags.DEFINE_string(
      'history_file',
      u'~/.storage.v1.history',
      'File with interactive shell history.')
  flags.DEFINE_enum(
      'alt',
      u'json',
      [u'json'],
      u'Data format for the response.')
  flags.DEFINE_string(
      'fields',
      None,
      u'Selector specifying which fields to include in a partial response.')
  flags.DEFINE_string(
      'key',
      None,
      u'API key. Your API key identifies your project and provides you with '
      u'API access, quota, and reports. Required unless you provide an OAuth '
      u'2.0 token.')
  flags.DEFINE_string(
      'oauth_token',
      None,
      u'OAuth 2.0 token for the current user.')
  flags.DEFINE_boolean(
      'prettyPrint',
      'True',
      u'Returns response with indentations and line breaks.')
  flags.DEFINE_string(
      'quotaUser',
      None,
      u'Available to use for quota purposes for server-side applications. Can'
      u' be any arbitrary string assigned to a user, but should not exceed 40'
      u' characters. Overrides userIp if both are provided.')
  flags.DEFINE_string(
      'trace',
      None,
      'A tracing token of the form "token:<tokenid>" to include in api '
      'requests.')
  flags.DEFINE_string(
      'userIp',
      None,
      u'IP address of the site where the request originates. Use this if you '
      u'want to enforce per-user limits.')


FLAGS = flags.FLAGS
apitools_base.DeclareBaseFlags()
_DeclareStorageFlags()


def GetGlobalParamsFromFlags():
  """Return a StandardQueryParameters based on flags."""
  result = messages.StandardQueryParameters()
  if FLAGS['alt'].present:
    result.alt = messages.StandardQueryParameters.AltValueValuesEnum(FLAGS.alt)
  if FLAGS['fields'].present:
    result.fields = FLAGS.fields.decode('utf8')
  if FLAGS['key'].present:
    result.key = FLAGS.key.decode('utf8')
  if FLAGS['oauth_token'].present:
    result.oauth_token = FLAGS.oauth_token.decode('utf8')
  if FLAGS['prettyPrint'].present:
    result.prettyPrint = FLAGS.prettyPrint
  if FLAGS['quotaUser'].present:
    result.quotaUser = FLAGS.quotaUser.decode('utf8')
  if FLAGS['trace'].present:
    result.trace = FLAGS.trace.decode('utf8')
  if FLAGS['userIp'].present:
    result.userIp = FLAGS.userIp.decode('utf8')
  return result


def GetClientFromFlags():
  """Return a client object, configured from flags."""
  log_request = FLAGS.log_request or FLAGS.log_request_response
  log_response = FLAGS.log_response or FLAGS.log_request_response
  api_endpoint = apitools_base.NormalizeApiEndpoint(FLAGS.api_endpoint)
  try:
    client = client_lib.StorageV1(
        api_endpoint, log_request=log_request,
        log_response=log_response)
  except apitools_base.CredentialsError as e:
    print 'Error creating credentials: %s' % e
    sys.exit(1)
  return client


class PyShell(appcommands.Cmd):
  def Run(self, _):
    """Run an interactive python shell with the client."""
    client = GetClientFromFlags()
    params = GetGlobalParamsFromFlags()
    for field in params.all_fields():
      value = params.get_assigned_value(field.name)
      if value != field.default:
        client.AddGlobalParam(field.name, value)
    banner = """
           == storage interactive console ==
                 client: a storage client
          apitools_base: base apitools module
         messages: the generated messages module
    """
    local_vars = {
        'apitools_base': apitools_base,
        'client': client,
        'client_lib': client_lib,
        'messages': messages,
    }
    if platform.system() == 'Linux':
      console = apitools_base.ConsoleWithReadline(
          local_vars, histfile=FLAGS.history_file)
    else:
      console = code.InteractiveConsole(local_vars)
    try:
      console.interact(banner)
    except SystemExit as e:
      return e.code


class BucketAccessControlsDelete(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.Delete."""

  usage = """bucketAccessControls_delete <bucket> <entity>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsDelete, self).__init__(name, fv)

  def RunWithArgs(self, bucket, entity):
    """Permanently deletes the ACL entry for the specified entity on the
    specified bucket.

    Args:
      bucket: Name of a bucket.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketAccessControlsDeleteRequest(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    result = client.bucketAccessControls.Delete(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketAccessControlsGet(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.Get."""

  usage = """bucketAccessControls_get <bucket> <entity>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsGet, self).__init__(name, fv)

  def RunWithArgs(self, bucket, entity):
    """Returns the ACL entry for the specified entity on the specified bucket.

    Args:
      bucket: Name of a bucket.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketAccessControlsGetRequest(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    result = client.bucketAccessControls.Get(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketAccessControlsInsert(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.Insert."""

  usage = """bucketAccessControls_insert <bucket>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsInsert, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entity',
        None,
        u'The entity holding the permission, in one of the following forms:  '
        u'- user-userId  - user-email  - group-groupId  - group-email  - '
        u'domain-domain  - project-team-projectId  - allUsers  - '
        u'allAuthenticatedUsers Examples:  - The user liz@example.com would '
        u'be user-liz@example.com.  - The group example@googlegroups.com '
        u'would be group-example@googlegroups.com.  - To refer to all members'
        u' of the Google Apps for Business domain example.com, the entity '
        u'would be domain-example.com.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#bucketAccessControl',
        u'The kind of item this is. For bucket access control entries, this '
        u'is always storage#bucketAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER, WRITER, or '
        u'OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Creates a new ACL entry on the specified bucket.

    Args:
      bucket: The name of the bucket.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For bucket access control entries, this
        is always storage#bucketAccessControl.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER, WRITER, or
        OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.BucketAccessControl(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entity'].present:
      request.entity = FLAGS.entity.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.BucketAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.bucketAccessControls.Insert(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketAccessControlsList(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.List."""

  usage = """bucketAccessControls_list <bucket>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsList, self).__init__(name, fv)

  def RunWithArgs(self, bucket):
    """Retrieves ACL entries on the specified bucket.

    Args:
      bucket: Name of a bucket.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketAccessControlsListRequest(
        bucket=bucket.decode('utf8'),
        )
    result = client.bucketAccessControls.List(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketAccessControlsPatch(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.Patch."""

  usage = """bucketAccessControls_patch <bucket> <entity>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsPatch, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#bucketAccessControl',
        u'The kind of item this is. For bucket access control entries, this '
        u'is always storage#bucketAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER, WRITER, or '
        u'OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket, entity):
    """Updates an ACL entry on the specified bucket. This method supports
    patch semantics.

    Args:
      bucket: The name of the bucket.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For bucket access control entries, this
        is always storage#bucketAccessControl.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER, WRITER, or
        OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.BucketAccessControl(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.BucketAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.bucketAccessControls.Patch(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketAccessControlsUpdate(apitools_base.NewCmd):
  """Command wrapping bucketAccessControls.Update."""

  usage = """bucketAccessControls_update <bucket> <entity>"""

  def __init__(self, name, fv):
    super(BucketAccessControlsUpdate, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#bucketAccessControl',
        u'The kind of item this is. For bucket access control entries, this '
        u'is always storage#bucketAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER, WRITER, or '
        u'OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket, entity):
    """Updates an ACL entry on the specified bucket.

    Args:
      bucket: The name of the bucket.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For bucket access control entries, this
        is always storage#bucketAccessControl.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER, WRITER, or
        OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.BucketAccessControl(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.BucketAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.bucketAccessControls.Update(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsDelete(apitools_base.NewCmd):
  """Command wrapping buckets.Delete."""

  usage = """buckets_delete <bucket>"""

  def __init__(self, name, fv):
    super(BucketsDelete, self).__init__(name, fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u'If set, only deletes the bucket if its metageneration matches this '
        u'value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u'If set, only deletes the bucket if its metageneration does not '
        u'match this value.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Permanently deletes an empty bucket.

    Args:
      bucket: Name of a bucket.

    Flags:
      ifMetagenerationMatch: If set, only deletes the bucket if its
        metageneration matches this value.
      ifMetagenerationNotMatch: If set, only deletes the bucket if its
        metageneration does not match this value.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsDeleteRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    result = client.buckets.Delete(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsGet(apitools_base.NewCmd):
  """Command wrapping buckets.Get."""

  usage = """buckets_get <bucket>"""

  def __init__(self, name, fv):
    super(BucketsGet, self).__init__(name, fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration matches the given value.",
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration does not match the given value.",
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Returns metadata for the specified bucket.

    Args:
      bucket: Name of a bucket.

    Flags:
      ifMetagenerationMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration matches the
        given value.
      ifMetagenerationNotMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration does not
        match the given value.
      projection: Set of properties to return. Defaults to noAcl.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsGetRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['projection'].present:
      request.projection = messages.StorageBucketsGetRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.buckets.Get(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsInsert(apitools_base.NewCmd):
  """Command wrapping buckets.Insert."""

  usage = """buckets_insert <project>"""

  def __init__(self, name, fv):
    super(BucketsInsert, self).__init__(name, fv)
    flags.DEFINE_string(
        'bucket',
        None,
        u'A Bucket resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'private', u'projectPrivate', u'publicRead', u'publicReadWrite'],
        u'Apply a predefined set of access controls to this bucket.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl, unless the bucket '
        u'resource specifies acl or defaultObjectAcl properties, when it '
        u'defaults to full.',
        flag_values=fv)

  def RunWithArgs(self, project):
    """Creates a new bucket.

    Args:
      project: A valid API project identifier.

    Flags:
      bucket: A Bucket resource to be passed as the request body.
      predefinedAcl: Apply a predefined set of access controls to this bucket.
      projection: Set of properties to return. Defaults to noAcl, unless the
        bucket resource specifies acl or defaultObjectAcl properties, when it
        defaults to full.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsInsertRequest(
        project=project.decode('utf8'),
        )
    if FLAGS['bucket'].present:
      request.bucket = apitools_base.JsonToMessage(messages.Bucket, FLAGS.bucket)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageBucketsInsertRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageBucketsInsertRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.buckets.Insert(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsList(apitools_base.NewCmd):
  """Command wrapping buckets.List."""

  usage = """buckets_list <project>"""

  def __init__(self, name, fv):
    super(BucketsList, self).__init__(name, fv)
    flags.DEFINE_integer(
        'maxResults',
        None,
        u'Maximum number of buckets to return.',
        flag_values=fv)
    flags.DEFINE_string(
        'pageToken',
        None,
        u'A previously-returned page token representing part of the larger '
        u'set of results to view.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl.',
        flag_values=fv)

  def RunWithArgs(self, project):
    """Retrieves a list of buckets for a given project.

    Args:
      project: A valid API project identifier.

    Flags:
      maxResults: Maximum number of buckets to return.
      pageToken: A previously-returned page token representing part of the
        larger set of results to view.
      projection: Set of properties to return. Defaults to noAcl.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsListRequest(
        project=project.decode('utf8'),
        )
    if FLAGS['maxResults'].present:
      request.maxResults = FLAGS.maxResults
    if FLAGS['pageToken'].present:
      request.pageToken = FLAGS.pageToken.decode('utf8')
    if FLAGS['projection'].present:
      request.projection = messages.StorageBucketsListRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.buckets.List(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsPatch(apitools_base.NewCmd):
  """Command wrapping buckets.Patch."""

  usage = """buckets_patch <bucket>"""

  def __init__(self, name, fv):
    super(BucketsPatch, self).__init__(name, fv)
    flags.DEFINE_string(
        'bucketResource',
        None,
        u'A Bucket resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration matches the given value.",
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration does not match the given value.",
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'private', u'projectPrivate', u'publicRead', u'publicReadWrite'],
        u'Apply a predefined set of access controls to this bucket.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to full.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Updates a bucket. This method supports patch semantics.

    Args:
      bucket: Name of a bucket.

    Flags:
      bucketResource: A Bucket resource to be passed as the request body.
      ifMetagenerationMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration matches the
        given value.
      ifMetagenerationNotMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration does not
        match the given value.
      predefinedAcl: Apply a predefined set of access controls to this bucket.
      projection: Set of properties to return. Defaults to full.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsPatchRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['bucketResource'].present:
      request.bucketResource = apitools_base.JsonToMessage(messages.Bucket, FLAGS.bucketResource)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageBucketsPatchRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageBucketsPatchRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.buckets.Patch(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class BucketsUpdate(apitools_base.NewCmd):
  """Command wrapping buckets.Update."""

  usage = """buckets_update <bucket>"""

  def __init__(self, name, fv):
    super(BucketsUpdate, self).__init__(name, fv)
    flags.DEFINE_string(
        'bucketResource',
        None,
        u'A Bucket resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration matches the given value.",
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u'Makes the return of the bucket metadata conditional on whether the '
        u"bucket's current metageneration does not match the given value.",
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'private', u'projectPrivate', u'publicRead', u'publicReadWrite'],
        u'Apply a predefined set of access controls to this bucket.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to full.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Updates a bucket.

    Args:
      bucket: Name of a bucket.

    Flags:
      bucketResource: A Bucket resource to be passed as the request body.
      ifMetagenerationMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration matches the
        given value.
      ifMetagenerationNotMatch: Makes the return of the bucket metadata
        conditional on whether the bucket's current metageneration does not
        match the given value.
      predefinedAcl: Apply a predefined set of access controls to this bucket.
      projection: Set of properties to return. Defaults to full.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageBucketsUpdateRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['bucketResource'].present:
      request.bucketResource = apitools_base.JsonToMessage(messages.Bucket, FLAGS.bucketResource)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageBucketsUpdateRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageBucketsUpdateRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.buckets.Update(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ChannelsStop(apitools_base.NewCmd):
  """Command wrapping channels.Stop."""

  usage = """channels_stop"""

  def __init__(self, name, fv):
    super(ChannelsStop, self).__init__(name, fv)
    flags.DEFINE_string(
        'address',
        None,
        u'The address where notifications are delivered for this channel.',
        flag_values=fv)
    flags.DEFINE_string(
        'expiration',
        None,
        u'Date and time of notification channel expiration, expressed as a '
        u'Unix timestamp, in milliseconds. Optional.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'A UUID or similar unique string that identifies this channel.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'api#channel',
        u'Identifies this as a notification channel used to watch for changes'
        u' to a resource. Value: the fixed string "api#channel".',
        flag_values=fv)
    flags.DEFINE_string(
        'params',
        None,
        u'Additional parameters controlling delivery channel behavior. '
        u'Optional.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'payload',
        None,
        u'A Boolean value to indicate whether payload is wanted. Optional.',
        flag_values=fv)
    flags.DEFINE_string(
        'resourceId',
        None,
        u'An opaque ID that identifies the resource being watched on this '
        u'channel. Stable across different API versions.',
        flag_values=fv)
    flags.DEFINE_string(
        'resourceUri',
        None,
        u'A version-specific identifier for the watched resource.',
        flag_values=fv)
    flags.DEFINE_string(
        'token',
        None,
        u'An arbitrary string delivered to the target address with each '
        u'notification delivered over this channel. Optional.',
        flag_values=fv)
    flags.DEFINE_string(
        'type',
        None,
        u'The type of delivery mechanism used for this channel.',
        flag_values=fv)

  def RunWithArgs(self):
    """Stop watching resources through this channel

    Flags:
      address: The address where notifications are delivered for this channel.
      expiration: Date and time of notification channel expiration, expressed
        as a Unix timestamp, in milliseconds. Optional.
      id: A UUID or similar unique string that identifies this channel.
      kind: Identifies this as a notification channel used to watch for
        changes to a resource. Value: the fixed string "api#channel".
      params: Additional parameters controlling delivery channel behavior.
        Optional.
      payload: A Boolean value to indicate whether payload is wanted.
        Optional.
      resourceId: An opaque ID that identifies the resource being watched on
        this channel. Stable across different API versions.
      resourceUri: A version-specific identifier for the watched resource.
      token: An arbitrary string delivered to the target address with each
        notification delivered over this channel. Optional.
      type: The type of delivery mechanism used for this channel.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.Channel(
        )
    if FLAGS['address'].present:
      request.address = FLAGS.address.decode('utf8')
    if FLAGS['expiration'].present:
      request.expiration = int(FLAGS.expiration)
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['params'].present:
      request.params = apitools_base.JsonToMessage(messages.Channel.ParamsValue, FLAGS.params)
    if FLAGS['payload'].present:
      request.payload = FLAGS.payload
    if FLAGS['resourceId'].present:
      request.resourceId = FLAGS.resourceId.decode('utf8')
    if FLAGS['resourceUri'].present:
      request.resourceUri = FLAGS.resourceUri.decode('utf8')
    if FLAGS['token'].present:
      request.token = FLAGS.token.decode('utf8')
    if FLAGS['type'].present:
      request.type = FLAGS.type.decode('utf8')
    result = client.channels.Stop(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsDelete(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.Delete."""

  usage = """defaultObjectAccessControls_delete <bucket> <entity>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsDelete, self).__init__(name, fv)

  def RunWithArgs(self, bucket, entity):
    """Permanently deletes the default object ACL entry for the specified
    entity on the specified bucket.

    Args:
      bucket: Name of a bucket.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageDefaultObjectAccessControlsDeleteRequest(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    result = client.defaultObjectAccessControls.Delete(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsGet(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.Get."""

  usage = """defaultObjectAccessControls_get <bucket> <entity>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsGet, self).__init__(name, fv)

  def RunWithArgs(self, bucket, entity):
    """Returns the default object ACL entry for the specified entity on the
    specified bucket.

    Args:
      bucket: Name of a bucket.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageDefaultObjectAccessControlsGetRequest(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    result = client.defaultObjectAccessControls.Get(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsInsert(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.Insert."""

  usage = """defaultObjectAccessControls_insert <bucket>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsInsert, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entity',
        None,
        u'The entity holding the permission, in one of the following forms:  '
        u'- user-userId  - user-email  - group-groupId  - group-email  - '
        u'domain-domain  - project-team-projectId  - allUsers  - '
        u'allAuthenticatedUsers Examples:  - The user liz@example.com would '
        u'be user-liz@example.com.  - The group example@googlegroups.com '
        u'would be group-example@googlegroups.com.  - To refer to all members'
        u' of the Google Apps for Business domain example.com, the entity '
        u'would be domain-example.com.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'The content generation of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#objectAccessControl',
        u'The kind of item this is. For object access control entries, this '
        u'is always storage#objectAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'object',
        None,
        u'The name of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER or OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Creates a new default object ACL entry on the specified bucket.

    Args:
      bucket: The name of the bucket.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      generation: The content generation of the object.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For object access control entries, this
        is always storage#objectAccessControl.
      object: The name of the object.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER or OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.ObjectAccessControl(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entity'].present:
      request.entity = FLAGS.entity.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['object'].present:
      request.object = FLAGS.object.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.ObjectAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.defaultObjectAccessControls.Insert(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsList(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.List."""

  usage = """defaultObjectAccessControls_list <bucket>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsList, self).__init__(name, fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"If present, only return default ACL listing if the bucket's current"
        u' metageneration matches this value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"If present, only return default ACL listing if the bucket's current"
        u' metageneration does not match the given value.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Retrieves default object ACL entries on the specified bucket.

    Args:
      bucket: Name of a bucket.

    Flags:
      ifMetagenerationMatch: If present, only return default ACL listing if
        the bucket's current metageneration matches this value.
      ifMetagenerationNotMatch: If present, only return default ACL listing if
        the bucket's current metageneration does not match the given value.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageDefaultObjectAccessControlsListRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    result = client.defaultObjectAccessControls.List(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsPatch(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.Patch."""

  usage = """defaultObjectAccessControls_patch <bucket> <entity>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsPatch, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'The content generation of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#objectAccessControl',
        u'The kind of item this is. For object access control entries, this '
        u'is always storage#objectAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'object',
        None,
        u'The name of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER or OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket, entity):
    """Updates a default object ACL entry on the specified bucket. This method
    supports patch semantics.

    Args:
      bucket: The name of the bucket.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      generation: The content generation of the object.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For object access control entries, this
        is always storage#objectAccessControl.
      object: The name of the object.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER or OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.ObjectAccessControl(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['object'].present:
      request.object = FLAGS.object.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.ObjectAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.defaultObjectAccessControls.Patch(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class DefaultObjectAccessControlsUpdate(apitools_base.NewCmd):
  """Command wrapping defaultObjectAccessControls.Update."""

  usage = """defaultObjectAccessControls_update <bucket> <entity>"""

  def __init__(self, name, fv):
    super(DefaultObjectAccessControlsUpdate, self).__init__(name, fv)
    flags.DEFINE_string(
        'domain',
        None,
        u'The domain associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'email',
        None,
        u'The email address associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'entityId',
        None,
        u'The ID for the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'etag',
        None,
        u'HTTP 1.1 Entity tag for the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'The content generation of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'id',
        None,
        u'The ID of the access-control entry.',
        flag_values=fv)
    flags.DEFINE_string(
        'kind',
        u'storage#objectAccessControl',
        u'The kind of item this is. For object access control entries, this '
        u'is always storage#objectAccessControl.',
        flag_values=fv)
    flags.DEFINE_string(
        'object',
        None,
        u'The name of the object.',
        flag_values=fv)
    flags.DEFINE_string(
        'projectTeam',
        None,
        u'The project team associated with the entity, if any.',
        flag_values=fv)
    flags.DEFINE_string(
        'role',
        None,
        u'The access permission for the entity. Can be READER or OWNER.',
        flag_values=fv)
    flags.DEFINE_string(
        'selfLink',
        None,
        u'The link to this access-control entry.',
        flag_values=fv)

  def RunWithArgs(self, bucket, entity):
    """Updates a default object ACL entry on the specified bucket.

    Args:
      bucket: The name of the bucket.
      entity: The entity holding the permission, in one of the following
        forms:  - user-userId  - user-email  - group-groupId  - group-email  -
        domain-domain  - project-team-projectId  - allUsers  -
        allAuthenticatedUsers Examples:  - The user liz@example.com would be
        user-liz@example.com.  - The group example@googlegroups.com would be
        group-example@googlegroups.com.  - To refer to all members of the
        Google Apps for Business domain example.com, the entity would be
        domain-example.com.

    Flags:
      domain: The domain associated with the entity, if any.
      email: The email address associated with the entity, if any.
      entityId: The ID for the entity, if any.
      etag: HTTP 1.1 Entity tag for the access-control entry.
      generation: The content generation of the object.
      id: The ID of the access-control entry.
      kind: The kind of item this is. For object access control entries, this
        is always storage#objectAccessControl.
      object: The name of the object.
      projectTeam: The project team associated with the entity, if any.
      role: The access permission for the entity. Can be READER or OWNER.
      selfLink: The link to this access-control entry.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.ObjectAccessControl(
        bucket=bucket.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['domain'].present:
      request.domain = FLAGS.domain.decode('utf8')
    if FLAGS['email'].present:
      request.email = FLAGS.email.decode('utf8')
    if FLAGS['entityId'].present:
      request.entityId = FLAGS.entityId.decode('utf8')
    if FLAGS['etag'].present:
      request.etag = FLAGS.etag.decode('utf8')
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['id'].present:
      request.id = FLAGS.id.decode('utf8')
    if FLAGS['kind'].present:
      request.kind = FLAGS.kind.decode('utf8')
    if FLAGS['object'].present:
      request.object = FLAGS.object.decode('utf8')
    if FLAGS['projectTeam'].present:
      request.projectTeam = apitools_base.JsonToMessage(messages.ObjectAccessControl.ProjectTeamValue, FLAGS.projectTeam)
    if FLAGS['role'].present:
      request.role = FLAGS.role.decode('utf8')
    if FLAGS['selfLink'].present:
      request.selfLink = FLAGS.selfLink.decode('utf8')
    result = client.defaultObjectAccessControls.Update(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsDelete(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.Delete."""

  usage = """objectAccessControls_delete <bucket> <object> <entity>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsDelete, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)

  def RunWithArgs(self, bucket, object, entity):
    """Permanently deletes the ACL entry for the specified entity on the
    specified object.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsDeleteRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    result = client.objectAccessControls.Delete(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsGet(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.Get."""

  usage = """objectAccessControls_get <bucket> <object> <entity>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsGet, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)

  def RunWithArgs(self, bucket, object, entity):
    """Returns the ACL entry for the specified entity on the specified object.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsGetRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    result = client.objectAccessControls.Get(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsInsert(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.Insert."""

  usage = """objectAccessControls_insert <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsInsert, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'objectAccessControl',
        None,
        u'A ObjectAccessControl resource to be passed as the request body.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Creates a new ACL entry on the specified object.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      objectAccessControl: A ObjectAccessControl resource to be passed as the
        request body.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsInsertRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['objectAccessControl'].present:
      request.objectAccessControl = apitools_base.JsonToMessage(messages.ObjectAccessControl, FLAGS.objectAccessControl)
    result = client.objectAccessControls.Insert(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsList(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.List."""

  usage = """objectAccessControls_list <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsList, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Retrieves ACL entries on the specified object.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsListRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    result = client.objectAccessControls.List(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsPatch(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.Patch."""

  usage = """objectAccessControls_patch <bucket> <object> <entity>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsPatch, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'objectAccessControl',
        None,
        u'A ObjectAccessControl resource to be passed as the request body.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object, entity):
    """Updates an ACL entry on the specified object. This method supports
    patch semantics.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      objectAccessControl: A ObjectAccessControl resource to be passed as the
        request body.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsPatchRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['objectAccessControl'].present:
      request.objectAccessControl = apitools_base.JsonToMessage(messages.ObjectAccessControl, FLAGS.objectAccessControl)
    result = client.objectAccessControls.Patch(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectAccessControlsUpdate(apitools_base.NewCmd):
  """Command wrapping objectAccessControls.Update."""

  usage = """objectAccessControls_update <bucket> <object> <entity>"""

  def __init__(self, name, fv):
    super(ObjectAccessControlsUpdate, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'objectAccessControl',
        None,
        u'A ObjectAccessControl resource to be passed as the request body.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object, entity):
    """Updates an ACL entry on the specified object.

    Args:
      bucket: Name of a bucket.
      object: Name of the object.
      entity: The entity holding the permission. Can be user-userId, user-
        emailAddress, group-groupId, group-emailAddress, allUsers, or
        allAuthenticatedUsers.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      objectAccessControl: A ObjectAccessControl resource to be passed as the
        request body.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectAccessControlsUpdateRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        entity=entity.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['objectAccessControl'].present:
      request.objectAccessControl = apitools_base.JsonToMessage(messages.ObjectAccessControl, FLAGS.objectAccessControl)
    result = client.objectAccessControls.Update(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectsCompose(apitools_base.NewCmd):
  """Command wrapping objects.Compose."""

  usage = """objects_compose <destinationBucket> <destinationObject>"""

  def __init__(self, name, fv):
    super(ObjectsCompose, self).__init__(name, fv)
    flags.DEFINE_string(
        'composeRequest',
        None,
        u'A ComposeRequest resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'destinationPredefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'bucketOwnerFullControl', u'bucketOwnerRead', u'private', u'projectPrivate', u'publicRead'],
        u'Apply a predefined set of access controls to the destination '
        u'object.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'download_filename',
        '',
        'Filename to use for download.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'overwrite',
        'False',
        'If True, overwrite the existing file when downloading.',
        flag_values=fv)

  def RunWithArgs(self, destinationBucket, destinationObject):
    """Concatenates a list of existing objects into a new object in the same
    bucket.

    Args:
      destinationBucket: Name of the bucket in which to store the new object.
      destinationObject: Name of the new object.

    Flags:
      composeRequest: A ComposeRequest resource to be passed as the request
        body.
      destinationPredefinedAcl: Apply a predefined set of access controls to
        the destination object.
      ifGenerationMatch: Makes the operation conditional on whether the
        object's current generation matches the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      download_filename: Filename to use for download.
      overwrite: If True, overwrite the existing file when downloading.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsComposeRequest(
        destinationBucket=destinationBucket.decode('utf8'),
        destinationObject=destinationObject.decode('utf8'),
        )
    if FLAGS['composeRequest'].present:
      request.composeRequest = apitools_base.JsonToMessage(messages.ComposeRequest, FLAGS.composeRequest)
    if FLAGS['destinationPredefinedAcl'].present:
      request.destinationPredefinedAcl = messages.StorageObjectsComposeRequest.DestinationPredefinedAclValueValuesEnum(FLAGS.destinationPredefinedAcl)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    download = None
    if FLAGS.download_filename:
      download = apitools_base.Download.FromFile(FLAGS.download_filename, overwrite=FLAGS.overwrite)
    result = client.objects.Compose(
        request, global_params=global_params, download=download)
    print apitools_base.FormatOutput(result)


class ObjectsCopy(apitools_base.NewCmd):
  """Command wrapping objects.Copy."""

  usage = """objects_copy <sourceBucket> <sourceObject> <destinationBucket> <destinationObject>"""

  def __init__(self, name, fv):
    super(ObjectsCopy, self).__init__(name, fv)
    flags.DEFINE_enum(
        'destinationPredefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'bucketOwnerFullControl', u'bucketOwnerRead', u'private', u'projectPrivate', u'publicRead'],
        u'Apply a predefined set of access controls to the destination '
        u'object.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the destination object's"
        u' current generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the destination object's"
        u' current generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the destination object's"
        u' current metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the destination object's"
        u' current metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifSourceGenerationMatch',
        None,
        u"Makes the operation conditional on whether the source object's "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifSourceGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the source object's "
        u'generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifSourceMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the source object's "
        u'current metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifSourceMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the source object's "
        u'current metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'object',
        None,
        u'A Object resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl, unless the object '
        u'resource specifies the acl property, when it defaults to full.',
        flag_values=fv)
    flags.DEFINE_string(
        'sourceGeneration',
        None,
        u'If present, selects a specific revision of the source object (as '
        u'opposed to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'download_filename',
        '',
        'Filename to use for download.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'overwrite',
        'False',
        'If True, overwrite the existing file when downloading.',
        flag_values=fv)

  def RunWithArgs(self, sourceBucket, sourceObject, destinationBucket, destinationObject):
    """Copies an object to a specified location. Optionally overrides
    metadata.

    Args:
      sourceBucket: Name of the bucket in which to find the source object.
      sourceObject: Name of the source object.
      destinationBucket: Name of the bucket in which to store the new object.
        Overrides the provided object metadata's bucket value, if any.
      destinationObject: Name of the new object. Required when the object
        metadata is not otherwise provided. Overrides the object metadata's
        name value, if any.

    Flags:
      destinationPredefinedAcl: Apply a predefined set of access controls to
        the destination object.
      ifGenerationMatch: Makes the operation conditional on whether the
        destination object's current generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        destination object's current generation does not match the given
        value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        destination object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        destination object's current metageneration does not match the given
        value.
      ifSourceGenerationMatch: Makes the operation conditional on whether the
        source object's generation matches the given value.
      ifSourceGenerationNotMatch: Makes the operation conditional on whether
        the source object's generation does not match the given value.
      ifSourceMetagenerationMatch: Makes the operation conditional on whether
        the source object's current metageneration matches the given value.
      ifSourceMetagenerationNotMatch: Makes the operation conditional on
        whether the source object's current metageneration does not match the
        given value.
      object: A Object resource to be passed as the request body.
      projection: Set of properties to return. Defaults to noAcl, unless the
        object resource specifies the acl property, when it defaults to full.
      sourceGeneration: If present, selects a specific revision of the source
        object (as opposed to the latest version, the default).
      download_filename: Filename to use for download.
      overwrite: If True, overwrite the existing file when downloading.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsCopyRequest(
        sourceBucket=sourceBucket.decode('utf8'),
        sourceObject=sourceObject.decode('utf8'),
        destinationBucket=destinationBucket.decode('utf8'),
        destinationObject=destinationObject.decode('utf8'),
        )
    if FLAGS['destinationPredefinedAcl'].present:
      request.destinationPredefinedAcl = messages.StorageObjectsCopyRequest.DestinationPredefinedAclValueValuesEnum(FLAGS.destinationPredefinedAcl)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['ifSourceGenerationMatch'].present:
      request.ifSourceGenerationMatch = int(FLAGS.ifSourceGenerationMatch)
    if FLAGS['ifSourceGenerationNotMatch'].present:
      request.ifSourceGenerationNotMatch = int(FLAGS.ifSourceGenerationNotMatch)
    if FLAGS['ifSourceMetagenerationMatch'].present:
      request.ifSourceMetagenerationMatch = int(FLAGS.ifSourceMetagenerationMatch)
    if FLAGS['ifSourceMetagenerationNotMatch'].present:
      request.ifSourceMetagenerationNotMatch = int(FLAGS.ifSourceMetagenerationNotMatch)
    if FLAGS['object'].present:
      request.object = apitools_base.JsonToMessage(messages.Object, FLAGS.object)
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsCopyRequest.ProjectionValueValuesEnum(FLAGS.projection)
    if FLAGS['sourceGeneration'].present:
      request.sourceGeneration = int(FLAGS.sourceGeneration)
    download = None
    if FLAGS.download_filename:
      download = apitools_base.Download.FromFile(FLAGS.download_filename, overwrite=FLAGS.overwrite)
    result = client.objects.Copy(
        request, global_params=global_params, download=download)
    print apitools_base.FormatOutput(result)


class ObjectsDelete(apitools_base.NewCmd):
  """Command wrapping objects.Delete."""

  usage = """objects_delete <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectsDelete, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, permanently deletes a specific revision of this object '
        u'(as opposed to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration does not match the given value.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Deletes an object and its metadata. Deletions are permanent if
    versioning is not enabled for the bucket, or if the generation parameter
    is used.

    Args:
      bucket: Name of the bucket in which the object resides.
      object: Name of the object.

    Flags:
      generation: If present, permanently deletes a specific revision of this
        object (as opposed to the latest version, the default).
      ifGenerationMatch: Makes the operation conditional on whether the
        object's current generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        object's current generation does not match the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        object's current metageneration does not match the given value.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsDeleteRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    result = client.objects.Delete(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectsGet(apitools_base.NewCmd):
  """Command wrapping objects.Get."""

  usage = """objects_get <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectsGet, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's generation "
        u'matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's generation "
        u'does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl.',
        flag_values=fv)
    flags.DEFINE_string(
        'download_filename',
        '',
        'Filename to use for download.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'overwrite',
        'False',
        'If True, overwrite the existing file when downloading.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Retrieves an object or its metadata.

    Args:
      bucket: Name of the bucket in which the object resides.
      object: Name of the object.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      ifGenerationMatch: Makes the operation conditional on whether the
        object's generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        object's generation does not match the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        object's current metageneration does not match the given value.
      projection: Set of properties to return. Defaults to noAcl.
      download_filename: Filename to use for download.
      overwrite: If True, overwrite the existing file when downloading.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsGetRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsGetRequest.ProjectionValueValuesEnum(FLAGS.projection)
    download = None
    if FLAGS.download_filename:
      download = apitools_base.Download.FromFile(FLAGS.download_filename, overwrite=FLAGS.overwrite)
    result = client.objects.Get(
        request, global_params=global_params, download=download)
    print apitools_base.FormatOutput(result)


class ObjectsInsert(apitools_base.NewCmd):
  """Command wrapping objects.Insert."""

  usage = """objects_insert <bucket>"""

  def __init__(self, name, fv):
    super(ObjectsInsert, self).__init__(name, fv)
    flags.DEFINE_string(
        'contentEncoding',
        None,
        u'If set, sets the contentEncoding property of the final object to '
        u'this value. Setting this parameter is equivalent to setting the '
        u'contentEncoding metadata property. This can be useful when '
        u'uploading an object with uploadType=media to indicate the encoding '
        u'of the content being uploaded.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'name',
        None,
        u'Name of the object. Required when the object metadata is not '
        u"otherwise provided. Overrides the object metadata's name value, if "
        u'any.',
        flag_values=fv)
    flags.DEFINE_string(
        'object',
        None,
        u'A Object resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'bucketOwnerFullControl', u'bucketOwnerRead', u'private', u'projectPrivate', u'publicRead'],
        u'Apply a predefined set of access controls to this object.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl, unless the object '
        u'resource specifies the acl property, when it defaults to full.',
        flag_values=fv)
    flags.DEFINE_string(
        'upload_filename',
        '',
        'Filename to use for upload.',
        flag_values=fv)
    flags.DEFINE_string(
        'upload_mime_type',
        '',
        'MIME type to use for the upload. Only needed if the extension on '
        '--upload_filename does not determine the correct (or any) MIME '
        'type.',
        flag_values=fv)
    flags.DEFINE_string(
        'download_filename',
        '',
        'Filename to use for download.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'overwrite',
        'False',
        'If True, overwrite the existing file when downloading.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Stores a new object and metadata.

    Args:
      bucket: Name of the bucket in which to store the new object. Overrides
        the provided object metadata's bucket value, if any.

    Flags:
      contentEncoding: If set, sets the contentEncoding property of the final
        object to this value. Setting this parameter is equivalent to setting
        the contentEncoding metadata property. This can be useful when
        uploading an object with uploadType=media to indicate the encoding of
        the content being uploaded.
      ifGenerationMatch: Makes the operation conditional on whether the
        object's current generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        object's current generation does not match the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        object's current metageneration does not match the given value.
      name: Name of the object. Required when the object metadata is not
        otherwise provided. Overrides the object metadata's name value, if
        any.
      object: A Object resource to be passed as the request body.
      predefinedAcl: Apply a predefined set of access controls to this object.
      projection: Set of properties to return. Defaults to noAcl, unless the
        object resource specifies the acl property, when it defaults to full.
      upload_filename: Filename to use for upload.
      upload_mime_type: MIME type to use for the upload. Only needed if the
        extension on --upload_filename does not determine the correct (or any)
        MIME type.
      download_filename: Filename to use for download.
      overwrite: If True, overwrite the existing file when downloading.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsInsertRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['contentEncoding'].present:
      request.contentEncoding = FLAGS.contentEncoding.decode('utf8')
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['name'].present:
      request.name = FLAGS.name.decode('utf8')
    if FLAGS['object'].present:
      request.object = apitools_base.JsonToMessage(messages.Object, FLAGS.object)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageObjectsInsertRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsInsertRequest.ProjectionValueValuesEnum(FLAGS.projection)
    upload = None
    if FLAGS.upload_filename:
      upload = apitools_base.Upload.FromFile(
          FLAGS.upload_filename, FLAGS.upload_mime_type)
    download = None
    if FLAGS.download_filename:
      download = apitools_base.Download.FromFile(FLAGS.download_filename, overwrite=FLAGS.overwrite)
    result = client.objects.Insert(
        request, global_params=global_params, upload=upload, download=download)
    print apitools_base.FormatOutput(result)


class ObjectsList(apitools_base.NewCmd):
  """Command wrapping objects.List."""

  usage = """objects_list <bucket>"""

  def __init__(self, name, fv):
    super(ObjectsList, self).__init__(name, fv)
    flags.DEFINE_string(
        'delimiter',
        None,
        u'Returns results in a directory-like mode. items will contain only '
        u'objects whose names, aside from the prefix, do not contain '
        u'delimiter. Objects whose names, aside from the prefix, contain '
        u'delimiter will have their name, truncated after the delimiter, '
        u'returned in prefixes. Duplicate prefixes are omitted.',
        flag_values=fv)
    flags.DEFINE_integer(
        'maxResults',
        None,
        u'Maximum number of items plus prefixes to return. As duplicate '
        u'prefixes are omitted, fewer total results may be returned than '
        u'requested.',
        flag_values=fv)
    flags.DEFINE_string(
        'pageToken',
        None,
        u'A previously-returned page token representing part of the larger '
        u'set of results to view.',
        flag_values=fv)
    flags.DEFINE_string(
        'prefix',
        None,
        u'Filter results to objects whose names begin with this prefix.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'versions',
        None,
        u'If true, lists all versions of a file as distinct results.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Retrieves a list of objects matching the criteria.

    Args:
      bucket: Name of the bucket in which to look for objects.

    Flags:
      delimiter: Returns results in a directory-like mode. items will contain
        only objects whose names, aside from the prefix, do not contain
        delimiter. Objects whose names, aside from the prefix, contain
        delimiter will have their name, truncated after the delimiter,
        returned in prefixes. Duplicate prefixes are omitted.
      maxResults: Maximum number of items plus prefixes to return. As
        duplicate prefixes are omitted, fewer total results may be returned
        than requested.
      pageToken: A previously-returned page token representing part of the
        larger set of results to view.
      prefix: Filter results to objects whose names begin with this prefix.
      projection: Set of properties to return. Defaults to noAcl.
      versions: If true, lists all versions of a file as distinct results.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsListRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['delimiter'].present:
      request.delimiter = FLAGS.delimiter.decode('utf8')
    if FLAGS['maxResults'].present:
      request.maxResults = FLAGS.maxResults
    if FLAGS['pageToken'].present:
      request.pageToken = FLAGS.pageToken.decode('utf8')
    if FLAGS['prefix'].present:
      request.prefix = FLAGS.prefix.decode('utf8')
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsListRequest.ProjectionValueValuesEnum(FLAGS.projection)
    if FLAGS['versions'].present:
      request.versions = FLAGS.versions
    result = client.objects.List(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectsPatch(apitools_base.NewCmd):
  """Command wrapping objects.Patch."""

  usage = """objects_patch <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectsPatch, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'objectResource',
        None,
        u'A Object resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'bucketOwnerFullControl', u'bucketOwnerRead', u'private', u'projectPrivate', u'publicRead'],
        u'Apply a predefined set of access controls to this object.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to full.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Updates an object's metadata. This method supports patch semantics.

    Args:
      bucket: Name of the bucket in which the object resides.
      object: Name of the object.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      ifGenerationMatch: Makes the operation conditional on whether the
        object's current generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        object's current generation does not match the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        object's current metageneration does not match the given value.
      objectResource: A Object resource to be passed as the request body.
      predefinedAcl: Apply a predefined set of access controls to this object.
      projection: Set of properties to return. Defaults to full.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsPatchRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['objectResource'].present:
      request.objectResource = apitools_base.JsonToMessage(messages.Object, FLAGS.objectResource)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageObjectsPatchRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsPatchRequest.ProjectionValueValuesEnum(FLAGS.projection)
    result = client.objects.Patch(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


class ObjectsUpdate(apitools_base.NewCmd):
  """Command wrapping objects.Update."""

  usage = """objects_update <bucket> <object>"""

  def __init__(self, name, fv):
    super(ObjectsUpdate, self).__init__(name, fv)
    flags.DEFINE_string(
        'generation',
        None,
        u'If present, selects a specific revision of this object (as opposed '
        u'to the latest version, the default).',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifGenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'generation does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration matches the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'ifMetagenerationNotMatch',
        None,
        u"Makes the operation conditional on whether the object's current "
        u'metageneration does not match the given value.',
        flag_values=fv)
    flags.DEFINE_string(
        'objectResource',
        None,
        u'A Object resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_enum(
        'predefinedAcl',
        u'authenticatedRead',
        [u'authenticatedRead', u'bucketOwnerFullControl', u'bucketOwnerRead', u'private', u'projectPrivate', u'publicRead'],
        u'Apply a predefined set of access controls to this object.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to full.',
        flag_values=fv)
    flags.DEFINE_string(
        'download_filename',
        '',
        'Filename to use for download.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'overwrite',
        'False',
        'If True, overwrite the existing file when downloading.',
        flag_values=fv)

  def RunWithArgs(self, bucket, object):
    """Updates an object's metadata.

    Args:
      bucket: Name of the bucket in which the object resides.
      object: Name of the object.

    Flags:
      generation: If present, selects a specific revision of this object (as
        opposed to the latest version, the default).
      ifGenerationMatch: Makes the operation conditional on whether the
        object's current generation matches the given value.
      ifGenerationNotMatch: Makes the operation conditional on whether the
        object's current generation does not match the given value.
      ifMetagenerationMatch: Makes the operation conditional on whether the
        object's current metageneration matches the given value.
      ifMetagenerationNotMatch: Makes the operation conditional on whether the
        object's current metageneration does not match the given value.
      objectResource: A Object resource to be passed as the request body.
      predefinedAcl: Apply a predefined set of access controls to this object.
      projection: Set of properties to return. Defaults to full.
      download_filename: Filename to use for download.
      overwrite: If True, overwrite the existing file when downloading.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsUpdateRequest(
        bucket=bucket.decode('utf8'),
        object=object.decode('utf8'),
        )
    if FLAGS['generation'].present:
      request.generation = int(FLAGS.generation)
    if FLAGS['ifGenerationMatch'].present:
      request.ifGenerationMatch = int(FLAGS.ifGenerationMatch)
    if FLAGS['ifGenerationNotMatch'].present:
      request.ifGenerationNotMatch = int(FLAGS.ifGenerationNotMatch)
    if FLAGS['ifMetagenerationMatch'].present:
      request.ifMetagenerationMatch = int(FLAGS.ifMetagenerationMatch)
    if FLAGS['ifMetagenerationNotMatch'].present:
      request.ifMetagenerationNotMatch = int(FLAGS.ifMetagenerationNotMatch)
    if FLAGS['objectResource'].present:
      request.objectResource = apitools_base.JsonToMessage(messages.Object, FLAGS.objectResource)
    if FLAGS['predefinedAcl'].present:
      request.predefinedAcl = messages.StorageObjectsUpdateRequest.PredefinedAclValueValuesEnum(FLAGS.predefinedAcl)
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsUpdateRequest.ProjectionValueValuesEnum(FLAGS.projection)
    download = None
    if FLAGS.download_filename:
      download = apitools_base.Download.FromFile(FLAGS.download_filename, overwrite=FLAGS.overwrite)
    result = client.objects.Update(
        request, global_params=global_params, download=download)
    print apitools_base.FormatOutput(result)


class ObjectsWatchAll(apitools_base.NewCmd):
  """Command wrapping objects.WatchAll."""

  usage = """objects_watchAll <bucket>"""

  def __init__(self, name, fv):
    super(ObjectsWatchAll, self).__init__(name, fv)
    flags.DEFINE_string(
        'channel',
        None,
        u'A Channel resource to be passed as the request body.',
        flag_values=fv)
    flags.DEFINE_string(
        'delimiter',
        None,
        u'Returns results in a directory-like mode. items will contain only '
        u'objects whose names, aside from the prefix, do not contain '
        u'delimiter. Objects whose names, aside from the prefix, contain '
        u'delimiter will have their name, truncated after the delimiter, '
        u'returned in prefixes. Duplicate prefixes are omitted.',
        flag_values=fv)
    flags.DEFINE_integer(
        'maxResults',
        None,
        u'Maximum number of items plus prefixes to return. As duplicate '
        u'prefixes are omitted, fewer total results may be returned than '
        u'requested.',
        flag_values=fv)
    flags.DEFINE_string(
        'pageToken',
        None,
        u'A previously-returned page token representing part of the larger '
        u'set of results to view.',
        flag_values=fv)
    flags.DEFINE_string(
        'prefix',
        None,
        u'Filter results to objects whose names begin with this prefix.',
        flag_values=fv)
    flags.DEFINE_enum(
        'projection',
        u'full',
        [u'full', u'noAcl'],
        u'Set of properties to return. Defaults to noAcl.',
        flag_values=fv)
    flags.DEFINE_boolean(
        'versions',
        None,
        u'If true, lists all versions of a file as distinct results.',
        flag_values=fv)

  def RunWithArgs(self, bucket):
    """Watch for changes on all objects in a bucket.

    Args:
      bucket: Name of the bucket in which to look for objects.

    Flags:
      channel: A Channel resource to be passed as the request body.
      delimiter: Returns results in a directory-like mode. items will contain
        only objects whose names, aside from the prefix, do not contain
        delimiter. Objects whose names, aside from the prefix, contain
        delimiter will have their name, truncated after the delimiter,
        returned in prefixes. Duplicate prefixes are omitted.
      maxResults: Maximum number of items plus prefixes to return. As
        duplicate prefixes are omitted, fewer total results may be returned
        than requested.
      pageToken: A previously-returned page token representing part of the
        larger set of results to view.
      prefix: Filter results to objects whose names begin with this prefix.
      projection: Set of properties to return. Defaults to noAcl.
      versions: If true, lists all versions of a file as distinct results.
    """
    client = GetClientFromFlags()
    global_params = GetGlobalParamsFromFlags()
    request = messages.StorageObjectsWatchAllRequest(
        bucket=bucket.decode('utf8'),
        )
    if FLAGS['channel'].present:
      request.channel = apitools_base.JsonToMessage(messages.Channel, FLAGS.channel)
    if FLAGS['delimiter'].present:
      request.delimiter = FLAGS.delimiter.decode('utf8')
    if FLAGS['maxResults'].present:
      request.maxResults = FLAGS.maxResults
    if FLAGS['pageToken'].present:
      request.pageToken = FLAGS.pageToken.decode('utf8')
    if FLAGS['prefix'].present:
      request.prefix = FLAGS.prefix.decode('utf8')
    if FLAGS['projection'].present:
      request.projection = messages.StorageObjectsWatchAllRequest.ProjectionValueValuesEnum(FLAGS.projection)
    if FLAGS['versions'].present:
      request.versions = FLAGS.versions
    result = client.objects.WatchAll(
        request, global_params=global_params)
    print apitools_base.FormatOutput(result)


def main(_):
  appcommands.AddCmd('pyshell', PyShell)
  appcommands.AddCmd('bucketAccessControls_delete', BucketAccessControlsDelete)
  appcommands.AddCmd('bucketAccessControls_get', BucketAccessControlsGet)
  appcommands.AddCmd('bucketAccessControls_insert', BucketAccessControlsInsert)
  appcommands.AddCmd('bucketAccessControls_list', BucketAccessControlsList)
  appcommands.AddCmd('bucketAccessControls_patch', BucketAccessControlsPatch)
  appcommands.AddCmd('bucketAccessControls_update', BucketAccessControlsUpdate)
  appcommands.AddCmd('buckets_delete', BucketsDelete)
  appcommands.AddCmd('buckets_get', BucketsGet)
  appcommands.AddCmd('buckets_insert', BucketsInsert)
  appcommands.AddCmd('buckets_list', BucketsList)
  appcommands.AddCmd('buckets_patch', BucketsPatch)
  appcommands.AddCmd('buckets_update', BucketsUpdate)
  appcommands.AddCmd('channels_stop', ChannelsStop)
  appcommands.AddCmd('defaultObjectAccessControls_delete', DefaultObjectAccessControlsDelete)
  appcommands.AddCmd('defaultObjectAccessControls_get', DefaultObjectAccessControlsGet)
  appcommands.AddCmd('defaultObjectAccessControls_insert', DefaultObjectAccessControlsInsert)
  appcommands.AddCmd('defaultObjectAccessControls_list', DefaultObjectAccessControlsList)
  appcommands.AddCmd('defaultObjectAccessControls_patch', DefaultObjectAccessControlsPatch)
  appcommands.AddCmd('defaultObjectAccessControls_update', DefaultObjectAccessControlsUpdate)
  appcommands.AddCmd('objectAccessControls_delete', ObjectAccessControlsDelete)
  appcommands.AddCmd('objectAccessControls_get', ObjectAccessControlsGet)
  appcommands.AddCmd('objectAccessControls_insert', ObjectAccessControlsInsert)
  appcommands.AddCmd('objectAccessControls_list', ObjectAccessControlsList)
  appcommands.AddCmd('objectAccessControls_patch', ObjectAccessControlsPatch)
  appcommands.AddCmd('objectAccessControls_update', ObjectAccessControlsUpdate)
  appcommands.AddCmd('objects_compose', ObjectsCompose)
  appcommands.AddCmd('objects_copy', ObjectsCopy)
  appcommands.AddCmd('objects_delete', ObjectsDelete)
  appcommands.AddCmd('objects_get', ObjectsGet)
  appcommands.AddCmd('objects_insert', ObjectsInsert)
  appcommands.AddCmd('objects_list', ObjectsList)
  appcommands.AddCmd('objects_patch', ObjectsPatch)
  appcommands.AddCmd('objects_update', ObjectsUpdate)
  appcommands.AddCmd('objects_watchAll', ObjectsWatchAll)

  apitools_base.SetupLogger()
  if hasattr(appcommands, 'SetDefaultCommand'):
    appcommands.SetDefaultCommand('pyshell')


run_main = apitools_base.run_main

if __name__ == '__main__':
  appcommands.Run()