from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from .models import FakeLeg, Date, Guest, Img
from django.core.mail import send_mail
from django.views.decorators import csrf
from django.db import IntegrityError

from django.shortcuts import get_object_or_404,render,redirect
from django.urls import reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType

# Submit query form
def search_form(request):
	return render_to_response('search_form.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# Deal with query
def search(request):
	request.encoding='utf-8'
	response = ""
	response1 = ""
	dic = {}
	if 'arrive' in request.GET and 'departure' in request.GET and 'suburb' in request.GET and 'person' in request.GET and 'price1' in request.GET and 'price2' in request.GET:
		b = 0
		c = 100000
		if request.GET['price1'] != '':
			b = int(request.GET['price1'])
		if request.GET['price2'] != '':
			c = int(request.GET['price2'])  
		if request.GET['suburb'] != '' :

			if request.GET['suburb'] =='All':
				not_use=1
			else:
				dic['suburb'] = request.GET['suburb'].lower()

		flag = False
		if request.GET['person'] != '' :
			if request.GET['person'] == 'All':
				not_use=1
			else:
				a = int(request.GET['person'])
				if a == 5:
					flag = True
				else:
					dic['tenant_num'] = a

		if dic != {}:
			if flag == True:
				li = FakeLeg.objects.filter(tenant_num__gte=5).filter(**dic)
			else:
				li = FakeLeg.objects.filter(**dic)
		else:
			if flag == True:
				li = FakeLeg.objects.filter(tenant_num__gte=5)
			else:
				li = FakeLeg.objects.all()

		date_range = []
		if request.GET['arrive'] != '' and request.GET['departure'] != '':
			s_d = request.GET['arrive'].split('/')
			s_d = int(s_d[2] + s_d[0] + s_d[1])
			e_d = request.GET['departure'].split('/')
			e_d = int(e_d[2] + e_d[0] + e_d[1])
			for i in range(s_d, e_d):
				current = str(i)
				d = current[4:6] + '/' + current[6:8] + '/' + current[0:4]
				date_range.append(d)
		print(date_range)
		res = []
		for var in li:
			fl = False
			dates = Date.objects.filter(PID_id=var.id)
			for date in dates:
				if date.booked_date in date_range:
					fl = True
					break
			if fl == True:
				continue
			if var.price < b or var.price > c:
				continue
			res.append(var)
		response = response1
		return render(request, "search_result.html", {'res': res})
	else:
		message = ''
	return HttpResponse(message)

# Indexing specific property
def index(request, ids):
	results = FakeLeg.objects.get(id=ids)
	dates = Date.objects.filter(PID_id=ids)
	images = Img.objects.filter(PID_id=ids)
	return render(request, "property.html", {'results': results, 'dates': dates, 'images': images})

# Submit booking form
def book_form(request, ids):
	return render(request, 'book_form.html', {'id': ids})

# Process book request 
def book(request, ids, uid):
	request.encoding='utf-8'
	try:
		if request.method == 'GET':
			message = 'Booking'
			s_d = request.GET['arrive'].split('/')
			e_d = request.GET['departure'].split('/')
			start = s_d[2] + s_d[0] + s_d[1]
			end = e_d[2] + e_d[0] + e_d[1]
			duration = int(end) - int(start)
			guest = Guest(first_name=request.GET['f_name'], last_name=request.GET['l_name'], mobile=int(request.GET['mobile']), email=request.GET['email'], start_date=request.GET['arrive'], duration=duration, ID_number=int(request.GET['id_num']), st_number=int(request.GET['st_num']), st_name=request.GET['st_name'], suburb=request.GET['suburb'], state=request.GET['state'], card_number=int(request.GET['card_num']), PID_id=ids, UID=uid)
			guest.save()
			newg = Guest.objects.get(first_name=request.GET['f_name'], last_name=request.GET['l_name'], mobile=int(request.GET['mobile']), email=request.GET['email'], start_date=request.GET['arrive'], duration=duration, ID_number=int(request.GET['id_num']), st_number=int(request.GET['st_num']), st_name=request.GET['st_name'], suburb=request.GET['suburb'], state=request.GET['state'], card_number=int(request.GET['card_num']), PID_id=ids, UID=uid)
			current_date = int(start)
			for i in range(duration):
				c_d = str(current_date)
				c_d = c_d[4:6] + '/' + c_d[6:8] + '/' + c_d[0:4]
				date = Date(booked_date=c_d, PID_id=ids, RID_id=newg.id)
				date.save()
				current_date += 1
			# send_mail('Booking Successfully', 'New Booking', '513339224@qq.com', [request.GET['email']], fail_silently=False)
			return render(request, 'success.html', {'message': message})
	except IndexError as e:
		return render(request, 'date_check.html')
	except IntegrityError as e:
		try:
			ntd = Guest.objects.get(id=newg.id)
			ntd.delete()
			return render(request, 'book_overlap.html')
		except UnboundLocalError as error:
			return render(request, 'book_overlap.html')

# Process new property post request
def post(request, ids):
	ctx ={}
	if request.POST:
		message = 'Post'
		state = 'NSW'
		suburb = request.POST['suburb']
		st_number = request.POST['st_num']
		st_name = request.POST['st_name']
		house_type = request.POST['house_type']
		pet = request.POST['pet']
		wifi = request.POST['wifi']
		kitchen = request.POST['kitchen']
		laundry = request.POST['laundry']
		park_lot = request.POST['park_lot']
		tenant_num = request.POST['person']
		price = request.POST['price']
		brief_intro = request.POST['brief_intro']
		fi = request.FILES.get('img')
		newp = FakeLeg(UID=ids, state=state, suburb=suburb, tenant_num=tenant_num, price=price, st_number=st_number, st_name=st_name, house_type=house_type, pet=pet, wifi=wifi, kitchen=kitchen, laundry=laundry, park_lot=park_lot, brief_intro=brief_intro, img_url=fi)
		newp.save()
		posted = FakeLeg.objects.get(UID=ids, state=state, suburb=suburb, tenant_num=tenant_num, price=price, st_number=st_number, st_name=st_name, house_type=house_type, pet=pet, wifi=wifi, kitchen=kitchen, laundry=laundry, park_lot=park_lot, brief_intro=brief_intro)
		files = request.FILES.getlist('img')
		for f in files:
			newi = Img(PID_id=posted.id, img_url=f)
			newi.save()
		return render(request, "success.html", {'message': message})
	return render(request, "post_form.html", {'id': ids})

def user_posted(request, ids):
	my_property = FakeLeg.objects.filter(UID=ids)
	return render(request, "my_property.html", {"res": my_property})
	
def review(request, ids):
	results = FakeLeg.objects.get(id=ids)
	images = Img.objects.filter(PID_id=ids)
	return render(request, "property_review.html", {'results': results, 'images': images})

def edit_form(request, ids):
	res = FakeLeg.objects.get(id=ids)
	return render(request, "edit_form.html", {'res': res})

def edit(request, ids):
	request.encoding='utf-8'
	if request.GET:
		message = 'Edit'
		state = request.GET['state']
		suburb = request.GET['suburb']
		st_number = request.GET['st_num']
		st_name = request.GET['st_name']
		house_type = request.GET['house_type']
		pet = request.GET['pet']
		wifi = request.GET['wifi']
		kitchen = request.GET['kitchen']
		laundry = request.GET['laundry']
		park_lot = request.GET['park_lot']
		tenant_num = request.GET['person']
		price = request.GET['price']
		brief_intro = request.GET['brief_intro']
		FakeLeg.objects.filter(id=ids).update(state=state, suburb=suburb, tenant_num=tenant_num, price=price, st_number=st_number, st_name=st_name, house_type=house_type, pet=pet, wifi=wifi, kitchen=kitchen, laundry=laundry, park_lot=park_lot, brief_intro=brief_intro)
		return render(request, "success.html", {'message': message})
		
def delete(request, ids):
	message = 'Delete'
	prop = FakeLeg.objects.get(id=ids)
	Img.objects.filter(PID_id=ids).delete()
	prop.delete()
	return render(request, "success.html", {'message': message})
		
def add_img(request, ids):
	if request.method == 'POST':
		urls = request.FILES.getlist('img')
		for url in urls:
			img = Img(PID_id=ids, img_url=url)
			img.save()
	return render(request, "add-img.html", {'id': ids})
	
def del_img(request, ids):
	imgs = Img.objects.filter(PID_id=ids)
	return render(request, "del-img.html", {'imgs': imgs})
		
def del_pic(request, ids):
	message = 'Delete'
	img = Img.objects.get(id=ids)
	img.delete()
	return render(request, "success.html", {'message': message})
		
def user_booked(request, ids):
	res = dict()
	results = Guest.objects.filter(UID=ids)
	for result in results:
		r = FakeLeg.objects.get(id=result.PID_id)
		res[result.id] = [result, r]
	print(res)
	return render(request, "my_booking.html", {'res': res})
	
	
def book_review(request, ids):
	res = Guest.objects.get(id=ids)
	return render(request, "book_review.html", {'res': res})
	
def book_edit_form(request, ids):
	res = Guest.objects.get(id=ids)
	res1 = FakeLeg.objects.get(id=res.PID_id)
	return render(request, "book_edit.html", {'res': res, 'res1': res1})
	
def book_edit_process(request, ids):
	return render(request, "apply_process.html")
		
	
def book_delete(request, ids):
	res = Guest.objects.get(id=ids)
	res1 = FakeLeg.objects.get(id=res.PID_id)
	return render(request, "book_delete.html", {'res': res, 'res1': res1})
	
def book_delete_process(request, ids):
	return render(request, "apply_process.html")


def comment(request,id):
    property = get_object_or_404(FakeLeg,id=id)
    property_content_type =ContentType.objects.get_for_model(property)
    comments = Comment.objects.filter(content_type=property_content_type,object_id = id,parent=None)


    context = {}
    context['property'] = property
    context['comments'] = comments

    response = render(request,'comment.html',context)
    return response

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': 'you should login ','redirect_to':referer})

    text = request.POST.get('text','').strip()
    #if comment is empty, return an error
    if text == '':
        return render(request,'error.html',{'message': 'Comment content is empty','redirect_to':referer})




    """
    try:

        # content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', '0'))
        # model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = ContentType.objects.get(id=object_id)

    except Exception as e:
        return render(request, 'error.html', {'message': 'Comment object does not exist','redirect_to':referer})
    """

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', '0'))
        model_class = ContentType.objects.get(app_label='property', model=content_type).model_class()
        model_obj = model_class.objects.get(id=object_id)

    except Exception as e:
        return render(request, 'error.html', {'message': 'Comment object does not exist','redirect_to':referer})

    #if all requirements is obeyed, then generate the model instance
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer)
	
	
	
			
		