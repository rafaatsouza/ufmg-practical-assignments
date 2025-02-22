import io
import time
import re as regex
from git import Repo
import os
import ComplexCalc as cc

class GitPyService:
	def __init__(self, path, url):
		self.path = path
		self.url = url
		self.repo = self.InitializeRepo(path, url)

	def InitializeRepo(self, path, url):
		if path != '':
			folder = path
		else:
			folder = './' + url.split('/')[-1].split('.')[0]
			try:
				Repo.clone_from(url, folder)
			except:
				print("")

		return Repo(folder)

	def GetCommitYear(self, element):
		return time.strftime("%Y", time.gmtime(element.committed_date))

	def IsInYearInterval(self, yearFrom, yearTo, setYear):
		return (yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo)

	def GetTotalCommits(self, yearFrom="1969", yearTo="2020", message=""):
		allCommits = self.repo.iter_commits()
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(((yearFrom=="1969" and yearTo=="2020") or (setYear>=yearFrom and setYear<=yearTo))
					 and (message == "" or element.message.find(message)>=0)):
					count = count + 1
			except StopIteration:
				break
		print ('Total number of commits: {}'.format(count))

	def GetTopCommiters(self, yearFrom="1969", yearTo="2020", max=10):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if (self.IsInYearInterval(yearFrom, yearTo, setYear)):
					if element.author.name in dictionary:
						dictionary[element.author.name] = dictionary[element.author.name] + 1
					else:
						dictionary[element.author.name] = 1
			except StopIteration:
				break
		print('Top %d Committers (from %s to %s):' % (max, yearFrom, yearTo))
		for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
			print (key, value)
			count = count + 1
			if count == max:
				break

	def GetNumberOfEdits(self, add=True, searchString='List<', yearFrom='1969', yearTo='2020'):
		allCommits = self.repo.iter_commits()
		total = 0
		if(add):
			searchRegex = r"\+.*" + regex.escape(searchString) + r".*\n"
		else:
			searchRegex = r"\-.*" + regex.escape(searchString) + r".*\n"
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(self.IsInYearInterval(yearFrom, yearTo, setYear)):
					nextCommit = next(allCommits)
					diff = self.repo.git.diff(element, nextCommit)
					allLists = regex.findall(searchRegex, diff)
					total = total + len(allLists)
			except StopIteration:
				print("Number of \'%s\' Edits: %d %s" % (searchString, total, "adds" if add else "removes"))
				break

	def GetMostModifiedFiles(self, yearFrom="1969", yearTo="2020", extension=".cs", max=5):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		count = 0
		while True:
			try:
				element = next(allCommits)
				setYear = self.GetCommitYear(element)
				if(self.IsInYearInterval(yearFrom, yearTo, setYear)):
					for key in element.stats.files:
						if key.endswith(extension):
							if key in dictionary:
								dictionary[key] = dictionary[key] + 1
							else:
								dictionary[key] = 1
			except StopIteration:
				break
		print("Top %d modified files with extension %s (from %s to %s):" % (max, extension, yearFrom, yearTo))
		for key, value in sorted(dictionary.items(), key=lambda kv: kv[1], reverse=True):
			print (key, value)
			count = count + 1
			if count == max:
				break

	def GetCountFilesFirstAndLastCommits(self, folderPath, fileType=""):
		self.repo.git.checkout('master')
		allCommits = self.repo.iter_commits()
		element = next(allCommits)
		count = 0
		self.repo.git.checkout(element)
		for root, directory, files in os.walk(folderPath):
			for file in files:
				if(fileType != "" and file.endswith(fileType)):
					count += 1
				elif(fileType==""):
					count += 1
		print('Number of files on latest commit: ', count)
		while True:
			try:
				element = next(allCommits)
			except StopIteration:
				break
		count = 0
		self.repo.git.checkout(element)
		for root, directory, files in os.walk(folderPath):
			for file in files:
				if(fileType != "" and file.endswith(fileType)):
					count += 1
				elif(fileType==""):
					count += 1
		print('Number of files on first commit: ', count)

	def GetCountFilesByCommit(self, folderPath, fileType="All"):
		self.repo.git.checkout('master')
		allCommits = self.repo.iter_commits()
		fileCountList = []
		while True:
			try:
				element = next(allCommits)
				self.repo.git.checkout(element)
				fileCount = 0
				for root, directory, files in os.walk(folderPath):
					for file in files:
						if fileType != "All" and file.endswith(fileType):
							fileCount +=1
						elif fileType == "All":
							fileCount +=1
				fileCountList.append(fileCount)
			except StopIteration:
				break
		print(fileType, 'Files per commit: ')
		print(fileCountList)

	def GetLinesByFile(self, folderPath, fileType='.cs'):
		self.repo.git.checkout('master')
		allCommits = self.repo.iter_commits()
		fullList = []
		while True:
			try:
				commit = next(allCommits)
				commitLines = {}
				self.repo.git.checkout(commit)
				for root, directory, files in os.walk(folderPath):
					for file in files:
						if not file.endswith(fileType):
							continue
						fullPath = os.path.join(root, file)
						with open(fullPath, 'rU') as f:
							num_lines = sum(1 for line in f)
							commitLines[fullPath] = num_lines
				fullList.append(commitLines)
			except StopIteration:
				break
		print(fullList)

	def GetCountFilesByYear(self, folderPath, fileType="All"):
		self.repo.git.checkout('master')
		allCommits = self.repo.iter_commits()
		latestCommit = next(allCommits)
		dictionary = {}
		lastYear = self.GetCommitYear(latestCommit)
		allCommits = self.repo.iter_commits()
		yearMax = 0
		while True:
			try:
				element = next(allCommits)
				self.repo.git.checkout(element)
				fileCount = 0
				year = self.GetCommitYear(element)
				if lastYear != year:
					dictionary[lastYear] = yearMax
					yearMax = 0
					lastYear = year
				for root, directory, files in os.walk(folderPath):
					for file in files:
						if fileType != "All":
							if file.endswith(fileType):
								fileCount += 1
						else:
							fileCount += 1
				if yearMax < fileCount:
					yearMax = fileCount
			except StopIteration:
				dictionary[lastYear] = yearMax
				break
		print (dictionary)

	def GetCommitedFilesByYear(self, folderPath, fileType):
		allCommits = self.repo.iter_commits()
		dictionary = {}
		while True:
			try:
				element = next(allCommits)
				self.repo.git.checkout(element)
				year = self.GetCommitYear(element)
				for file in element.stats.files:
					if not file.endswith(fileType):
						continue
					try:
						targetfile = element.tree / file
					# files not found
					except KeyError:
						continue
					with io.BytesIO(targetfile.data_stream.read()) as f:
						num_lines = sum(1 for line in f)
					if year not in dictionary and file.endswith(fileType):
							dictionary[year] = num_lines
					elif year in dictionary and file.endswith(fileType):
						dictionary[year] = dictionary[year] + num_lines
			except StopIteration:
				break
		print (dictionary)

	def GetAllFilesByYear(self, folderPath, fileType):
		self.repo.git.checkout('master')
		allCommits = self.repo.iter_commits()
		dictionary = {}
		while True:
			try:
				element = next(allCommits)
				self.repo.git.checkout(element)
				year = self.GetCommitYear(element)
				for root, directory, files in os.walk(folderPath):
					for file in files:
						if(file.endswith(fileType)):
							fullPath = os.path.join(root, file)
							with open(fullPath, 'rU') as f:
								num_lines = sum(1 for line in f)
							if year not in dictionary and file.endswith(fileType):
									dictionary[year] = num_lines
							elif year in dictionary and file.endswith(fileType):
								dictionary[year] = dictionary[year] + num_lines
			except StopIteration:
				break
		print (dictionary)

	def GetCommitedComplexityMetrics(self, commit, folderPath, fileType='.cs'):
		self.repo.git.checkout(commit)
		craDic = {}
		ctaDic = {}
		mcaDic = {}
		complexCalc = cc.ComplexCalc()

		for root, directory, files in os.walk(folderPath):
			for file in files:
				if(file.endswith(fileType)):
					fullPath = os.path.join(root, file)
					craDic[fullPath] = complexCalc.GetCRAByIndent(fullPath)
					ctaDic[fullPath] = complexCalc.GetCTAByIndent(fullPath)
					mcaDic[fullPath] = complexCalc.GetMCAByIndent(fullPath)
		print('Highest CRA:\n', sorted(craDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[0], '\n')
		print('Highest CTA:\n', sorted(ctaDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[0], '\n')
		print('Highest MCA:\n', sorted(mcaDic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True)[0], '\n')
