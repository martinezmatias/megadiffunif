import unittest
from UnifDiff2Patched import  *

import sys
#reload(sys)
#sys.setdefaultencoding("utf-8")

class UnifDiff2PatchedTest(unittest.TestCase):



	def testUnifDiff2Patched(self):
		input = '/Users/matias/develop/megadiffs'
		output = '/Users/matias/develop/sketch-repair/outmegadiff2/'#'./outMegadiff/'
		runvisit(input,output)

	def testUnifDiff2PatchedNew(self):
		input = '/Users/matias/develop/newAstorexecution/megadiff-last-zip/'
		output = '/Users/matias/develop/newAstorexecution/megadiff-expansion-temp/'
		print("Start conversion megadiff")
		runvisit(input,output)

	def _testRun150611(self):
		file_object  = open('/Users/matias/develop/sketch-repair/svn-diff.d/150611.diff'
			, 'r')

		patch = PatchSet(file_object)
		pi = 0
		for patchfile in patch.modified_files:

			print("patch info {} {}".format(pi,patchfile.patch_info))
			hi = 0
			for hunk in patchfile:
				print("hunk nr {}".format(hi))
				print(getContent(hunk.source, "s"))
				print(getContent(hunk.target, "t"))
				hi+=1

			pi+=1

	def testRun2_Math101(self):
			runsingle('math-101','/Users/matias/develop/overfitting-research/git-overfitting-analysis/data/Training/patches/Cardumen/Math/101/patch1-Math-101-Cardumen-full-context.diff',"/tmp/" )


	def _testRun2_150611(self):
			runsingle('150611','/Users/matias/develop/sketch-repair/svn-diff.d/150611.diff',"/tmp/" )

	def _testRun2_990(self):
		runsingle("990",
			"/Users/matias/develop/sketch-repair/git-sketch4repair/datasets/CodeRep/unified_diffs/Dataset1_unidiff/990.diff","/tmp/" )

	def _testRun986499(self):
		file_object = open('/Users/matias/develop/sketch-repair/svn-diff.d/986499.diff'
						   , 'r')

		patch = PatchSet(file_object)

		for patchfile in patch.modified_files:
			# patchfile = patch.modified_files[0]
			for hunk in patchfile:
				print(getContent(hunk.source, "s"))
				print(getContent(hunk.target, "t"))

if __name__ == '__main__':
	unittest.main()
