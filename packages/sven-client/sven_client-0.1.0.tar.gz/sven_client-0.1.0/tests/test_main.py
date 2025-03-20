"""
Unit tests for the main module.
"""

import argparse
from unittest.mock import MagicMock, patch

import pytest
from sven.cli.base import DotNotationArgumentParser
from sven.cli.main import main


class TestDotNotationArgumentParser:
    """Tests for the DotNotationArgumentParser class."""

    def test_parse_args_with_dot_notation(self):
        """Test parsing arguments with dot notation."""
        parser = DotNotationArgumentParser()
        with patch.object(argparse.ArgumentParser, "parse_args") as mock_parse_args:
            mock_parse_args.return_value = "parsed_args"

            # Test with dot notation
            result = parser.parse_args(["command.subcommand", "--option", "value"])

            # Verify the dot notation was expanded
            mock_parse_args.assert_called_once_with(
                ["command", "subcommand", "--option", "value"], None
            )
            assert result == "parsed_args"

    def test_parse_args_without_dot_notation(self):
        """Test parsing arguments without dot notation."""
        parser = DotNotationArgumentParser()
        with patch.object(argparse.ArgumentParser, "parse_args") as mock_parse_args:
            mock_parse_args.return_value = "parsed_args"

            # Test without dot notation
            result = parser.parse_args(["command", "--option", "value"])

            # Verify the arguments were passed through unchanged
            mock_parse_args.assert_called_once_with(
                ["command", "--option", "value"], None
            )
            assert result == "parsed_args"


class TestMain:
    """Tests for the main function."""

    @patch("sven.cli.base.DotNotationArgumentParser")
    def test_main_with_version_argument(self, mock_parser_class):
        """Test main function with --version argument."""
        # Setup mock parser
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser

        # Mock the parse_args method to simulate --version argument
        args = MagicMock()
        args.version = True
        mock_parser.parse_args.return_value = args

        # Call main with --version
        result = main(["--version"])

        # Verify parser was created with correct arguments
        mock_parser_class.assert_called_once()
        assert result == 0  # Successful exit

    @patch("sven.cli.base.DotNotationArgumentParser")
    def test_main_with_invalid_arguments(self, mock_parser_class):
        """Test main function with invalid arguments."""
        # Setup mock parser
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser

        # Mock the parse_args method to raise an error
        def side_effect(*args, **kwargs):
            raise SystemExit(2)

        mock_parser.parse_args.side_effect = side_effect

        # Call main with invalid arguments and catch the SystemExit
        with pytest.raises(SystemExit) as excinfo:
            main(["--invalid"])

        # Verify the exit code
        assert excinfo.value.code == 2
        # Verify parser was created
        mock_parser_class.assert_called_once()
