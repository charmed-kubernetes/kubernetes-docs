# -*- coding: utf-8 -*-

from pathlib import Path
import pytest
import unittest.mock as mock
import k8s_docs_tools.generate_release as generator
from types import SimpleNamespace
from typing import Mapping


@pytest.fixture(autouse=True)
def github_client():
    with mock.patch.object(generator, "Github") as mock_gh:
        yield mock_gh


def test_gh(github_client):
    generator.gh()
    github_client.assert_called_once_with(None)


def test_ver_to_tuple():
    assert generator._ver_to_tuple("1.2.3.4") == (1, 2, 3, 4)


@pytest.mark.parametrize(
    "ranges,expected",
    [
        ({"min": "0.12", "max": "0.15"}, True),
        ({"min": "0.14", "max": "0.15"}, False),
        ({"min": "0.12"}, True),
        ({"min": "0.14"}, False),
        ({"max": "0.15"}, True),
        ({"max": "0.12"}, False),
        ({"foo": "bar"}, True),
        (None, True),
    ],
    ids=[
        "within_min_and_max",
        "outside_min_and_max",
        "after_min",
        "before_min",
        "before_max",
        "after_max",
        "neither_ranges",
        "missing_ranges",
    ],
)
def test_within_channel_range(ranges: Mapping, expected: bool):
    assert generator.within_channel_range("0.13", ranges) is expected


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
    assert generator.get_charms("0.13") == expected
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
    mock_get_charms.assert_called_with("0.13")
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


@mock.patch.object(
    generator.PageWriter,
    "generate_release_notes_page",
    mock.MagicMock(return_value="# 0.13\nrelease-notes"),
)
@pytest.mark.parametrize("next_release", ["# 0.12", "# 0.13"])
def test_append_release_notes_page(tmpdir, next_release):
    original_text = "".join(
        [
            "<!-- AUTOGENERATE RELEASE NOTES HERE  -->\n",
            next_release + "\n",
        ]
    )
    release_notes = tmpdir / "pages" / "k8s" / "release-notes.md"
    Path(release_notes).parent.mkdir(parents=True)
    release_notes.write_text(original_text, "utf-8")
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.append_release_notes()
    assert release_notes.read_text("utf-8") == text
    assert text.endswith("\n"), "file should end with Line Feed"
    if "0.12" in next_release:
        assert text != original_text, "file contents should have changed"
    elif "0.13" in next_release:
        assert text == original_text, "file contents shouldn't change"
    assert "# 0.13" in text.splitlines()[1], "latest release is on line 2"
    assert text.count("# 0.13") == 1


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
def test_generate_supported_versions_page(tmpdir):
    pw = generator.PageWriter("0.13", Path(tmpdir))
    text = pw.generate_supported_versions().decode("utf-8")
    expected = tmpdir / "pages" / "k8s" / "supported-versions.md"
    assert expected.read_text("utf-8") == text
    assert text.endswith("\n")
    assert "mock_snăp_info" in text


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
    inst.append_release_notes.assert_called_once_with()
    inst.generate_supported_versions.assert_called_once_with()
