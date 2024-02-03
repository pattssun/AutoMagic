#!/usr/bin/env python
# coding=utf-8

from aeneas.executetask import ExecuteTask
from aeneas.task import Task

# create Task object
config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
task = Task(config_string=config_string)
task.audio_file_path_absolute = u"output/body_audio.mp3"
task.text_file_path_absolute = u"body.txt"
task.sync_map_file_path_absolute = u"output/syncmap.json"

# process Task
ExecuteTask(task).execute()

# output sync map to file
task.output_sync_map_file()