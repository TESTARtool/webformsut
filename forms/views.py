from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.http import HttpResponse
from textwrap import wrap
from copy import deepcopy
import json,time,datetime
import subprocess


def get_git_revision_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

VERSION=get_git_revision_hash()
print("Running git commit version {0} ".format(VERSION))

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
	'col': {'type':'color', 'name': 'color'},
	'da1': {'type':'date', 'name': 'begin date'},
	'da2': {'type':'date', 'name': 'end date'},
	'da3': {'type':'date', 'name': 'birthday'},
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


# Create your views here.

def index(request,formstring=""):

	form = ''
	id_counts = dict()
	name_counts = dict()

	formset= wrap(formstring,3)
	print("Formset = {}".format(formset))
	for i in formset:
		if i in id_counts:
			id_counts[i] += 1
		else:
			id_counts[i] = 1
		if i in formInput:
			if id_counts[i] > 1:
				form = form + '<input id="' + i + '_'+str(id_counts[i])+'" '
			else:
				form = form + '<input id="' + i + '" '
			for j in formInput[i]:
				if j.lower() == 'name':
					if formInput[i][j] in name_counts:
						name_counts[formInput[i][j]] += 1
						form = form + j  +  '="' + formInput[i][j]+ '_' + str(name_counts[formInput[i][j]]) + '" '
					else:
						name_counts[formInput[i][j]] = 1
						form = form + j  +  '="' + formInput[i][j]+ '" '
				else:
					form = form + j +  '="' + formInput[i][j]+ '" '
			form = form + ' > </p> \n'
		else:
			print("WARNING: unknown field '{}', skipping".format(i))

	form = form + '<input type="submit" value="Submit" />'
	print(form)
	context = { 'formstring': formstring , 'formset': formset, 'form': form, 'version': VERSION}

	if request.method =='POST':
		rawPost = deepcopy(request.POST)
		del rawPost['csrfmiddlewaretoken'] # remove csrfmiddlewaretoken, unneeded information 
		rawPost['epoch']=int(time.time())
		rawPost['datetime']=str(datetime.datetime.now())
		print(json.dumps(rawPost))
		# reset for to a back link
		form ="<a href='{0}'>return to form</a>".format(request.path)
		context = { 'formstring': formstring , 'formset': formset, 'form': form, 'rawpost': rawPost, 'version': VERSION}
		return render(request,'forms/form.html', context)

	return render(request,'forms/form.html', context)
