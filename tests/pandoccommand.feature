Feature: Pandoc command
  Take an email message with one or more attachments and run pandoc on it

Scenario: Basic pandoc command
  Given an email message with a body and attachments
  Then the action should execute
  And create transcribed documents
  And write a response
