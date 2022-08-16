# -*- coding: utf-8 -*-

from pathlib import Path
import pytest
import unittest.mock as mock
import k8s_docs_tools.generate_release as generator
from types import SimpleNamespace


@pytest.fixture(autouse=True)
def github_client():
    with mock.patch.object(generator, "Github") as mock_gh:
        yield mock_gh


def test_gh(github_client):
    generator.gh()
    github_client.assert_called_once_with(None)


def test_ver_to_tuple():
    assert generator._ver_to_tuple("1.2.3.4") == (1, 2, 3, 4)


def test_ReleaseBundle():
    rel1_12_1 = generator.ReleaseBundle("0.12.1", "cs:charmed-kubernetes-1234")
    rel1_13 = generator.ReleaseBundle("0.13", "cs:charmed-kubernetes-1234")
    assert rel1_13.no_cs_bundle == "charmed-kubernetes-1234"
    assert rel1_13 > rel1_12_1


def test_PageWriter_supported(tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    assert pw.supported == ["0.13", "0.12", "0.11"]


def test_charm_cmp():
    assert generator.Charm("a") < generator.Charm("b")


@pytest.mark.parametrize(
    "contents, expected",
    [
        ("[]", []),
        (
            """[{charm: {summary: '', store: charmhub.io, docs: charmhub.io, """
            """upstream: github.com/charmed-kubernetes/, """
            """bugs: https://bugs.launchpad.net/charmed-kubernetes, tags: []}}]""",
            [generator.Charm("charm")],
        ),
    ],
    ids=["empty", "default charm"],
)
def test_get_charms(github_client, contents, expected):
    get_repo = github_client.return_value.get_repo
    get_contents = get_repo.return_value.get_contents
    charm_matrix_file = get_contents.return_value
    charm_matrix_file.decoded_content = contents
    assert generator.get_charms() == expected
    get_repo.assert_called_once_with("charmed-kubernetes/jenkins")
    get_contents.assert_called_once_with(
        "jobs/includes/charm-support-matrix.inc", ref="main"
    )


def test_get_containers_doesnt_match_release(github_client):
    get_repo = github_client.return_value.get_repo
    get_dir_contents = get_repo.return_value.get_dir_contents
    get_dir_contents.return_value = []
    assert generator.get_containers("0.13") == []
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
    assert generator.get_containers("0.13") == ["addon-resizer-amd64:1.8.9"]
    get_repo.assert_called_once_with("charmed-kubernetes/bundle")
    get_dir_contents.assert_called_once_with("container-images")


@mock.patch("k8s_docs_tools.generate_release.get_charms", return_value=[])
@mock.patch("k8s_docs_tools.generate_release.get_containers", return_value=[])
def test_generate_component_page(mock_get_containers, mock_get_charms, tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    pw.generate_component_page()
    mock_get_charms.assert_called_with()
    mock_get_containers.assert_called_with("0.13")


def test_generate_release_notes_page(tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.generate_release_notes_page()
    expected = tmpdir / "pages" / "k8s" / "0.13" / "release-notes.md"
    assert expected.read_text("utf-8") == text
    assert text.endswith("\n")

    text = pw.generate_release_notes_page(as_str=True)
    assert text != expected.read_text("utf-8") and text in expected.read_text(
        "utf-8"
    ), "text should be a subset, not equal"


def test_generate_upgrading_page(tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.generate_upgrading_page()
    expected = tmpdir / "pages" / "k8s" / "0.13" / "upgrading.md"
    assert expected.read_text("utf-8") == text
    assert text.endswith("\n")


@mock.patch.object(
    generator,
    "check_output",
    mock.MagicMock(return_value="mock_snăp_info".encode("utf-8")),
)
@mock.patch.object(
    generator.PageWriter, "_bundle_table", mock.PropertyMock(return_value="mock-table")
)
def test_generate_supported_versions_page(tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.generate_supported_versions().decode("utf-8")
    expected = tmpdir / "pages" / "k8s" / "supported-versions.md"
    assert expected.read_text("utf-8") == text
    assert text.endswith("\n")
    assert "mock_snăp_info" in text
    assert "mock-table" in text


def test_empty_bundle_table(github_client, tmpdir):
    bundles = github_client.return_value.get_repo.return_value
    bundles.get_dir_contents.return_value = []
    text = generator.PageWriter("0.13", Path(tmpdir))._bundle_table
    assert text.splitlines() == [
        "| Kubernetes version | Charmed Kubernetes bundle |",
        "| --- | --- |",
    ]


def test_update_index(tmpdir):
    original_text = "- [Version 0.12]"
    index_file = tmpdir / "index.md"
    index_file.write_text(original_text, "utf-8")
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.update_index()
    assert index_file.read_text("utf-8") == text
    assert text.endswith("\n")
    assert text != original_text


@mock.patch.object(generator, "PageWriter", autospec=True)
def test_generate_release_docs(mock_page_writer, tmpdir):
    generator.generate_release_docs("0.13", Path(tmpdir))
    mock_page_writer.assert_called_once_with("0.13", Path(tmpdir))
    inst = mock_page_writer.return_value
    inst.generate_component_page.assert_called_once_with()
    inst.generate_release_notes_page.assert_called_once_with()
    inst.generate_upgrading_page.assert_called_once_with()
    inst.update_index.assert_called_once_with()
    inst.update_install_manual.assert_called_once_with()
    inst.append_release_notes.assert_called_once_with()
    inst.generate_supported_versions.assert_called_once_with()
