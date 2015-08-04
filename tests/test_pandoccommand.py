from pytest_bdd import scenario, given, then
from cary_pandoccommand import PandocAction
from cary.parsed_email import ParsedEmail
import tempfile
import shutil
import os


@scenario('pandoccommand.feature', 'Basic pandoc command')
def test_pandoc_command():
    pass


@given('an email message with a body and attachments')
def pandocaction(request):
    message_text = """                                                                                                                                                                                                                                                               
MIME-Version: 1.0
Sender: vbputz@gmail.com
Received: by 10.96.179.170 with HTTP; Thu, 2 Jul 2015 08:33:57 -0700 (PDT)
Date: Thu, 2 Jul 2015 15:33:57 +0000
Delivered-To: vbputz@gmail.com
X-Google-Sender-Auth: xsC_n76tVTZgoqsWPaj9URbCxF0
Message-ID: <CADsvd-RzBFwFkMHtaHmvNTK4-Upkv3X+VD3XfJMka5=Z4wn9Ow@mail.gmail.com>
Subject: pandoc
From: Vic Putz <vputz@nyx.net>
To: Vic Putz <vbputz@gmail.com>
Content-Type: multipart/mixed; boundary=001a11c132f8fbf47b0519e62a97

--001a11c132f8fbf47b0519e62a97
Content-Type: text/plain; charset=UTF-8



--001a11c132f8fbf47b0519e62a97
Content-Type: text/markdown; charset=US-ASCII; name="test.md"
Content-Disposition: attachment; filename="test.md"
Content-Transfer-Encoding: base64
X-Attachment-Id: f_ibmew1tz0

VGVzdCBNYXJrZG93bgotLS0tLS0tLS0tLS0tCgpUZXN0IG1hcmtkb3duIQo=
--001a11c132f8fbf47b0519e62a97--"""
    tempworkingdir = tempfile.mkdtemp()
    os.mkdir(os.path.join(tempworkingdir, "transactions"))

    def fin():
        shutil.rmtree(tempworkingdir)
    request.addfinalizer(fin)
    result = PandocAction(ParsedEmail(message_text))
    result.set_config(dict(PANDOC_PATH='/usr/bin/pandoc',
                           TEXLIVE_PATH='/usr/bin'),
                      WORKSPACE_DIR=tempworkingdir,
                      FROM_ADDRESS="CaryTest <carytest@carytest.com>")
    return result


@then('the action should execute')
def execute_action(pandocaction):
    pandocaction.execute()


@then('create transcribed documents')
def check_output_attachments(pandocaction):
    expected = """<h2 id="test-markdown">Test Markdown</h2>
<p>Test markdown!</p>
"""
    attachments = [('test.html', expected)]
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
        with open(fnam) as f:
            contents = f.read()
            assert attachment[1] == contents
