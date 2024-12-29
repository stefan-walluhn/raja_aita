from raja_aita.factories import RepositoryFactory


class TestRepositoryFactory:
    def test_call_returns_single_factory(self):
        factory = RepositoryFactory()
        another_factory = RepositoryFactory()

        assert factory() is another_factory()
