from io import BufferedIOBase
import pytest
import unittest.mock as mock
from k8s_docs_tools.generate_release import (
    generate_component_page,
    get_containers,
    gh,
    Charm,
    get_charms,
)
from types import SimpleNamespace


@pytest.fixture(autouse=True)
def github_client():
    with mock.patch("k8s_docs_tools.generate_release.Github") as mock_gh:
        yield mock_gh


def test_gh(github_client):
    gh()
    github_client.assert_called_once_with(None)


def test_charm_cmp():
    assert Charm("a") < Charm("b")


@pytest.mark.parametrize(
    "contents, expected",
    [
        ("[]", []),
        (
            """[{charm: {summary: '', store: charmhub.io, docs: charmhub.io, """
            """upstream: github.com/charmed-kubernetes/, """
            """bugs: https://bugs.launchpad.net/charmed-kubernetes, tags: []}}]""",
            [Charm("charm")],
        ),
    ],
    ids=["empty", "default charm"],
)
def test_get_charms(github_client, contents, expected):
    get_repo = github_client.return_value.get_repo
    get_contents = get_repo.return_value.get_contents
    charm_matrix_file = get_contents.return_value
    charm_matrix_file.decoded_content = contents
    assert get_charms() == expected
    get_repo.assert_called_once_with("charmed-kubernetes/jenkins")
    get_contents.assert_called_once_with(
        "jobs/includes/charm-support-matrix.inc", ref="docs/components"
    )


def test_get_containers_doesnt_match_release(github_client):
    get_repo = github_client.return_value.get_repo
    get_dir_contents = get_repo.return_value.get_dir_contents
    get_dir_contents.return_value = []
    with pytest.raises(IndexError):
        assert get_containers("0.13") == []
    get_repo.assert_called_once_with("charmed-kubernetes/bundle")
    get_dir_contents.assert_called_once_with("container-images")


def test_get_containers_match_release(github_client):
    get_repo = github_client.return_value.get_repo
    get_dir_contents = get_repo.return_value.get_dir_contents
    content = b"rocks.canonical.com/cdk/addon-resizer-amd64:1.8.9"
    get_dir_contents.return_value = [
        SimpleNamespace(path="container-images/README.md"),
        SimpleNamespace(path="container-images/v0.12.2.txt"),
        SimpleNamespace(path="container-images/v0.13.1.txt"),
        SimpleNamespace(path="container-images/v0.13.2.txt", decoded_content=content),
    ]
    assert get_containers("0.13") == ["addon-resizer-amd64:1.8.9"]
    get_repo.assert_called_once_with("charmed-kubernetes/bundle")
    get_dir_contents.assert_called_once_with("container-images")


@mock.patch("k8s_docs_tools.generate_release.get_charms", return_value=[])
@mock.patch("k8s_docs_tools.generate_release.get_containers", return_value=[])
def test_generate_component_page(mock_get_containers, mock_get_charms):
    output = mock.MagicMock(spec=BufferedIOBase)
    generate_component_page("0.13", output)
    mock_get_charms.assert_called_with()
    mock_get_containers.assert_called_with("0.13")
