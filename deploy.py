import boto3
import copy

client = boto3.client('ecs')
IMAGE = '360844283138.dkr.ecr.us-east-1.amazonaws.com/create-branch-from-issue:latest'
APP_NAME = 'create-branch-from-issue'


COMMON_TASK_DEF = {
    'name': APP_NAME,
    'image': IMAGE,
    'cpu': 64,
    'memory': 128,
    'portMappings': [
        {
            'containerPort': 5000
        },
    ],
    'environment': [
        {
            'name': 'APP_ENV',
            'value': 'production'
        },
    ],
    'essential': True,
    'command': [
        'ruby',
        'server.rb'
    ],
    'workingDirectory': '/app'
}


def update_service():
    monitor_task_def = copy.deepcopy(COMMON_TASK_DEF)
    monitor_task_def.update({'name': APP_NAME})
    resp = client.register_task_definition(
        family=APP_NAME,
        containerDefinitions=[monitor_task_def],
        requiresCompatibilities=['EC2']
    )

    family = resp['taskDefinition']['family']
    revision = resp['taskDefinition']['revision']
    new_task_arn = family + ':' + str(revision)
    print(new_task_arn)

    resp = client.update_service(
        cluster='ECS',
        service=APP_NAME,
        desiredCount=1,
        taskDefinition=new_task_arn
    )

    for i in range(revision):
        try:
            client.deregister_task_definition(
                taskDefinition=family + ':' + str(i)
            )
        except:
            continue


if __name__ == '__main__':
    update_service()
