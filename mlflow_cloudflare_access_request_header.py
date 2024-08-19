import os

try:
    from environs import Env
except ImportError:
    Env = None


class CloudflareAccessRequestHeaderProvider:
    """
    Injects Cloudflare Access service token headers into requests.

    Set `CF_ACCESS_CLIENT_ID` and `CF_ACCESS_CLIENT_SECRET` environment variables.
    """

    headers = {}

    def __init__(self):
        if Env is None:

            def var(name):
                return os.environ.get(name)
        else:
            env = Env()
            env.read_env(f"{os.getcwd()}/.env")

            def var(name):
                return env(name, default=None)

        if (v := var("CF_ACCESS_CLIENT_ID")) or (
            v := var("CLOUDFLARE_ACCESS_CLIENT_ID")
        ):
            self.headers["CF-Access-Client-Id"] = v
        if (v := var("CF_ACCESS_CLIENT_SECRET")) or (
            v := var("CLOUDFLARE_ACCESS_CLIENT_SECRET")
        ):
            self.headers["CF-Access-Client-Secret"] = v

    def request_headers(self):
        return self.headers

    @classmethod
    def in_context(cls):
        return True
