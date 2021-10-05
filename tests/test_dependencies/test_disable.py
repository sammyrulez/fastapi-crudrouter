import pytest

from fastapi_crudrouter.core import CRUDGenerator

from tests.implementations import implementations, BaseImpl
from tests.conftest import yield_test_client
from tests.utils import create_base_impl_with_overrides

URLS = ["/potato", "/carrot"]
AUTH = {"Authorization": "Bearer my_token"}
KEY_WORDS = {f"{r}_route" for r in CRUDGenerator.get_routes()}
DISABLE_KWARGS = {k: False for k in KEY_WORDS}


@pytest.fixture(params=implementations, scope="class")
def client(request):
    impl: BaseImpl = request.param
    app = create_base_impl_with_overrides(impl, **DISABLE_KWARGS)

    yield from yield_test_client(app, impl)


@pytest.mark.parametrize("url", URLS)
def test_route_disable(client, url):
    assert client.get(url).status_code == 404
    assert client.get(url).status_code == 404
    assert client.post(url).status_code == 404

    for id_ in [-1, 1, 0, 14]:
        assert client.get(f"{url}/{id_}").status_code == 404
        assert client.put(f"{url}/{id_}").status_code == 404
        assert client.delete(f"{url}/{id_}").status_code == 404
