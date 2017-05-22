from __future__ import print_function
from django.shortcuts import render
from .models import *
import requests
import random
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from login.models import user_data
import jwt
import sendotp
from django.core.mail import send_mail
from django.core.mail import EmailMessage

# Create your views here.

@csrf_exempt
def get_otp(request):
	if request.method == 'GET':
		response_json = {}
		try:
			# # url='https://control.msg91.com/api/sendhttp.php?authkey=152879AMa1te4hi0r6591d655f&mobiles=91'
			# url='https://control.msg91.com/api/sendotp.php?authkey=152879AMa1te4hi0r6591d655f&mobile=91'
			name = str(request.GET.get('name'))
			mobile = str(request.GET.get('mobile'))
			email = str(request.GET.get('email'))
			# name = "Aman Agrawal"
			# mobile = "8109573930"
			# email = "amanjain.1596@gmail.com"
			print(mobile)
			print(email)
			print(name)

			n=random.randint(1000,9999)
			# url+=str(mobile)
			otp=str(n)
			# url+= '&message='+'%5CnYour%20One%20Time%20Password%3A%20'+otp
			# # url+='&sender=mCNice&route=4'
			# url+='&sender=CodeNy&otp='+ otp
			# result =requests.request('GET',url)
			# print(url)
			# print otpobj.verify(910000000000,3245)

			# print otpobj.retry(910000000000) OR
			# print otpobj.retry(910000000000,'text')

			try:
				send_mail('CodeNicely OTP','Your One Time Password is :'+ otp,'amanjain.6951@gmail.com',[email],fail_silently=False)
				otpobj =  sendotp.sendotp('152879AMa1te4hi0r6591d655f','Your Verification code is {{otp}}.')
				print(otpobj.send(int(mobile),'mCNICE',int(otp)))
				try:
					otp_list= otp_data.objects.get(mobile= str(mobile))
					print(otp)
					setattr(otp_list, 'flag',False)
					otp_list.save()
					print("Old User")

				except Exception as e:
					otp_data.objects.create(mobile=str(mobile),email = str(email),name=str(name))

				otp_list= otp_data.objects.get(mobile= str(mobile))
				setattr(otp_list, 'otp',int(otp))
				otp_list.save()
				response_json['success']=True
				response_json['message']="Otp Sent Successfully"

			except Exception as e:
				response_json['success']=False
				response_json['message']="Otp Not Send"	
				# email = EmailMessage('CodeNicely OTP', 'Your One Time Password is :'+ otp, to=[email])
				# email.send()
				# print(result)
		except Exception as  e:
			response_json['success']= False
			response_json['message']= "Failed"
			print(e)
		print(str(response_json))
		# return JsonResponse(response_json)
		return HttpResponse(str(response_json))

@csrf_exempt
def verify_otp(request):
	# if request.method == 'POST':
		response_json = {}	
		try:
			mobile =str(request.POST.get('mobile'))
			otp =str(request.POST.get('otp'))
			access_token = 'Null'
			print(mobile)
			print(otp)
			otp_list= otp_data.objects.get(mobile= str(mobile))
			print(mobile)
			name = otp_list.name
			mobile = otp_list.mobile
			email = otp_list.email
			if otp_list.otp == int(otp):
				setattr(otp_list,'flag',True)
				access_token = jwt.encode({'mobile': str(mobile)}, '810810',algorithm = 'HS256')
				otp_list.save()
				try:
					user_list= user_data.objects.get(mobile = str(mobile))
					setattr(user_list, 'name', name)
					setattr(user_list,'email',email)
					user_list.save()
					print('User Details Updated')
				except:
					user_data.objects.create(
						name=name,
						email=email,
						mobile=str(mobile)
						)
					print('User Created')
					print(e)

				response_json['access_token']= str(access_token)
				print('Access Token Created')

				# json=jwt.decode(str(access_token),'999123',algorithms= 'HS256')
				response_json['success']=True
				response_json['message']='Success'
			else:
				response_json['success'] = False
				response_json['message'] = 'Invalid Otp'

		except Exception as e:
			response_json['success'] = False
			response_json['message'] = 'Invalid Mobile Number'
			print(e)
			print(str(response_json))
		return JsonResponse(response_json)