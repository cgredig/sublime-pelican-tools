import sublime
import sublime_plugin
import os
import re
from collections import Counter

def blog_tags_list():
	project_data = sublime.active_window().project_data()
	project_folder = project_data['folders'][0]['path']
	tags = []
	for root, dirs, files in os.walk(project_folder + "/konzertheld/content", topdown=False):
		for name in files:
			if name.endswith(".md"):
				with open(root + "/" + name) as f:
					content = f.readlines()
					content = [x.strip() for x in content]
					for line in content:
						#if line == "Status: Draft":
							#self.view.insert(edit, 0, name + "\n")
						if line.startswith("Tags:"):							
							tags.extend(line[5:].replace(" ", "").split(","))
	
	return Counter(tags)

class BlogRelatedTags(sublime_plugin.WindowCommand):
	def quick_panel(self, *args, **kwargs):
		self.window.show_quick_panel(*args, **kwargs)

	def run(self):
		self.tagslist = blog_tags_list()
		words = re.split(r'\W+', self.window.active_view().substr(sublime.Region(0, self.window.active_view().size())))
		words = [x.lower() for x in words]
		self.result = []
		for tagname in self.tagslist.keys():
			if tagname in words:
				self.result.append(tagname)

		self.quick_panel(
			self.result, self.panel_done,
			sublime.MONOSPACE_FONT
		)

	def panel_done(self, picked):
		active_editor = self.window.active_view()
		if active_editor:
			active_editor.run_command('insert', {'characters': self.result[picked]})


class PelicanTagsCountCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		project_data = sublime.active_window().project_data()
		project_folder = project_data['folders'][0]['path']
		tags = []
		for root, dirs, files in os.walk(project_folder + "/konzertheld/content", topdown=False):
			for name in files:
				if name.endswith(".md"):
					with open(root + "/" + name) as f:
						content = f.readlines()
						content = [x.strip() for x in content]
						for line in content:
							#if line == "Status: Draft":
								#self.view.insert(edit, 0, name + "\n")
							if line.startswith("Tags:"):							
								tags.extend(line[5:].replace(" ", "").split(","))
		
		tagslist = Counter(tags)
		words = re.split(r'\W+', self.view.substr(sublime.Region(0, self.view.size())))
		words = [x.lower() for x in words]
		
		for tagname, tagcount in tagslist.items():
			self.view.insert(edit, 0, tagname + ": " + str(tagcount) + "\n")
