from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponse
from textwrap import wrap
from copy import deepcopy
import json,time,datetime
import subprocess
import random

try:
    HOSTNAME = url('index')
except:
    HOSTNAME = 'http://localhost'

def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

VERSION=get_git_revision_hash()
print("Running git commit version {0} ".format(VERSION))


information = '''
<h1>How to use:</h1>
<p>
Up to 4 different forms can be added to webformsut page. Every form  can be configed with a &lt;form string&gt; 
consisting of one or more 3 letter codes as defined below. 

</p>
<p>
HOSTNAME/forms/&lt;form string 1&gt;<br />
HOSTNAME/forms/&lt;form string 1&gt;/&lt;form string 2&gt;<br />
HOSTNAME/forms/&lt;form string 1&gt;/&lt;form string 2&gt;/&lt;form string 3&gt;<br />
HOSTNAME/forms/&lt;form string 1&gt;/&lt;form string 2&gt;/&lt;form string 3&gt;/&lt;form string 4&gt;<br />
</p>
<hr />

'''.replace("HOSTNAME", HOSTNAME)


formInput = {
	'cb0': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox0"},
	'cb1': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox1"},
	'cb2': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox2"},
	'cb3': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox3"},
	'cb4': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox4"},
	'cb5': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox5"},
	'cb6': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox6"},
	'cb7': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox7"},
	'cb8': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox8"},
	'cb9': {'type':'checkbox', 'name': 'checkbox', 'value': "checkbox9"},
	'col': {'type':'color', 'name': 'color', 'label': "Pick your color" },
	'da1': {'type':'date', 'name': 'begin date', 'label':"Begin date" },
	'da2': {'type':'date', 'name': 'end date'},
	'da3': {'type':'date', 'name': 'birthday', 'label':'birthday'},
	'da4': {'type':'date', 'name': 'birthday'},
	'ema': {'type':'email', 'name': 'email', 'placeholder': 'Enter your e-mail'},
	'nf1': {'type':'text', 'name': 'firstname', 'maxlength': '10' , 'placeholder': 'Enter your first name' },
	'nf2': {'type':'text', 'name': 'firstname', 'maxlength': '20' , 'value': 'Ramon', 'placeholder': 'Enter your first name' },
	'nl1': {'type':'text', 'name': 'lastname', 'maxlength': '20'},
	'pas': {'type':'password', 'name': 'password', 'placeholder': 'Enter your password' },
	'res': {'type':'reset', 'name': 'reset' },
	'sea': {'type':'search', 'name': 'search'},
	'tel': {'type':'tel', 'name': 'phone','placeholder': 'Enter your phone number' },
	'tex': {'type':'text', 'name': 'text'},
	'tim': {'type':'time', 'name': 'time'},
	'url': {'type':'url', 'name': 'url', 'placeholder': 'Enter your url' },
	'usr': {'type':'text', 'name': 'username', 'placeholder': 'Enter your username' },
	'wee': {'type':'week', 'name': 'week'},
}


def get_client_ip(request):
    """get the client ip from the request
    """
    #remote_address = request.META.get('REMOTE_ADDR')
    remote_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
    # set the default value of the ip to be the REMOTE_ADDR if available
    # else None
    ip = remote_address
    # try to get the first non-proxy ip (not a private ip) from the
    # HTTP_X_FORWARDED_FOR
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        # remove the private ips from the beginning
        while (len(proxies) > 0 and proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
            # take the first ip which is not a private one (of a proxy)
            if len(proxies) > 0:
                ip = proxies[0]
    return ip


def random_formstring (formInput):
	max_fields = len(formInput)
	for i in range (random.randrange(max_fields)+1):
		print(i)
	

def create_form(formstring):
	'''
	Create web form from the formstring.
	The formstring is wrapped every 3 chars.
	'''
	begin_epoch=float(time.time())
	form = ''
	id_counts = dict()
	name_counts = dict()
	random_formstring (formInput)
	formset = wrap(formstring,3)
	for i in formset:
		form_item = ''
		label_item = ''
		id_item = ''
		if i in id_counts:
			id_counts[i] += 1
		else:
			id_counts[i] = 1
		if i in formInput:
			if id_counts[i] > 1:
				id_item=i + '_'+str(id_counts[i])
			else:
				id_item=i
			form_item = '<input id="' + id_item + '" '
			for j in formInput[i]:
				if j.lower() == 'name':
					if formInput[i][j] in name_counts:
						name_counts[formInput[i][j]] += 1
						form_item = form_item + j  +  '="' + formInput[i][j]+ '_' + str(name_counts[formInput[i][j]]) + '" '
					else:
						name_counts[formInput[i][j]] = 1
						form_item = form_item + j  +  '="' + formInput[i][j]+ '" '
				elif j.lower() == 'label':
					label_item=str(formInput[i][j])
				else:
					form_item = form_item + j +  '="' + formInput[i][j]+ '" '
			if label_item != '':
				form = form + '<label for="'+id_item+ '">'+label_item + ': </label>' 
			form = form + form_item +'> </br> \n'
		else:
			print("WARNING: unknown field '{}', skipping".format(i))
	form = form + '<input type="hidden" name="formstring" id="formstring" value="{}">\n'.format(formstring)
	form = form + '<input type="hidden" name="begin_epoch" id="begin_epoch" value="{}">\n'.format(begin_epoch)
	form = form + '<input type="submit" value="Submit" />\n'
	return form


# Create your views here.

def index(request,formstring1="",formstring2="",formstring3="",formstring4=""):
	rawPost=None

	form1, form2, form3, form4 = '', '', '',''
	if formstring1 != "":
		form1 = create_form(formstring1)
		print(form1)
	if formstring2 != "":
		form2 = create_form(formstring2)
		print(form2)
	if formstring3 != "":
		form3 = create_form(formstring3)
		print(form3)
	if formstring4 != "":
		form4 = create_form(formstring4)
		print(form4)

	context = { 'form1': form1, 'form2': form2, 'form3': form3, 'form4':form4, 'rawpost':rawPost, 'version': VERSION}

	if formstring1 == "" and formstring2 == "" and formstring3 == "" and formstring4 == "":
		rawPost=formInput
		context = {'rawpost': rawPost, 'information': information, 'version': VERSION}

	if request.method =='POST':
		rawPost = deepcopy(request.POST)
		del rawPost['csrfmiddlewaretoken'] # remove csrfmiddlewaretoken, unneeded information 
		end_epoch = float(time.time())
		rawPost['end_epoch']=end_epoch
		# try to calculate delta_epoch.
		try:
			begin_epoch=float(rawPost['begin_epoch'])
			delta_epoch = end_epoch-begin_epoch
			rawPost['delta_epoch']=delta_epoch
		except:
			print('Warning: Cannot calculate delta_epoch')
		rawPost['datetime']=str(datetime.datetime.now())

		print(json.dumps(rawPost))
		# return a back link
		backlink ="<a href='{0}'>return to form</a>".format(request.path)
		context = { 'backlink': backlink, 'rawpost': rawPost, 'version': VERSION}
		return render(request,'forms/form.html', context)

	return render(request,'forms/form.html', context)
