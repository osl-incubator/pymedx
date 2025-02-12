"""Test helpers module."""

from xml.etree.ElementTree import Element, SubElement

from pymedx.helpers import batches, getContent


class TestHelpers:
    """Test the helpers module."""

    def test_batches(self):
        """Test the batches function."""
        input_list = [
            str(i) for i in range(10)
        ]  # Example list ['0', '1', ..., '9']
        batch_size = 3
        expected_batches = [
            ["0", "1", "2"],
            ["3", "4", "5"],
            ["6", "7", "8"],
            ["9"],
        ]

        # Execute
        generated_batches = list(batches(input_list, batch_size))

        # Verify
        assert generated_batches == expected_batches, (
            "Batches not generated as expected."
        )

    def test_get_content(self):
        """Test the getContent function."""
        # Dynamically create XML structure
        root = Element("root")
        child_with_text = SubElement(root, "child1")
        child_with_text.text = "example text"
        child_without_text = SubElement(root, "child2")

        # Test retrieving existing text
        assert getContent(root, "child1") == "example text"

        # Test default value when no text is present
        child_without_text.text = None  # Ensuring the child has no text
        assert getContent(root, "child2", default="default text") == ""
        assert (
            getContent(root, "child_x", default="default text")
            == "default text"
        )

        # Test separator functionality
        another_child_with_text = SubElement(root, "child3")
        another_child_with_text.text = "another example"
        assert getContent(root, "child3", separator=", ") == "another example"
