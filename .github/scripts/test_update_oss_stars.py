import importlib.util
import pathlib
import unittest


SCRIPT = pathlib.Path(__file__).with_name("update_oss_stars.py")
SPEC = importlib.util.spec_from_file_location("update_oss_stars", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UpdateOssStarsTest(unittest.TestCase):
    def test_updates_star_count_for_matching_repository_row(self):
        readme = (
            "| Project | Stars | About |\n"
            "| --- | ---: | --- |\n"
            "| [Tiptap](https://github.com/ueberdosis/tiptap) | 1 | Editor |\n"
        )

        updated = MODULE.update_readme(readme, {"ueberdosis/tiptap": 38023})

        self.assertIn("| [Tiptap](https://github.com/ueberdosis/tiptap) | 38,023 | Editor |", updated)


if __name__ == "__main__":
    unittest.main()
