from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Trunk, Room, Soup, Activity

import re

def home(request):
    if request.method == 'POST':
        
        def make_row_and_cookie(Obj, name, cookie_name):
            obj = Obj(name=name)
            obj.save()
            name_dashes = re.sub(' ', '-', name)#convert any spaces in name to dashes for cookie storage
            response = HttpResponseRedirect('/trunk')
            response.set_cookie(cookie_name, name_dashes, max_age=4233600)
            return response

        def delete_row_and_cookie(Obj, name, cookie_name):
            obj = Obj.objects.filter(name=name)
            obj.delete()
            name_dashes = re.sub(' ', '-', name)#convert any spaces in name to dashes for cookie storage
            response = HttpResponseRedirect('/trunk')#delete cookie and redirect to same page
            response.delete_cookie(cookie_name)
            return response

        if request.POST['submit'] == "I'm bringing a trunk!":
            return make_row_and_cookie(Trunk, request.POST['name'], 'trunk')           
        elif request.POST['submit'] == "I want a room!":
            return make_row_and_cookie(Room, request.POST['name'], 'room')                            
        elif request.POST['submit'] == "I'm making soup!":
            return make_row_and_cookie(Soup, request.POST['name'], 'soup')                
        elif request.POST['submit'] == "Delete trunk signup":
            return delete_row_and_cookie(Trunk, request.POST['name'], 'trunk')
        elif request.POST['submit'] == "Delete room signup":
            return delete_row_and_cookie(Room, request.POST['name'], 'room')
        elif request.POST['submit'] == "Delete soup signup":
            return delete_row_and_cookie(Soup, request.POST['name'], 'soup')
        
        elif request.POST['submit'] == "Submit an activity!":
            name = request.POST['name']
            activity = request.POST['activity']
            idea = Activity(name=name, activity=activity)
            idea.save()
            name_dashes = re.sub(' ', '-', name)#convert any spaces in name to dashes for cookie storage
            response = HttpResponseRedirect('/trunk/confirmation')
            response.set_cookie('activity', name_dashes, max_age=4233600)
            return response
    else:
        
        def context_dict_and_flag(Obj, cookie_name):
            context_list = []
            objects = Obj.objects.all()
            if cookie_name in request.COOKIES.keys():
                name = re.sub('-', ' ', request.COOKIES[cookie_name])
                for obj in objects:
                    if obj.name == name:
                        added_flag = True
                        context_list.append({'name':name, 'allow_delete':True})
                    else:
                        context_list.append({'name':obj.name, 'allow_delete':False})
            else:
                context_list = [{'name':obj.name, 'allow_delete':False} for obj in objects]
                added_flag = False
            return context_list, added_flag
        trunks, trunk_added = context_dict_and_flag(Trunk, 'trunk')
        rooms, room_added = context_dict_and_flag(Room, 'room')
        soups, soup_added = context_dict_and_flag(Soup, 'soup')


        activities = Activity.objects.filter(approved=True)

        context = {
            'trunks':trunks,
            'trunk_added':trunk_added,
            'rooms':rooms,
            'room_added':room_added,
            'soups':soups,
            'soup_added':soup_added,
            'activities':activities,
        }
    return render(request, 'trunk_or_treat/home.html', context)

def confirmation(request):
    return render(request, 'trunk_or_treat/confirmation.html')