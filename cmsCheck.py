#encoding:utf8
import sys
import threading
import os
import getopt
import urlparse
import requests

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
reload(sys)
sys.setdefaultencoding("utf8")

def check(url, fp):
	headers = {
	"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
	# "Referer":url
	}

	while True:
		count = 0
		try:
			if count >= 5:
				break
			pro = {}
			#pro = {"https":"http://127.0.0.1:8080"}
			r = requests.get(url, headers = headers, timeout = 10, proxies = pro, verify = False)
			mycheck(r, url, fp)
			break
		except:
			pass
		count += 1


def iter_files(rootDir, paths):
    #遍历根目录
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            file_name = os.path.join(root,file)
            paths.append(file_name)
        for dirname in dirs:
            #递归调用自身,只改变目录名称
            iter_files(dirname, paths)
def mycheck(r, url, fp):
	print url+"########"+str(r.status_code)
	if r.status_code == 404:
		return False
	else:
		fp.write(url+"******"+str(r.status_code)+"\r\n")
		fp.flush()
		return True
if __name__ == '__main__':
	if len(sys.argv) >= 5:
		url = "http://jxlts6.com"
		mypath = "/Users/evilangel/Documents/software/chat/chat"
		limit = 10
		file_name = ""
		try:
			options, args = getopt.getopt(sys.argv[1:], "u:c:l:o:h", ["help", "limit="])
		except getopt.GetoptError:
			sys.exit()
		for option, value in options:
			if option in ("-h", "--help"):
				print "example: python cmsCheck.py -u http://target.com -c /tmp/xxcms --limit 10 -o savepath"
			if option in ("-u"):
				url = value
			if option in ("-c"):
				mypath = value
			if option in ("-l","--limit"):
				limit = value
			if option in ("-o"):
				file_name = value
		paths = []
		iter_files(mypath,paths)
		if file_name == "":
			url_change = urlparse.urlparse(url)
			print url_change
			file_name = str(url_change.netloc).replace(".","_")
		fp = open("result/"+file_name,"w")
		tasks = []
		for p in paths:
			t = p.replace(mypath, "")
			u = url + t
			task = threading.Thread(target=check, args=(u, fp,))
			tasks.append(task)
		runningTasks = []
		while len(tasks) > 0:
			for t in tasks:
				if len(runningTasks) < limit:
					tasks.remove(t)
					runningTasks.append(t)
					t.start()
				else:
					for k in runningTasks:
						if k.isAlive() == False:
							runningTasks.remove(k)

		for t in runningTasks:
			t.join()
		fp.close()
	else:
		print "example: python cmsCheck.py -u http://target.com -c /tmp/xxcms --limit 10 -o savepath"


