import urllib.request

print('Beginning file download with urllib2...')

url = 'https://new.mospolytech.ru/upload/files/mfc-blank/На%20выход%20из%20академического%20отпуска.pdf'


print("       ",url)
urllib.request.urlretrieve(url, '/Users/andreybesedin/PycharmProjects/tlgm_Politech/cat.jpg')