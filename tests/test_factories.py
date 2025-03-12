from raja_aita.factories import RepositoryFactory


class TestRepositoryFactory:
    def test_call_returns_single_factory(self, settings):
        factory = RepositoryFactory()
        another_factory = RepositoryFactory()

        assert factory(settings) is another_factory(settings)
