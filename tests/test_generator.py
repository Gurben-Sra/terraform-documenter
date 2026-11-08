"""Tests for Terraform documentation generation."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from tf_doc_gen.cli import main, merge_generated_section
from tf_doc_gen.generator import generate_readme, scan_module


class GeneratorTests(unittest.TestCase):
    def test_scan_and_render_module_documentation(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tf").write_text(
                '''terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "subnet_id" {
  type        = string
  description = "Subnet for the instance"
}

resource "aws_instance" "web" {
  subnet_id = aws_subnet.public.id
}

resource "aws_subnet" "public" {
  vpc_id = "vpc-example"
}

output "instance_id" {
  value       = aws_instance.web.id
  description = "Created instance identifier"
  sensitive   = true
}
''',
                encoding="utf-8",
            )
            (root / "examples" / "basic").mkdir(parents=True)
            (root / "examples" / "basic" / "main.tf").write_text(
                'module "web" { source = "../.." }\n', encoding="utf-8"
            )

            readme = generate_readme(scan_module(root))

        self.assertIn("`subnet_id`", readme)
        self.assertIn("Required", readme)
        self.assertIn("`instance_id`", readme)
        self.assertIn("aws_instance.web", readme)
        self.assertIn("-->", readme)
        self.assertNotIn("module.web", readme)
        self.assertIn("Terraform: `>= 1.5.0`", readme)
        self.assertIn("Provider `aws`: source `hashicorp/aws`, version `~> 5.0`", readme)
        self.assertIn("examples/basic/main.tf", readme)
        self.assertIn("Breaking Changes", readme)

    def test_generated_section_preserves_authored_readme_and_is_replaceable(self) -> None:
        existing = "# My module\n\nAuthored notes.\n"
        first = merge_generated_section(existing, "Generated v1\n")
        updated = merge_generated_section(first, "Generated v2\n")

        self.assertIn("Authored notes.", updated)
        self.assertNotIn("Generated v1", updated)
        self.assertIn("Generated v2", updated)

    def test_scan_command_writes_generated_readme(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "main.tf").write_text(
                'variable "region" {\n  type = string\n}\n', encoding="utf-8"
            )
            (root / "README.md").write_text("# Existing notes\n", encoding="utf-8")

            self.assertEqual(main(["scan", str(root)]), 0)
            first = (root / "README.md").read_text(encoding="utf-8")
            self.assertEqual(main(["scan", str(root)]), 0)
            second = (root / "README.md").read_text(encoding="utf-8")

        self.assertIn("# Existing notes", second)
        self.assertIn("`region`", second)
        self.assertEqual(second.count("<!-- tf-doc-gen:start -->"), 1)
        self.assertEqual(first.count("<!-- tf-doc-gen:start -->"), 1)


if __name__ == "__main__":
    unittest.main()
