import re

from common.fastapi.core.parameters import get_param_manager


class AwsConfig(object):

    @property
    def param_manager(self):
        return get_param_manager()

    def get_boto3_session(self):
        if not (self.param_manager.variables.ACCESS_KEY_ID and self.param_manager.variables.SECRET_ACCESS_KEY):
            raise AttributeError(
                "if you want to use aws manager you must put "
                "ACCESS_KEY_ID and SECRET_ACCESS_KEY in your environment configurations"
            )

        import boto3
        return boto3.Session(
            aws_access_key_id=self.param_manager.variables.ACCESS_KEY_ID,
            aws_secret_access_key=self.param_manager.variables.SECRET_ACCESS_KEY
        )

    def __getattr__(self, item):
        is_aws = re.fullmatch(r"get_\w+_\w+", item)
        if is_aws:
            session = self.get_boto3_session()
            elements = item.split("_")

            client_name = elements[-2]
            aws_type = elements[-1]

            if aws_type == 'client':
                return lambda: session.client(client_name)
            elif aws_type == 'resource':
                return lambda: session.resource(client_name)
        else:
            return self.__getattribute__(item)
