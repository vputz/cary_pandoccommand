from pytest_bdd import scenario, given, then
from cary_pandoccommand import PandocAction
from cary.parsed_email import ParsedEmail
import tempfile
import shutil
import os



@scenario('pandoccommand.feature', 'Basic pandoc command')
def test_pandoc_command():
    pass

@given('an email message <filename>')
def pandocaction(request, filename):
    message_text = compdata(filename).decode("utf-8")
    tempworkingdir = tempfile.mkdtemp()
    os.mkdir(os.path.join(tempworkingdir, "transactions"))

    def fin():
        pass
        #shutil.rmtree(tempworkingdir)
    request.addfinalizer(fin)
    result = PandocAction(ParsedEmail(message_text))
    result.set_config(dict(PANDOC_PATH='/usr/bin/pandoc',
                           TEXLIVE_PATH='/usr/bin'),
                      WORKSPACE_DIR=tempworkingdir,
                      FROM_ADDRESS="CaryTest <carytest@carytest.com>")
    return result


def compdata(fnam):
    to_testfiles = os.path.abspath(
        os.path.join(os.path.split(__file__)[0], "test_data"))
    path = os.path.join(to_testfiles, fnam)
    with open(path, "rb") as f:
        result = f.read()
    return result


@then('the action should execute')
def execute_action(pandocaction):
    pandocaction.execute()
    if not pandocaction.command_is_valid:
        print(pandocaction.invalid_command_response)
    assert pandocaction.command_is_valid


@then('create a transcribed <document>')
def check_output_attachments(pandocaction, document):
    attachments = [(document, compdata(document))]
    check_attachments(pandocaction.output_dir, attachments)


@then('write a response')
def check_response(pandocaction):
    fnam = os.path.join(pandocaction.output_dir, 'message.txt')
    with open(fnam) as f:
        contents = f.read()
        message = ParsedEmail(contents)
        assert message.from_address == "carytest@carytest.com"
        assert message.subject == "Pandoc: your transcribed versions of test.md"
        assert message.body == "Please find enclosed the transcribed versions you requested of document 'test.md'."

attachments = [("text_1", "Hello, text 1!\n"),
               ("text_2", "Hello, text 2!\n")]


def check_attachments(base_path, attachments):
    for attachment in attachments:
        fnam = os.path.join(base_path, attachment[0])
        with open(fnam, "rb") as f:
            contents = f.read()
            assert attachment[1] == contents
