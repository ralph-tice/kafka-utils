from behave import then
from behave import when
from util import call_cmd
from util import get_cluster_config

from yelp_kafka_tool.util.zookeeper import ZK


def offsets_data(topic, offset):
    return '''{topic}.{partition}={offset}'''.format(
        topic=topic,
        partition='0',
        offset=offset,
    )


def call_offset_rewind(groupid, topic):
    cmd = ['kafka-consumer-manager',
           '--cluster-type', 'test',
           '--cluster-name', 'test_cluster',
           '--discovery-base-path', 'tests/acceptance/config',
           'offset_rewind',
           groupid,
           '--topic', topic]
    return call_cmd(cmd)


@when(u'we call the offset_rewind command with a groupid and topic')
def step_impl3(context):
    call_offset_rewind(context.group, context.topic)


@then(u'the committed offsets will match the earliest message offsets')
def step_impl4(context):
    cluster_config = get_cluster_config()
    with ZK(cluster_config) as zk:
        offsets = zk.get_group_offsets(context.group)
    assert offsets[context.topic]["0"] == 0