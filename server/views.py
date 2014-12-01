from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from server.models import File
from server.forms import FileForm
from server.forms import StudyForm
from pyper import R
import datetime
import csv
import os

def index(request):
    context = RequestContext(request)
    user = request.user
    filepath = "media/server/%s" % user
    if os.path.exists(filepath)==False:
        os.mkdir(filepath)
    context_dict = {'testmsg': "It works!"}
    #print(context_dict['targets'])
    return render_to_response('server/index.html', context_dict, context)
	
@login_required	
def manage_studies(request):
    context = RequestContext(request)
    context_dict = {}
    user = request.user
    filepath = "media/server/%s" % user
    study_list = []
    for dir in os.listdir(filepath):
        if dir != "study.txt":
            study_list.append(dir)
    context_dict['studies'] = study_list
    form = StudyForm()
    context_dict['form'] = form
    return render_to_response('server/manage_studies.html', context_dict, context)
	
@login_required	
def choose_study(request, study):
    context = RequestContext(request)
    user = request.user
    filepath = "media/server/%s/" % user
    f = open(filepath + "study.txt", 'w')
    f.write(study)
    f.close()
    return render_to_response('server/index.html', {}, context)
	
@login_required	
def remove_study(request, study):
    context = RequestContext(request)
    user = request.user
    filepath = "media/server/%s/" % user
    os.remove(filepath+study)
    return render_to_response('server/index.html', {}, context)

@login_required	
def create_study(request):
    context = RequestContext(request)
    form = StudyForm(request.POST)
    if form.is_valid():
        user = request.user
        filepath = "media/server/%s/" % user
        if os.path.exists(filepath+form.cleaned_data['study']):
            return render(request, 'server/error.html', {'message': "Study already exists"})
        os.mkdir(filepath+form.cleaned_data['study'])
        f = open(filepath + "study.txt", 'w')
        f.write(form.cleaned_data['study'])
        f.close()
    return render(request, 'server/index.html', [])

@login_required	
def choose_target(request):
    context = RequestContext(request)
    user = request.user
    filepath = "media/server/%s/" % user
    f = open(filepath + "study.txt", 'r')
    study = f.read()
    f.close()
    filepath += study+"/"
    context_dict = {}
    #current target
    try:
        with open(filepath+'target.csv', newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
            for row in spamreader:
                context_dict['target'] = row
                break
    except:
        context_dict['target'] = 'none'
    #list aviable targets
    try:
        with open(filepath+'targets.csv', newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
            for row in spamreader:
                context_dict['targets'] =  row
                break
    except:
        return render_to_response('server/choose_target.html', context_dict, context)
    return render_to_response('server/choose_target.html', context_dict, context)

@login_required	
def set_target(request, target):
    context = RequestContext(request)
    user = request.user
    filepath = "media/server/%s/" % user
    f = open(filepath + "study.txt", 'r')
    study = f.read()
    f.close()
    filepath += study+"/"
    with open(filepath + "targets.csv", newline = '') as csvread:
        with open(filepath + "target.csv", 'w', newline='') as csvwrite:
            spamwriter = csv.writer(csvwrite, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamreader = csv.DictReader(csvread, delimiter = ';', quotechar = '|')
            spamwriter.writerow([target])
            for row in spamreader:
                spamwriter.writerow(row[target])
    return render_to_response('server/index.html', {}, context)


@login_required	
def results(request):
    context = RequestContext(request)
    user = request.user
    filename = "static/server/%s_message.txt" % user
    f= open(filename, "r")
    message = f.read()
    f.close
    filename = "static/server/%s_testowy.pdf" % user
    message2 = ""
    if os.path.exists(filename) == False:
        message2 = "No results"
    return render_to_response('server/results.html', {'message': message, 'message2' : message2}, context)
	
def handle_uploaded_file(request, name):
    user = request.user
    form = request.FILES['file']
    filepath = "media/server/%s/" % user
    f = open(filepath + "study.txt", 'r')
    study = f.read()
    f.close()
    filepath += study+"/"
    with open(filepath + name, 'wb+') as dest:
        for chunk in form.chunks():
            dest.write(chunk)

@login_required			
def add_data(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            #page = form.save(commit=True)
            handle_uploaded_file(request, 'data.csv')
            return index(request)
        else:
            print(form.errors)
    else:
        form = FileForm()
    return render_to_response( 'server/add_data.html', {'form': form}, context)

@login_required
def add_targets(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            #page = form.save(commit=True)
            handle_uploaded_file(request, 'targets.csv')
            return index(request)
        else:
            print(form.errors)
    else:
        form = FileForm()
    return render_to_response( 'server/add_targets.html', {'form': form}, context)
	
@login_required
def run_rscript(request):
    user = request.user
    datapath = "media/server/%s/" % user
    if os.path.exists(datapath+"study.txt")==False:
        return render(request, 'server/error.html', {'message': "No study"})
    f = open(datapath + "study.txt", 'r')
    study = f.read()
    f.close()
    datapath += study
    target = ""
    try:
        with open(datapath + "/target.csv", newline = '') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ';', quotechar = '|')
            for row in spamreader:
                target = row
                break
    except:
        return render(request, 'server/error.html', {'message': "No target"})
    message = "Results of user %s on " % user
    message += "Date: " +  datetime.datetime.now().strftime("%y-%m-%d %H:%M")
    message += ", Target: " + target[0]
    message += ", Study: " + study
    message += '\n'
    if os.path.exists(datapath+"/data.csv")==False:
        return render(request, 'server/error.html', {'message': "No data file"})
    r = R(use_numpy=True)
    r("datadir2<-\""+datapath+"\"; source('server/r_files/globaltest-przyklad-kodnaserwer.r')")
    del(r)
    filename = "static/server/%s_message.txt" % user
    f= open(filename, "w")
    f.write(message)
    f.close()
    filename = "static/server/%s_testowy.pdf" % user
    if os.path.exists(filename)==True:
        os.remove(filename)
    while os.path.exists("static/server/testowy.pdf")==False:
        continue
    os.rename("static/server/testowy.pdf", filename)
    filename = "media/server/{0}/{1}/{0}_out.txt".format(user, study)
    if os.path.exists(filename)==True:
        os.remove(filename)
    while os.path.exists("static/server/out.txt")==False:
        continue
    os.rename("static/server/out.txt", filename)
	#os.system("Rscript server/r_files/globaltest-przyklad-kodnaserwer.r")
    return render(request, 'server/results.html', {'study':study})