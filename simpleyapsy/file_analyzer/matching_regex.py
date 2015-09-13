# NOTE: UNTESTED!
class PluginFileAnalyzerMathingRegex(object):
	"""
	An analyzer that targets plugins decribed by files whose name match a given regex.
	"""
	def __init__(self, regexp):
		self.regexp = regexp
	
	def isValidPlugin(self, filename):
		"""
		Checks if the given filename is a valid plugin for this Strategy
		"""
		reg = re.compile(self.regexp)
		if reg.match(filename) is not None:
			return True
		return False
	
	def getInfosDictFromPlugin(self, dirpath, filename):
		"""
		Returns the extracted plugin informations as a dictionary.
		This function ensures that "name" and "path" are provided.
		"""
		# use the filename alone to extract minimal informations.
		infos = {}
		module_name = os.path.splitext(filename)[0]
		plugin_filename = os.path.join(dirpath,filename)
		if module_name == "__init__":
			module_name = os.path.basename(dirpath)
			plugin_filename = dirpath
		infos["name"] = "%s" % module_name
		infos["path"] = plugin_filename
		cf_parser = ConfigParser()
		cf_parser.add_section("Core")
		cf_parser.set("Core","Name",infos["name"])
		cf_parser.set("Core","Module",infos["path"])
		return infos,cf_parser
