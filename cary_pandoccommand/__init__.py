from cary.carycommand import CaryCommand, CaryAction
import os
import logging
from subprocess import call

"""
A command to run pandoc on the attachment(s)
"""

class PandocCommand(CaryCommand):

    @property
    def name(self):
        return "pandoc"

    @property
    def description(self):
        return "Use pandoc to convert markdown documents"

    @property
    def required_attachments(self):
        return ["sourcedoc.md", "support1.file", "support2.file..."]

    def _create_action(self, parsed_message):
        return PandocAction(parsed_message)


class PandocAction(CaryAction):

    def __init__(self, parsed_message):
        super().__init__(parsed_message)

    def validate_command(self):
        # pandoc should at least have one attachment and we hope it is valid markdown
        self.command_is_valid = False
        if len(self._attachments) > 0:
            if len (self._attachments) == 1:
                self.command_is_valid = True
            else:
                for attachment in self._attachments:
                    fnam_root, fnam_ext = os.path.splitext(os.path.split(attachment)[-1])
                    if fnam_ext == ".md":
                        self.command_is_valid = True
                if not self.command_is_valid:
                    self.invalid_command_response = """
I'm sorry, pandoc with multiple files requires one of them to have a markdown (.md) suffix.
"""
                
        else:
            self.invalid_command_response = """
I'm sorry, pandoc requires an input document, and I did not see one in your email.
"""

    def execute_action(self):
        source_path = self._attachments[0]
        self._output_filenames = []
        for filetype, suffix in (('epub', 'epub'),
                                 ('docx', 'docx'),
                                 ('latex', 'pdf'),
                                 ('html', 'html')):
            self.convert_to(filetype, suffix)

    def output_path(self, suffix):
        base_fnam = os.path.split(self.source_file())[-1]
        fnam_root, fnam_ext = os.path.splitext(base_fnam)
        return os.path.join(self.output_dir, fnam_root+"."+suffix)

    def source_file(self):
        result = None
        if len(self._attachments) == 1:
            result = self._attachments[0]
        else:
            for attachment in self._attachments:
                fnam_root, fnam_ext = os.path.splitext(os.path.split(attachment)[-1])
                if fnam_ext == ".md":
                    result = attachment
        return result

    def convert_to(self, filetype, suffix):
        source = self.source_file()
        print("SOURCE FILE "+self.source_file())
        print("WD " + self.working_dir)
        target = self.output_path(suffix)
        command_list = [self.config['PANDOC_PATH'],
                        '-f', 'markdown', '-t', filetype, '-o',
                        target, source]
        self._output_filenames.append(target)
        call_result = call(command_list, env=self.execution_environment(), 
                           cwd=os.path.join(self.working_dir, "input"))
        logging.log(logging.INFO, " ".join(command_list)
                    + "::" + str(call_result) + "\n")

    def execution_environment(self):
        result = os.environ.copy()
        result['PATH'] = self.config['TEXLIVE_PATH']+':'+os.environ['PATH']
        return result

    @property
    def response_subject(self):
        return "Pandoc: your transcribed versions of {0}".format(
            os.path.split(self._attachments[0])[-1])

    @property
    def response_body(self):
        return "Please find enclosed the transcribed versions you requested of document '{0}'.".format(
            os.path.split(self._attachments[0])[-1])
