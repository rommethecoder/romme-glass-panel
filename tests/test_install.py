from pathlib import Path
import tempfile
import unittest
import manage


class Style(unittest.TestCase):
    def test_assets(self):
        self.assertEqual(manage.check()["KPlugin"]["Id"], manage.ID)

    def test_install_remove_and_collision(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = manage.install(tmp)
            self.assertTrue(dest.is_dir())
            with self.assertRaises(ValueError):
                manage.install(tmp)
            manage.uninstall(tmp)
            self.assertFalse(dest.exists())

    def test_preserve_unmanaged_style(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = manage.target(tmp)
            dest.mkdir(parents=True)
            (dest / "personal-file").write_text("keep")
            with self.assertRaises(ValueError):
                manage.uninstall(tmp)
            self.assertEqual((dest / "personal-file").read_text(), "keep")

    def test_reject_modified_install(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = manage.install(tmp)
            (dest / "extra").write_text("keep")
            with self.assertRaises(ValueError):
                manage.uninstall(tmp)

    def test_reject_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            link = Path(tmp) / "link"
            link.symlink_to(tmp, target_is_directory=True)
            with self.assertRaises(ValueError):
                manage.install(link)

    def test_preserve_modified_svg(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = manage.install(tmp)
            asset = dest / "widgets/panel-background.svg"
            asset.write_text(asset.read_text() + "<!-- personal edit -->")
            with self.assertRaises(ValueError):
                manage.uninstall(tmp)
