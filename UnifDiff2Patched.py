import os
from unidiff import PatchSet

def getContentWOComments(lines,  subfix ):
	content = ""
	for line in lines:
		if iscomment(line):
			continue

		if line.startswith("-"):
			if subfix is "s":
				ln = line[1:]
				if not iscomment(ln):
					content += formatcomment(ln)
					continue

		if line.startswith("+"):
			if subfix is "t":
				ln = line[1:]
				if not iscomment(ln):
					content += formatcomment(ln)
					continue
		else:

			content += formatcomment(line)

	return content

def getContent(lines,  subfix ):
	content = ""
	for line in lines:

		if line.startswith("-"):
			if subfix is "s":
				ln = line[1:]
				content += (ln)
				continue

		if line.startswith("+"):
			if subfix is "t":
				ln = line[1:]
				content += (ln)
				continue
		else:
			content += (line)

	return content

def iscomment(line):
	tline = line.strip()
	return tline.startswith("//")

def formatcomment(line):

	if "//" in line:
		return line.split("//")[0] + "\n"
	return line

def save(out , name, lines, filename,  subfix):
	content = getContent(lines, subfix)
	pathout = os.path.join(out,name+"_"+filename+ "_"+subfix+ ".java")
	print("save {}".format(pathout))
	file_object = open(pathout, 'w')
	file_object.write(content)
	file_object.flush()
	file_object.close()

def saveHunk(out , name, lines, filename, hunkid, subfix):
	content = getContent(lines, subfix)
	pathout = os.path.join(out,name+"_"+filename+"_"+str(hunkid)+ "_"+subfix+ ".java")
	file_object = open(pathout, 'w')
	file_object.write(content)
	file_object.flush()
	file_object.close()

def getIndex(modifFiles):
	return modifFiles.source_file


def getIndex1(modifFiles):

	if modifFiles.source_file is not None:
		return modifFiles.source_file

	if modifFiles.patch_info is not None:
		for pi in modifFiles.patch_info:
			if pi.startswith("Index") or pi.startswith("--- "):
				return pi.replace("\n", "")


	return None


def patchSave(index,filename,patch, out, getnalenamefromfile = True):
	if len(patch.modified_files) == 0:
		return False

	for modifFiles in patch.modified_files:
		##See here

		patchfile = getIndex1(modifFiles)
		if not patchfile.endswith("java"):
				continue

		names = patchfile.split("/")
		name = names[len(names) - 1].replace(".java", "")

		for hunk in modifFiles:

			foldername = filename[:-8] #filename.replace(".diff.xz", "")

			folderoutdiff = os.path.join(out,index, foldername, name)
			if not os.path.exists(folderoutdiff):
				os.makedirs(folderoutdiff)

			save(folderoutdiff, foldername, hunk.source, name, "s")
			save(folderoutdiff, foldername, hunk.target, name,  "t")

	return True


def patchSaveWithhunk(filename,patch, out, getnalenamefromfile = True):
	if len(patch.modified_files) == 0:
		return False

	for modifFiles in patch.modified_files:
		hunkid = 0
		##See here

		patchfile = getIndex1(modifFiles)
		if not patchfile.endswith("java"):
				continue

		names = patchfile.split("/")
		name = names[len(names) - 1].replace(".java", "")

		for hunk in modifFiles:

			foldername = filename.replace(".diff", "")

			folderoutdiff = os.path.join(out, foldername, name)
			if not os.path.exists(folderoutdiff):
				os.makedirs(folderoutdiff)

			save(folderoutdiff, foldername, hunk.source, name, hunkid, "s")
			save(folderoutdiff, foldername, hunk.target, name, hunkid, "t")
			hunkid += 1


	return True

def runsingle(filename, input, output):
	file_object = open(input , 'r')
	patch = PatchSet(file_object)
	patchSave(filename,patch,output )

def runvisit(input, output, removeZipFile = False ):
	empty = []
	ok = 0
	for root, dirs, files in os.walk(input):
		for filename in files:
			if filename == ".DS_Store":
				continue

			index = os.path.basename(root)
			path = os.path.join(root, filename)
			print(path)

			#if int(index) > 6:
			#	continue

			if filename.endswith("xz"):
				#print("xz file")

				#if int(index) > 5:
				#	continue

				print("index %{}".format(index))

				try:
					import lzma
				except ImportError:
					print("error import")
					##from backports import lzma

				try:
					import codecs


					content = str((lzma.open(path).read().decode('utf-8','ignore')))
					#Original
					##content = str((lzma.open(path).read().decode('utf-8')))
					#content = str((lzma.open(path).read()))

					#content = unicode(lzma.open(path).read(errors="surrogateescape"), errors='ignore')
					#file_object = open(path, encoding = "ISO-8859-1")
					#content = file_object.read()
					patch = PatchSet(content)

					result = patchSave(index,index +"_" + filename,patch,output)
					if result is True:
						ok+=1
					else:
						empty.append(filename)

					if removeZipFile:
						os.remove(path)

				except Exception as e:
					print("error {}".format(e))
					print("error {} {}".format(e,filename))
					empty.append(path)

	print("END: # error {}, # ok {}".format(len(empty),ok))

def runvisitOLD(input, output):
	empty = []
	ok = 0
	for root, dirs, files in os.walk(input):
		for filename in files:
			if filename == ".DS_Store":
				continue

			path = os.path.join(root, filename)
			print(path)

			if filename.endswith("xz"):
				print("xz file")

				try:
					import lzma
				except ImportError:
					print("error import")
					##from backports import lzma

				content = (lzma.open(path).read())


			try:
				file_object = open(path, encoding = "ISO-8859-1")
				str = file_object.read()
				patch = PatchSet(str)

				result = patchSave(filename,patch,output)
				if result is True:
					ok+=1
				else:
					empty.append(filename)

			except Exception as e:
				print("error {} {}".format(e,filename))
				empty.append(path)

	print("error {} ok {}".format(len(empty),ok))

