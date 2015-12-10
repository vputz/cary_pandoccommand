Feature: Pandoc command
  Take an email message with one or more attachments and run pandoc on it

Scenario Outline: Basic pandoc command
  Given an email message <filename>
  Then the action should execute
  And create a transcribed <document>
  And write a response

  Examples:
  | filename           | document  |
  | simple_message.msg | test.html |



