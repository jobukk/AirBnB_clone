import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
from console import HBNBCommand
from models import storage


class TestHBNBCommand(unittest.TestCase):

    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        self.console = None

    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.emptyline()
            self.assertEqual(fake_out.getvalue(), '')

    def test_do_quit(self):
        self.assertTrue(self.console.do_quit(''))

    def test_help_quit(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.help_quit()
            self.assertIn(
                "Quit command to exit the program",
                fake_out.getvalue()
            )

    def test_do_create(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_create("BaseModel")
            output = fake_out.getvalue().strip()
            self.assertTrue(len(output) > 0)

    def test_do_show(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_show("")
            self.assertIn("** class name missing **", fake_out.getvalue())

    def test_do_destroy(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_destroy("")
            self.assertIn("** class name missing **", fake_out.getvalue())

    def test_do_all(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_all("")
            self.assertIn("** class name missing **", fake_out.getvalue())

    def test_do_update(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.do_update("")
            self.assertIn("** class name missing **", fake_out.getvalue())

    def test_default_unknown_syntax(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("UnknownClass.unknownMethod()")
            self.assertIn("*** Unknown syntax:", fake_out.getvalue())

    def test_default_all(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("BaseModel.all()")
            self.assertIn("[]", fake_out.getvalue())

    def test_default_count(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("BaseModel.count()")
            self.assertIn("0", fake_out.getvalue())

    def test_default_show(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("BaseModel.show('123')")
            self.assertIn("** instance id missing **", fake_out.getvalue())

    def test_default_destroy(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("BaseModel.destroy('123')")
            self.assertIn("** instance id missing **", fake_out.getvalue())

    def test_default_update(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.default("BaseModel.update('123', {'name': 'test'})")
            self.assertIn("** instance id missing **", fake_out.getvalue())


if __name__ == '__main__':
    unittest.main()
    with patch('sys.stdout', new=StringIO()) as f:
        HBNBCommand().onecmd("help show")
